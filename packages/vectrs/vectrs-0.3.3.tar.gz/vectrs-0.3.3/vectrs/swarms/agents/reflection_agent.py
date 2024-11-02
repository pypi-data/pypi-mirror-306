from .base_agent import BaseAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Dict, Any, Set, Union, Callable
from vectrs.swarms.types import Result

class ReflectionAgent(BaseAgent):
    def __init__(self, agent_id: str, coordinator: Any, vector_db: VectorDB, llm: LLMInterface, skills: Set[str], model: str, instructions: Union[str, Callable[[], str]]):
        super().__init__(agent_id=agent_id, coordinator=coordinator, vector_db=vector_db, llm=llm, skills=skills, model=model, instructions=instructions)
        self.skills = {"self-evaluation"}

    async def process_task(self, task: Dict[str, Any]) -> Result:
        self.logger.info(f"ReflectionAgent processing task: {task}")
        reflection_prompt = f"Reflect on this task and provide insights: {task['data']}. Your response should start with 'Reflection:' and include your thoughts on the task."
        reflection = await self.llm.generate_text(reflection_prompt)
        reflection_str = str(reflection)
        
        # Ensure the reflection starts with "Reflection:"
        if not reflection_str.lower().startswith("reflection:"):
            reflection_str = f"Reflection: {reflection_str}"
        
        embedding = await self.llm.embed_text(reflection_str)
        reflection_id = await self.add_to_database(embedding, {"reflection": reflection_str, "task": task})
        self.logger.info(f"ReflectionAgent generated reflection: {reflection_str}")
        return Result(value={"reflection_id": reflection_id, "reflection": reflection_str})

    async def analyze_performance(self, performance_data: Dict[str, Any]) -> Result:
        # Retrieve all previous reflections
        all_reflections = await self.get_all_knowledge()
        
        analysis_prompt = f"Analyze the following performance data and suggest improvements, considering these past reflections: {performance_data}\n\nPast reflections: {all_reflections}"
        analysis = await self.llm.generate_text(analysis_prompt)
        
        # Store analysis in VectorDB
        embedding = await self.llm.embed_text(analysis)
        analysis_id = await self.add_to_database(embedding, {"analysis": analysis, "performance_data": performance_data})
        
        return Result(value={"analysis_id": analysis_id, "analysis": analysis})

    async def clear_reflection_history(self) -> bool:
        return await self.clear_knowledge()
