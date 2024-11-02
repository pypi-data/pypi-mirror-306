from vectrs.swarms.knowledge_base.vector_db import VectorDB as SwarmVectorDB
from vectrs.database.vectrbase import VectorDB as VectrBaseDB
from vectrs.swarms.types import Agent, Result
from vectrs.swarms.llm.llm_interface import LLMInterface
from typing import Set, List, Dict, Any, Union, Callable
import asyncio
import logging
from pydantic import BaseModel, Field, ConfigDict
from abc import ABC, abstractmethod

class BaseAgent(Agent, ABC, BaseModel):
    agent_id: str
    coordinator: Any
    vector_db: Union[SwarmVectorDB, VectrBaseDB]
    llm: LLMInterface
    skills: Set[str]
    model: str
    instructions: Union[str, Callable[[], str]]
    logger: logging.Logger = Field(default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Result:
        self.logger.debug(f"Agent {self.agent_id} processing task: {task}")
        pass

    async def send_message(self, recipient: str, message_type: str, content: Any):
        self.logger.debug(f"Agent {self.agent_id} sending message to {recipient}: {message_type}")
        await self.coordinator.send_message(self.agent_id, recipient, message_type, content)

    async def receive_message(self, message: Dict[str, Any]):
        print(f"Agent {self.agent_id} received message: {message}")

    async def query_database(self, query_vector: List[float], k: int = 1) -> List[Dict[str, Any]]:
        self.logger.debug(f"Agent {self.agent_id} querying database")
        return await self.vector_db.search(query_vector, k)

    async def update_database(self, id: str, new_vector: List[float], new_data: Dict[str, Any]) -> bool:
        return await self.vector_db.update_item(id, new_vector, new_data)

    async def add_to_database(self, vector: List[float], data: Dict[str, Any]) -> str:
        self.logger.debug(f"Agent {self.agent_id} adding to database: {data}")
        return await self.vector_db.add_item(vector, data)

    async def get_all_knowledge(self) -> List[Dict[str, Any]]:
        return await self.vector_db.get_all_items()

    async def clear_knowledge(self) -> bool:
        return await self.vector_db.clear()

    def get_instructions(self) -> str:
        if callable(self.instructions):
            return self.instructions()
        return self.instructions
