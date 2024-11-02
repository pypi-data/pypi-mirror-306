import os
import unittest
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import sys
import asyncio

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vectrs.database.vectrbase import VectorDBManager, IndexType, SimilarityMetric
from vectrs.swarms.main import Swarm
from vectrs.swarms.llm.anthropic_llm import AnthropicLLM
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.network import KademliaNode
from vectrs.networking.message_broker import MessageBroker

# Load environment variables
load_dotenv()

# API keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Initialize SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

class TestRAGSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.db_manager = VectorDBManager()
        cls.db_id = cls.loop.run_until_complete(cls.create_database())
        cls.vector_db = VectorDB(cls.db_manager, cls.db_id)
        cls.llm = AnthropicLLM(ANTHROPIC_API_KEY)
        cls.node = KademliaNode(host="localhost", port=8000)
        cls.message_broker = MessageBroker(cls.node)
        cls.swarm = Swarm(cls.vector_db, "localhost", 8000)

    @classmethod
    async def create_database(cls):
        return cls.db_manager.create_database(
            dim=model.get_sentence_embedding_dimension(),
            space=SimilarityMetric.COSINE,
            max_elements=1000,
            index_type=IndexType.HNSW
        )

    def setUp(self):
        # Add some sample data to the vector database
        self.loop.run_until_complete(self.add_to_vector_db("The capital of France is Paris.", {"topic": "geography"}))
        self.loop.run_until_complete(self.add_to_vector_db("Python is a popular programming language.", {"topic": "technology"}))
        self.loop.run_until_complete(self.add_to_vector_db("The Eiffel Tower is located in Paris.", {"topic": "landmarks"}))

    async def add_to_vector_db(self, content: str, metadata: Dict[str, Any] = None):
        embedding = model.encode([content])[0]
        vector_id = f"vector_{len(self.db_manager.get_database(self.db_id).id_map)}"
        metadata = metadata or {}
        metadata["content"] = content  # Store the content in the metadata
        self.db_manager.add_vector(self.db_id, vector_id, embedding, metadata)

    async def query_vector_db(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_embedding = model.encode([query])[0]
        db = self.db_manager.get_database(self.db_id)
        results = db.knn_query(query_embedding, k=top_k)
        return [{"content": db.get(r[0])[1].get("content", ""), "metadata": r[2]} for r in results]

    def test_vector_db_query(self):
        results = self.loop.run_until_complete(self.query_vector_db("What is the capital of France?"))
        self.assertEqual(len(results), 3)
        self.assertIn("Paris", results[0]["content"])

    def test_rag_workflow(self):
        question = "Tell me about the capital of France."
        result = self.loop.run_until_complete(self.swarm.run_rag_workflow(question))
        
        self.assertIsNotNone(result)
        self.assertIn('query', result)
        self.assertIn('retrieved_context', result)
        self.assertIn('plan', result)
        self.assertIn('generated_answer', result)
        self.assertIn('reflection', result)
        
        self.assertEqual(result['query'], question)
        self.assertIn("Paris", result['retrieved_context'])
        self.assertIn("capital", result['plan'])
        self.assertIn("Paris", result['generated_answer'])
        self.assertIn("France", result['generated_answer'])

    def test_swarm_task_analysis(self):
        task = {
            "type": "complex_task",
            "data": "Analyze the economic impact of climate change on coastal cities."
        }
        analysis = self.loop.run_until_complete(self.swarm.analyze_task(task))
        
        self.assertIn("required_skills", analysis)
        self.assertIn("complexity", analysis)
        self.assertIn("dependencies", analysis)
        self.assertIn("estimated_duration", analysis)
        
        self.assertGreater(len(analysis["required_skills"]), 0)
        self.assertGreater(analysis["complexity"], 1)
        self.assertGreater(analysis["estimated_duration"], 0)

    def test_swarm_custom_agent_creation(self):
        agent = self.loop.run_until_complete(self.swarm.create_custom_agent("reflection", "custom_reflection_agent"))
        self.assertIsNotNone(agent)
        self.assertEqual(agent.agent_id, "custom_reflection_agent")
        self.assertIn("self-evaluation", agent.skills)

if __name__ == '__main__':
    unittest.main()
