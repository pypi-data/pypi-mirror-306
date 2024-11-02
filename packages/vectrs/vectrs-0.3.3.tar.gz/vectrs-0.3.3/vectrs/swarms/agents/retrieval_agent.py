from .base_agent import BaseAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Dict, Any, Set, Union, Callable
from vectrs.swarms.types import Result

class RetrievalAgent(BaseAgent):
    def __init__(self, agent_id: str, coordinator: Any, vector_db: VectorDB, llm: LLMInterface, skills: Set[str], model: str, instructions: Union[str, Callable[[], str]]):
        super().__init__(agent_id=agent_id, coordinator=coordinator, vector_db=vector_db, llm=llm, skills=skills, model=model, instructions=instructions)
        self.skills = {"information_retrieval"}

    async def process_task(self, task: Dict[str, Any]) -> Result:
        self.logger.info(f"RetrievalAgent processing task: {task}")
        query = task['data']
        embedding = await self.llm.embed_text(query)
        results = await self.query_database(embedding)
        
        if results:
            retrieved_info = results[0]['data']['content']  # Assuming the first result is the most relevant
        else:
            retrieved_info = "No relevant information found."
        
        self.logger.info(f"RetrievalAgent retrieved information: {retrieved_info}")
        return Result(value=retrieved_info)  # Return the string directly, not wrapped in a dictionary

# ... rest of the file remains the same
