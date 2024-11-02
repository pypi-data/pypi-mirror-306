from vectrs.database.vectrbase import VectorDBManager
from vectrs.network import KademliaNode
from typing import List, Dict, Any, Tuple, Optional
import logging
import asyncio
import numpy as np

class VectorDB:
    def __init__(self, vectr_base: VectorDBManager, node: KademliaNode):
        self.vectr_base = vectr_base
        self.node = node
        self.logger = logging.getLogger(__name__)

    async def add_item(self, vector: List[float], data: Dict[str, Any], entity_type: Optional[str] = None) -> str:
        self.logger.debug(f"Adding item to VectorDB: {data}")
        vector_id = self.vectr_base.add_vector(vector, data, entity_type=entity_type)
        await self.node.set_value(vector_id, (self.node.host, self.node.port))
        return vector_id

    async def search(self, query_vector: List[float], k: int = 1, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        local_results = self.vectr_base.search_vector(query_vector, k, entity_type=entity_type)
        network_results = await self.node.get_nearest_neighbors(query_vector, k)
        return self._merge_results(local_results, network_results)

    async def batch_add(self, vectors: List[List[float]], data_list: List[Dict[str, Any]], entity_types: Optional[List[str]] = None) -> List[str]:
        vector_ids = self.vectr_base.batch_add_vectors(vectors, data_list, entity_types=entity_types)
        for vector_id in vector_ids:
            await self.node.set_value(vector_id, (self.node.host, self.node.port))
        return vector_ids

    async def update_item(self, id: str, new_vector: List[float], new_data: Dict[str, Any]) -> bool:
        success = self.vectr_base.update_vector(id, new_vector, new_data)
        if success:
            await self.node.set_value(id, (self.node.host, self.node.port))
        return success

    async def delete_item(self, id: str) -> bool:
        success = self.vectr_base.delete_vector(id)
        if success:
            await self.node.delete_value(id)
        return success

    async def get_nearest_neighbors(self, query_vector: List[float], k: int = 5, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        local_results = self.vectr_base.get_nearest_neighbors(query_vector, k, entity_type=entity_type)
        network_results = await self.node.get_nearest_neighbors(query_vector, k)
        return self._merge_results(local_results, network_results)

    def get_stats(self) -> Dict[str, Any]:
        return self.vectr_base.get_stats()

    async def clear(self) -> bool:
        success = self.vectr_base.clear()
        if success:
            await self.node.clear_storage()
        return success

    async def get_item(self, id: str) -> Dict[str, Any]:
        local_result = self.vectr_base.get_vector(id)
        if local_result:
            return local_result
        return await self.node.get_value(id)

    async def get_all_items(self) -> List[Dict[str, Any]]:
        local_items = self.vectr_base.get_all_vectors()
        network_items = await self.node.get_all_values()
        return self._merge_results(local_items, network_items)

    def _merge_results(self, local_results: List[Dict[str, Any]], network_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        merged = local_results + network_results
        merged.sort(key=lambda x: x.get('distance', float('inf')))
        return [dict(t) for t in {tuple(d.items()) for d in merged}]

    async def add_relationship(self, source_id: str, target_id: str, relation_type: str, metadata: Dict[str, Any] = {}) -> bool:
        return self.vectr_base.add_relationship(source_id, target_id, relation_type, metadata)

    async def get_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        return self.vectr_base.get_relationships(entity_id)

    async def delete_relationship(self, source_id: str, target_id: str, relation_type: str) -> bool:
        return self.vectr_base.delete_relationship(source_id, target_id, relation_type)

    async def graphine_search(self, query_vector: List[float], entity_type: Optional[str] = None, relation_filter: Optional[Dict[str, str]] = None, k: int = 5, alpha: float = 0.5) -> List[Tuple[str, float, Dict[str, Any]]]:
        return self.vectr_base.graphine_search(query_vector, entity_type, relation_filter, k, alpha)

    async def expand_search(self, initial_results: List[Tuple[str, float, Dict[str, Any]]], max_depth: int = 2, expansion_factor: float = 0.5) -> List[Tuple[str, float, Dict[str, Any]]]:
        return self.vectr_base.expand_search(initial_results, max_depth, expansion_factor)

    async def filter_results(self, results: List[Tuple[str, float, Dict[str, Any]]], filter_criteria: Dict[str, Any]) -> List[Tuple[str, float, Dict[str, Any]]]:
        return self.vectr_base.filter_results(results, filter_criteria)

    async def get_entity_info(self, entity_id: str) -> Dict[str, Any]:
        return self.vectr_base.get_entity_info(entity_id)

    async def bulk_update(self, updates: List[Tuple[str, List[float], Dict[str, Any]]]) -> List[bool]:
        results = []
        for id, new_vector, new_data in updates:
            success = await self.update_item(id, new_vector, new_data)
            results.append(success)
        return results

    async def search_by_metadata(self, metadata_query: Dict[str, Any], k: int = 10) -> List[Dict[str, Any]]:
        local_results = self.vectr_base.search_by_metadata(metadata_query, k)
        # Implement network search if needed
        return local_results

    async def get_entity_types(self) -> List[str]:
        return self.vectr_base.get_entity_types()

    async def get_relation_types(self) -> List[str]:
        return self.vectr_base.get_relation_types()

    async def backup(self, backup_path: str) -> bool:
        return self.vectr_base.backup(backup_path)

    async def restore(self, backup_path: str) -> bool:
        success = self.vectr_base.restore(backup_path)
        if success:
            # Sync restored data with the network
            all_items = self.vectr_base.get_all_vectors()
            for item in all_items:
                await self.node.set_value(item['id'], (self.node.host, self.node.port))
        return success
