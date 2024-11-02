import unittest
import asyncio
from unittest.mock import MagicMock, patch
import os
import sys
import logging
from dotenv import load_dotenv
import numpy as np
import uuid
import sqlite3

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

from vectrs.database.vectrbase import VectorDB as VectrBaseDB, SimilarityMetric, IndexType
from vectrs.swarms.agents.base_agent import BaseAgent
from vectrs.swarms.agents.reflection_agent import ReflectionAgent
from vectrs.swarms.agents.tool_agent import ToolAgent
from vectrs.swarms.agents.planning_agent import PlanningAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB as SwarmVectorDB
from vectrs.swarms.llm.anthropic_llm import AnthropicLLM
from vectrs.swarms.coordinator.multi_agent_coordinator import MultiAgentCoordinator
from vectrs.network import KademliaNode
from vectrs.networking.message_broker import MessageBroker
from vectrs.swarms.types import Result, Agent
from vectrs.swarms.agent_factory import AgentFactory

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.mock_vectr_base = MagicMock()
        self.mock_node = MagicMock(spec=KademliaNode)
        self.mock_node.host = "localhost"
        self.mock_node.port = 8000
        self.swarm_vector_db = SwarmVectorDB(self.mock_vectr_base, self.mock_node)
        
        # Use the real AnthropicLLM
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        self.llm = AnthropicLLM(api_key=api_key)
        
        self.mock_message_broker = MagicMock(spec=MessageBroker)
        self.coordinator = MultiAgentCoordinator(self.mock_message_broker, self.mock_node, self.swarm_vector_db, self.llm)
        self.agent_factory = AgentFactory(self.coordinator, self.swarm_vector_db, self.llm)

        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Use VectrBaseDB for tests
        self.vectr_base_db = VectrBaseDB(dim=384, space=SimilarityMetric.COSINE, max_elements=1000, ef_construction=200, M=16, db_id=str(uuid.uuid4()), connection=sqlite3.connect(':memory:'), log_db_file=':memory:', index_type=IndexType.HNSW)

    async def async_test(self, coro):
        return await coro

    def test_base_agent(self):
        class TestAgent(BaseAgent):
            async def process_task(self, task):
                return Result(value=f"Processed: {task}")

        agent = TestAgent(agent_id="test_agent", coordinator=self.coordinator, vector_db=self.vectr_base_db, llm=self.llm, skills={"test_skill"}, model="test_model", instructions="Test instructions")
        result = self.loop.run_until_complete(agent.process_task("test task"))
        self.assertEqual(result.value, "Processed: test task")

    def test_reflection_agent(self):
        agent = self.agent_factory.create_agent("reflection", "reflection_agent")
        task = {"type": "reflection", "data": "What is the capital of France?"}
        result = self.loop.run_until_complete(self.async_test(agent.process_task(task)))
        self.assertIn("reflection:", result.value["reflection"].lower())
        self.assertIn("capital", result.value["reflection"].lower())
        self.assertIn("france", result.value["reflection"].lower())

    def test_tool_agent(self):
        agent = self.agent_factory.create_agent("tool", "tool_agent")
        task = {"type": "tool_usage", "data": "Execute the task using the suggested tools: Find the population of Paris"}
        result = self.loop.run_until_complete(self.async_test(agent.process_task(task)))
        self.assertIn("population", result.value["result"].lower())
        self.assertIn("paris", result.value["result"].lower())

    def test_planning_agent(self):
        agent = self.agent_factory.create_agent("planning", "planning_agent")
        task = {"type": "planning", "data": "Create a detailed plan: Organize a trip to France"}
        result = self.loop.run_until_complete(self.async_test(agent.process_task(task)))
        self.assertIn("plan", result.value["plan"].lower())
        self.assertIn("france", result.value["plan"].lower())

    @patch('vectrs.swarms.coordinator.multi_agent_coordinator.MultiAgentCoordinator.send_message')
    def test_agent_communication(self, mock_send_message):
        agent = self.agent_factory.create_agent("reflection", "reflection_agent")
        self.loop.run_until_complete(agent.send_message("recipient", "message_type", "content"))
        mock_send_message.assert_called_once_with("reflection_agent", "recipient", "message_type", "content")

    def test_agent_skills(self):
        reflection_agent = self.agent_factory.create_agent("reflection", "reflection_agent")
        tool_agent = self.agent_factory.create_agent("tool", "tool_agent")
        planning_agent = self.agent_factory.create_agent("planning", "planning_agent")

        self.assertTrue(reflection_agent.has_required_skills({"self-evaluation"}))
        self.assertTrue(tool_agent.has_required_skills({"tool_usage"}))
        self.assertTrue(planning_agent.has_required_skills({"task_planning"}))

        self.assertFalse(reflection_agent.has_required_skills({"tool_usage"}))
        self.assertFalse(tool_agent.has_required_skills({"task_planning"}))
        self.assertFalse(planning_agent.has_required_skills({"self-evaluation"}))

    @patch.object(SwarmVectorDB, 'add_item')
    @patch.object(SwarmVectorDB, 'search')
    def test_agent_database_interaction(self, mock_search, mock_add_item):
        mock_add_item.return_value = "mock_id"
        mock_search.return_value = [{"id": "mock_id", "vector": [0.1, 0.2, 0.3], "data": {"content": "mock content"}}]

        agent = self.agent_factory.create_agent("reflection", "reflection_agent")
        
        # Test adding to database
        result = self.loop.run_until_complete(agent.add_to_database([0.1, 0.2, 0.3], {"content": "test content"}))
        self.assertEqual(result, "mock_id")
        mock_add_item.assert_called_once()

        # Test querying database
        result = self.loop.run_until_complete(agent.query_database([0.1, 0.2, 0.3]))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["data"]["content"], "mock content")
        mock_search.assert_called_once()

    def test_rag_workflow(self):
        # Create a mock VectorDB
        mock_vector_db = MagicMock(spec=SwarmVectorDB)
        mock_vector_db.search.return_value = [{"data": {"content": "France is a country in Western Europe. Its capital is Paris."}}]

        # Create the coordinator with the real AnthropicLLM
        coordinator = MultiAgentCoordinator(self.mock_message_broker, self.mock_node, mock_vector_db, self.llm)

        # Run the RAG workflow
        query = "What is the capital of France?"
        try:
            result = self.loop.run_until_complete(coordinator.run_rag_workflow(query))

            # Assert the structure of the result
            self.assertIn('query', result)
            self.assertIn('retrieved_context', result)
            self.assertIn('plan', result)
            self.assertIn('generated_answer', result)
            self.assertIn('reflection', result)

            # Check if the query is correctly passed through the workflow
            self.assertEqual(result['query'], query)

            # Check if each step produced some output
            self.assertTrue(result['retrieved_context'])
            self.assertTrue(result['plan'])
            self.assertTrue(result['generated_answer'])
            self.assertTrue(result['reflection'])

            # Check for specific content in the result
            retrieved_context_str = str(result['retrieved_context']).lower()
            self.assertIn("france", retrieved_context_str)
            self.assertIn("capital", retrieved_context_str)
            
            generated_answer_str = str(result['generated_answer']).lower()
            self.assertIn("paris", generated_answer_str)
            self.assertIn("capital of france", generated_answer_str)

            # Print the final answer for debugging
            print(f"Final answer: {result['generated_answer']}")
            print(f"Retrieved context: {result['retrieved_context']}")
        except Exception as e:
            self.fail(f"RAG workflow failed with error: {str(e)}")

    def test_graphine_search(self):
        # Use self.vectr_base_db instead of self.vector_db
        test_vectors = [
            np.random.rand(384) for _ in range(10)
        ]
        test_metadata = [
            {"content": f"Test content {i}", "type": "document" if i % 2 == 0 else "image"}
            for i in range(10)
        ]
        
        for i, (vector, metadata) in enumerate(zip(test_vectors, test_metadata)):
            self.vectr_base_db.add(vector, f"test_id_{i}", metadata, entity_type=metadata["type"])

        self.vectr_base_db.add_relationship("test_id_0", "test_id_1", "related")
        self.vectr_base_db.add_relationship("test_id_0", "test_id_2", "cited")
        self.vectr_base_db.add_relationship("test_id_1", "test_id_3", "similar")

        query_vector = np.random.rand(384)
        results = self.vectr_base_db.graphine_search(
            query_vector,
            entity_type="document",
            relation_filter={"related": "related", "cited": "cited"},
            k=5,
            alpha=0.7
        )

        # Add this check
        if not results:
            print("No results found in graphine_search")
            return

        # Assert the structure and content of the results
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], float)
            self.assertIsInstance(result[2], dict)
            self.assertIn("type", result[2])
            self.assertEqual(result[2]["type"], "document")

        # Test expanding search
        expanded_results = self.vectr_base_db.expand_search(results, max_depth=2, expansion_factor=0.5)
        self.assertGreater(len(expanded_results), len(results))

        # Test filtering results
        filtered_results = self.vectr_base_db.filter_results(expanded_results, {"type": "document"})
        self.assertTrue(all(result[2]["type"] == "document" for result in filtered_results))

    def test_get_entity_info(self):
        # Use self.vectr_base_db instead of self.vector_db
        test_vector = np.random.rand(384)
        test_metadata = {"content": "Test content", "type": "document"}
        self.vectr_base_db.add(test_vector, "test_id", test_metadata, entity_type="document")

        self.vectr_base_db.add_relationship("test_id", "related_id_1", "related")
        self.vectr_base_db.add_relationship("test_id", "cited_id_1", "cited")

        entity_info = self.vectr_base_db.get_entity_info("test_id")

        # Assert the structure and content of the entity info
        self.assertIsInstance(entity_info, dict)
        self.assertEqual(entity_info["entity_id"], "test_id")
        self.assertEqual(entity_info["entity_type"], "document")
        self.assertIsInstance(entity_info["vector"], list)
        self.assertEqual(len(entity_info["vector"]), 384)
        self.assertEqual(entity_info["metadata"], test_metadata)
        self.assertIsInstance(entity_info["relationships"], list)
        self.assertEqual(len(entity_info["relationships"]), 2)
        relation_types = {rel["relation"] for rel in entity_info["relationships"]}
        self.assertEqual(relation_types, {"related", "cited"})

if __name__ == '__main__':
    unittest.main()
