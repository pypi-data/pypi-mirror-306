import unittest
import asyncio
import numpy as np
import sys
import os
import json
from typing import List, Tuple, Dict, Any

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vectrs.network.node import KademliaNode
from vectrs.database.vectrbase import VectorDB, VectorDBManager, IndexType, SimilarityMetric
from vectrs.load_balancer import LoadBalancer
from vectrs.replication_manager import ReplicationManager

# Add these imports
import networkx as nx

class TestVectorDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.db_manager = VectorDBManager()

    def setUp(self):
        self.db_id = self.loop.run_until_complete(self.create_database())

    async def create_database(self):
        return self.db_manager.create_database(
            dim=3,
            space=SimilarityMetric.L2,
            max_elements=1000,
            index_type=IndexType.HNSW
        )

    async def add_vector(self, db_id: str, vector_id: str, vector: List[float], metadata: Dict[str, Any] = None):
        self.db_manager.add_vector(db_id, vector_id, vector, metadata)

    async def query_vector(self, db_id: str, vector_id: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        return self.db_manager.get_vector(db_id, vector_id)

    def test_create_database(self):
        db_id = self.loop.run_until_complete(self.create_database())
        self.assertIsNotNone(db_id)

    def test_add_vector(self):
        db_id = self.loop.run_until_complete(self.create_database())
        vector_id = "test_vector"
        vector = np.array([1.0, 2.0, 3.0])
        metadata = {"key": "value"}
        self.loop.run_until_complete(self.add_vector(db_id, vector_id, vector, metadata))
        
        # Verify the vector was added
        result = self.loop.run_until_complete(self.query_vector(db_id, vector_id))
        self.assertIsNotNone(result)
        np.testing.assert_array_almost_equal(result[0], vector)
        self.assertEqual(result[1], metadata)

    def test_query_vector(self):
        db_id = self.loop.run_until_complete(self.create_database())
        vector_id = "test_vector"
        vector = np.array([1.0, 2.0, 3.0])
        self.loop.run_until_complete(self.add_vector(db_id, vector_id, vector))
        
        query_vector = np.array([1.1, 2.1, 3.1])
        results = self.loop.run_until_complete(self.query_nearest(db_id, query_vector, k=1))
        self.assertEqual(len(results), 1)
        np.testing.assert_array_almost_equal(results[0][1], vector)

    def test_delete_vector(self):
        db_id = self.loop.run_until_complete(self.create_database())
        vector_id = "test_vector"
        vector = np.array([1.0, 2.0, 3.0])
        self.loop.run_until_complete(self.add_vector(db_id, vector_id, vector))
        
        self.loop.run_until_complete(self.delete_vector(db_id, vector_id))
        
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(self.query_vector(db_id, vector_id))

    def test_update_vector(self):
        db_id = self.loop.run_until_complete(self.create_database())
        vector_id = "test_vector"
        vector = np.array([1.0, 2.0, 3.0])
        self.loop.run_until_complete(self.add_vector(db_id, vector_id, vector))
        
        new_vector = np.array([4.0, 5.0, 6.0])
        self.loop.run_until_complete(self.update_vector(db_id, vector_id, new_vector))
        
        result = self.loop.run_until_complete(self.query_vector(db_id, vector_id))
        np.testing.assert_array_almost_equal(result[0], new_vector)

    def test_replication(self):
        source_db_id = self.loop.run_until_complete(self.create_database())
        target_db_id = self.loop.run_until_complete(self.create_database())
        vector_id = "test_vector"
        vector = np.array([1.0, 2.0, 3.0])
        self.loop.run_until_complete(self.add_vector(source_db_id, vector_id, vector))
        
        result = self.loop.run_until_complete(self.db_manager.replicate(source_db_id, target_db_id))
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "success")
        
        # Verify the vector was replicated
        replicated_vector = self.loop.run_until_complete(self.query_vector(target_db_id, vector_id))
        np.testing.assert_array_almost_equal(replicated_vector[0], vector)

    def test_add_relationship(self):
        vector_id1 = "test_vector1"
        vector_id2 = "test_vector2"
        vector1 = np.array([1.0, 2.0, 3.0])
        vector2 = np.array([4.0, 5.0, 6.0])
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id1, vector1))
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id2, vector2))
        
        self.db_manager.add_relationship(self.db_id, vector_id1, vector_id2, "related_to")
        
        relationships = self.db_manager.get_relationships(self.db_id, vector_id1)
        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0], (vector_id1, vector_id2, "related_to"))

    def test_delete_relationship(self):
        vector_id1 = "test_vector1"
        vector_id2 = "test_vector2"
        vector1 = np.array([1.0, 2.0, 3.0])
        vector2 = np.array([4.0, 5.0, 6.0])
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id1, vector1))
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id2, vector2))
        
        self.db_manager.add_relationship(self.db_id, vector_id1, vector_id2, "related_to")
        self.db_manager.delete_relationship(self.db_id, vector_id1, vector_id2, "related_to")
        
        relationships = self.db_manager.get_relationships(self.db_id, vector_id1)
        self.assertEqual(len(relationships), 0)

    def test_query_with_graph(self):
        vector_id1 = "test_vector1"
        vector_id2 = "test_vector2"
        vector_id3 = "test_vector3"
        vector1 = np.array([1.0, 2.0, 3.0])
        vector2 = np.array([4.0, 5.0, 6.0])
        vector3 = np.array([7.0, 8.0, 9.0])
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id1, vector1))
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id2, vector2))
        self.loop.run_until_complete(self.add_vector(self.db_id, vector_id3, vector3))
        
        self.db_manager.add_relationship(self.db_id, vector_id1, vector_id2, "related_to")
        self.db_manager.add_relationship(self.db_id, vector_id2, vector_id3, "related_to")
        
        query_vector = np.array([1.1, 2.1, 3.1])
        results = self.db_manager.query_with_graph(self.db_id, query_vector, k=3, max_depth=2)
        self.assertEqual(len(results), 3)
        result_ids = [r[0] for r in results]
        self.assertIn(vector_id1, result_ids)
        self.assertIn(vector_id2, result_ids)
        self.assertIn(vector_id3, result_ids)
        # Check if the closest vector is returned first
        self.assertEqual(results[0][0], vector_id1)

    def test_complex_graph_query(self):
        # Create a more complex graph structure
        vectors = [
            ("v1", np.array([1.0, 0.0, 0.0])),
            ("v2", np.array([0.0, 1.0, 0.0])),
            ("v3", np.array([0.0, 0.0, 1.0])),
            ("v4", np.array([1.0, 1.0, 0.0])),
            ("v5", np.array([1.0, 0.0, 1.0])),
        ]
        
        for vid, vec in vectors:
            self.loop.run_until_complete(self.add_vector(self.db_id, vid, vec))
        
        # Add relationships
        self.db_manager.add_relationship(self.db_id, "v1", "v2", "connected")
        self.db_manager.add_relationship(self.db_id, "v2", "v3", "connected")
        self.db_manager.add_relationship(self.db_id, "v3", "v4", "connected")
        self.db_manager.add_relationship(self.db_id, "v4", "v5", "connected")
        
        # Query with a vector close to v1
        query_vector = np.array([0.9, 0.1, 0.1])
        results = self.db_manager.query_with_graph(self.db_id, query_vector, k=5, max_depth=3)
        
        # Check if all vectors are in the result
        result_ids = [r[0] for r in results]
        for vid, _ in vectors:
            self.assertIn(vid, result_ids)
        
        # Check if the closest vector is returned first
        self.assertEqual(results[0][0], "v1")

    async def query_nearest(self, db_id: str, vector: List[float], k=10) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
        db = self.db_manager.get_database(db_id)
        results = db.knn_query(np.array(vector), k=k)
        return [(r[0], db.get(r[0])[0], r[2]) for r in results]

    async def delete_vector(self, db_id: str, vector_id: str) -> None:
        db = self.db_manager.get_database(db_id)
        db.delete(vector_id)

    async def update_vector(self, db_id: str, vector_id: str, new_vector: List[float], metadata: Dict[str, Any] = None) -> None:
        db = self.db_manager.get_database(db_id)
        db.update(vector_id, new_vector, metadata)

if __name__ == '__main__':
    unittest.main()
