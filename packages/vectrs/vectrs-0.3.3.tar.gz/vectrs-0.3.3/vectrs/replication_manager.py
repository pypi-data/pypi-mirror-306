import asyncio
from typing import List, Tuple, Dict, Any

class ReplicationManager:
    def __init__(self, node, replication_factor: int):
        self.node = node
        self.replication_factor = replication_factor

    async def replicate_vector(self, db_id: str, vector_id: str, vector: List[float], metadata: Dict[str, Any]):
        replica_nodes = await self.node.load_balancer.get_n_best_nodes(self.replication_factor)
        
        replication_tasks = []
        for node_address in replica_nodes:
            task = asyncio.create_task(self._replicate_to_node(node_address, db_id, vector_id, vector, metadata))
            replication_tasks.append(task)
        
        await asyncio.gather(*replication_tasks, return_exceptions=True)

    async def _replicate_to_node(self, node_address: Tuple[str, int], db_id: str, vector_id: str, vector: List[float], metadata: Dict[str, Any]):
        try:
            await self.node.remote_add_vector(node_address, db_id, vector_id, vector, metadata)
            self.node.logger.info(f"Replicated vector {vector_id} to node at {node_address[0]}:{node_address[1]}")
        except Exception as e:
            self.node.logger.error(f"Failed to replicate to {node_address}: {str(e)}")

    async def update_replicas(self, db_id: str, vector_id: str, vector: List[float], metadata: Dict[str, Any]):
        replica_nodes = await self._get_replica_nodes(db_id, vector_id)
        update_tasks = []
        for node_address in replica_nodes:
            task = asyncio.create_task(self._update_replica(node_address, db_id, vector_id, vector, metadata))
            update_tasks.append(task)
        
        await asyncio.gather(*update_tasks, return_exceptions=True)

    async def _get_replica_nodes(self, db_id: str, vector_id: str) -> List[Tuple[str, int]]:
        key = f"{db_id}:{vector_id}"
        return await self.node.get_replicas(key)

    async def _update_replica(self, node_address: Tuple[str, int], db_id: str, vector_id: str, vector: List[float], metadata: Dict[str, Any]):
        try:
            await self.node.remote_update_vector(node_address, db_id, vector_id, vector, metadata)
            self.node.logger.info(f"Updated vector {vector_id} replica on node at {node_address[0]}:{node_address[1]}")
        except Exception as e:
            self.node.logger.error(f"Failed to update replica on {node_address}: {str(e)}")

    async def ensure_replication_factor(self, db_id: str, vector_id: str):
        current_replicas = await self._get_replica_nodes(db_id, vector_id)
        if len(current_replicas) < self.replication_factor:
            additional_replicas_needed = self.replication_factor - len(current_replicas)
            new_replica_nodes = await self.node.load_balancer.get_n_best_nodes(additional_replicas_needed)
            vector, metadata = await self.node.get_vector(db_id, vector_id)
            
            replication_tasks = []
            for node_address in new_replica_nodes:
                task = asyncio.create_task(self._replicate_to_node(node_address, db_id, vector_id, vector, metadata))
                replication_tasks.append(task)
            
            await asyncio.gather(*replication_tasks, return_exceptions=True)

    async def handle_node_failure(self, failed_node: Tuple[str, int]):
        affected_vectors = await self.node.get_vectors_on_node(failed_node)
        for db_id, vector_id in affected_vectors:
            await self.ensure_replication_factor(db_id, vector_id)

    async def periodic_replication_check(self, interval: int = 3600):
        while True:
            all_vectors = await self.node.get_all_vectors()
            for db_id, vector_id in all_vectors:
                await self.ensure_replication_factor(db_id, vector_id)
            await asyncio.sleep(interval)
