from .base_agent import BaseAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Dict, Any, Set, Union, Callable
from vectrs.swarms.types import Result

class GenerationAgent(BaseAgent):
    def __init__(self, agent_id: str, coordinator: Any, vector_db: VectorDB, llm: LLMInterface, skills: Set[str], model: str, instructions: Union[str, Callable[[], str]]):
        super().__init__(agent_id=agent_id, coordinator=coordinator, vector_db=vector_db, llm=llm, skills=skills, model=model, instructions=instructions)
        self.skills = {"text_generation"}

    async def process_task(self, task: Dict[str, Any]) -> Result:
        self.logger.info(f"GenerationAgent processing task: {task}")
        generation_prompt = f"Generate a response for the following task: {task['data']}"
        generated_text = await self.llm.generate_text(generation_prompt)
        
        self.logger.info(f"GenerationAgent generated text: {generated_text}")
        return Result(value={"generated_text": generated_text})
