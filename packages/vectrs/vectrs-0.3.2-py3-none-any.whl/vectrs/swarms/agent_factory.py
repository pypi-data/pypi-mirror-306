from typing import Dict, Any
from vectrs.swarms.agents.reflection_agent import ReflectionAgent
from vectrs.swarms.agents.tool_agent import ToolAgent
from vectrs.swarms.agents.planning_agent import PlanningAgent
from vectrs.swarms.agents.retrieval_agent import RetrievalAgent
from vectrs.swarms.agents.generation_agent import GenerationAgent
from vectrs.swarms.knowledge_base.vector_db import VectorDB
from vectrs.swarms.llm.llm_interface import LLMInterface

class AgentFactory:
    def __init__(self, coordinator: Any, vector_db: VectorDB, llm: LLMInterface):
        self.coordinator = coordinator
        self.vector_db = vector_db
        self.llm = llm

    def create_agent(self, agent_type: str, agent_id: str, **kwargs) -> Any:
        common_args = {
            "agent_id": agent_id,
            "coordinator": self.coordinator,
            "vector_db": self.vector_db,
            "llm": self.llm,
            "skills": kwargs.get("skills", set()),
            "model": kwargs.get("model", "claude-2.1"),
            "instructions": kwargs.get("instructions", "Default instructions")
        }

        if agent_type == "reflection":
            return ReflectionAgent(**common_args)
        elif agent_type == "tool":
            return ToolAgent(**common_args)
        elif agent_type == "planning":
            return PlanningAgent(**common_args)
        elif agent_type == "retrieval":
            return RetrievalAgent(**common_args)
        elif agent_type == "generation":
            return GenerationAgent(**common_args)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")


