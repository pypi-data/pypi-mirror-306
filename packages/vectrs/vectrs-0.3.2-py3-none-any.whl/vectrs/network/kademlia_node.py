import asyncio
from kademlia.network import Server
from typing import List, Dict, Any, Set
import numpy as np

class KademliaNode:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = Server()

    async def start(self):
        await self.server.listen(self.port, self.host)

    async def bootstrap(self, bootstrap_host: str, bootstrap_port: int):
        await self.server.bootstrap([(bootstrap_host, bootstrap_port)])

    async def set_value(self, key: str, value: Any):
        await self.server.set(key, value)

    async def get_value(self, key: str) -> Any:
        return await self.server.get(key)

    async def delete_value(self, key: str):
        await self.server.delete(key)

    async def get_nearest_neighbors(self, query_vector: List[float], k: int) -> List[Dict[str, Any]]:
        all_vectors = await self.get_all_values()
        distances = [np.linalg.norm(np.array(query_vector) - np.array(v['vector'])) for v in all_vectors]
        sorted_indices = np.argsort(distances)
        return [all_vectors[i] for i in sorted_indices[:k]]

    async def find_agents_with_skills(self, required_skills: Set[str]) -> List[Any]:
        all_agents = await self.get_all_values()
        return [agent for agent in all_agents if required_skills.issubset(set(agent.get('skills', [])))]

    async def clear_storage(self):
        for key in list(self.server.storage.keys()):
            await self.server.storage.__delitem__(key)

    async def get_all_values(self) -> List[Any]:
        return list(self.server.storage.values())

    async def stop(self):
        self.server.stop()