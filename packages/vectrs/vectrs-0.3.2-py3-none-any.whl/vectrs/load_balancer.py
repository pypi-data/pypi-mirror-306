import asyncio
from typing import List, Tuple
import random

class LoadBalancer:
    def __init__(self, node):
        self.node = node
        self.known_nodes = set()

    async def update_known_nodes(self):
        self.known_nodes = set(await self.node.get_peers())

    async def get_node_stats(self, node_address: Tuple[str, int]) -> dict:
        try:
            return await self.node.get_remote_stats(node_address)
        except Exception as e:
            self.node.logger.error(f"Failed to get stats from node {node_address}: {str(e)}")
            return None

    def calculate_node_score(self, stats: dict) -> float:
        if not stats:
            return float('inf')
        return (
            0.3 * stats.get('cpu_usage', 100) +
            0.2 * stats.get('memory_usage', 100) +
            0.3 * stats.get('storage_usage', 100) +
            0.2 * stats.get('network_latency', 1000)
        )

    async def get_best_node_for_storage(self) -> Tuple[str, int]:
        await self.update_known_nodes()
        if not self.known_nodes:
            return self.node.host, self.node.port

        node_scores = []
        for node in self.known_nodes:
            stats = await self.get_node_stats(node)
            score = self.calculate_node_score(stats)
            node_scores.append((node, score))

        return min(node_scores, key=lambda x: x[1])[0]

    async def get_best_node_for_query(self) -> Tuple[str, int]:
        # For simplicity, we'll use the same logic as storage
        return await self.get_best_node_for_storage()

    async def get_n_best_nodes(self, n: int) -> List[Tuple[str, int]]:
        await self.update_known_nodes()
        if len(self.known_nodes) <= n:
            return list(self.known_nodes)

        node_scores = []
        for node in self.known_nodes:
            stats = await self.get_node_stats(node)
            score = self.calculate_node_score(stats)
            node_scores.append((node, score))

        return [node for node, _ in sorted(node_scores, key=lambda x: x[1])[:n]]
