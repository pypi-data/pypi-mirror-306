from .base_agent import BaseAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Dict, Any, Set, Union, Callable
from vectrs.swarms.types import Result

class ToolAgent(BaseAgent):
    def __init__(self, agent_id: str, coordinator: Any, vector_db: VectorDB, llm: LLMInterface, skills: Set[str], model: str, instructions: Union[str, Callable[[], str]]):
        super().__init__(agent_id=agent_id, coordinator=coordinator, vector_db=vector_db, llm=llm, skills=skills, model=model, instructions=instructions)
        self.skills = {"tool_usage", "task_execution"}

    async def process_task(self, task: Dict[str, Any]) -> Result:
        tool_prompt = f"Analyze the following task and suggest appropriate tools: {task['data']}"
        tool_suggestion = await self.llm.generate_text(tool_prompt)
        
        execution_prompt = f"Execute the task using the suggested tools: {tool_suggestion}"
        execution_result = await self.llm.generate_text(execution_prompt)
        execution_result_str = str(execution_result)
        
        # Store result in VectorDB
        embedding = await self.llm.embed_text(execution_result_str)
        result_id = await self.add_to_database(embedding, {"result": execution_result_str, "task": task})
        
        return Result(value={"result_id": result_id, "result": execution_result_str})
