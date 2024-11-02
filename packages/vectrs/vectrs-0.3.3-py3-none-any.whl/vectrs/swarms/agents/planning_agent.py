from .base_agent import BaseAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Dict, Any, Set, Union, Callable
from vectrs.swarms.types import Result

class PlanningAgent(BaseAgent):
    def __init__(self, agent_id: str, coordinator: Any, vector_db: VectorDB, llm: LLMInterface, skills: Set[str], model: str, instructions: Union[str, Callable[[], str]]):
        super().__init__(agent_id=agent_id, coordinator=coordinator, vector_db=vector_db, llm=llm, skills=skills, model=model, instructions=instructions)
        self.skills = {"task_planning", "strategy_formulation"}

    async def process_task(self, task: Dict[str, Any]) -> Result:
        planning_prompt = f"Create a detailed plan for the following task: {task['data']}"
        plan = await self.llm.generate_text(planning_prompt)
        plan_str = str(plan)
        
        # Store plan in VectorDB
        embedding = await self.llm.embed_text(plan_str)
        plan_id = await self.add_to_database(embedding, {"plan": plan_str, "task": task})
        
        return Result(value={"plan_id": plan_id, "plan": plan_str})

    async def formulate_strategy(self, goal: Dict[str, Any]) -> Result:
        strategy_prompt = f"Formulate a strategy to achieve the following goal: {goal}"
        strategy = await self.llm.generate_text(strategy_prompt)
        
        # Store strategy in VectorDB
        embedding = await self.llm.embed_text(strategy)
        strategy_id = await self.add_to_database(embedding, {"strategy": strategy, "goal": goal})
        
        return Result(value={"strategy_id": strategy_id, "strategy": strategy})
