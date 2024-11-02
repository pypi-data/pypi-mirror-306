import sqlite3
import numpy as np
import hnswlib
import uuid
import hashlib
import shutil
import os
import time
import json
from typing import List, Dict, Any, Tuple, Optional
import networkx as nx
from enum import Enum

class VectrBase:
    def __init__(self):
        # Initialize your VectrBase here
        pass

    # Add other methods as needed

class IndexType(Enum):
    HNSW = "hnsw"
    IVF = "ivf"
    FLAT = "flat"

class SimilarityMetric(Enum):
    L2 = "l2"
    INNER_PRODUCT = "ip"
    COSINE = "cosine"

class VectorDB:
    def __init__(
        self,
        dim: int,
        space: SimilarityMetric,
        max_elements: int,
        ef_construction: int,
        M: int,
        db_id: str,
        connection: sqlite3.Connection,
        log_db_file: str,
        index_type: IndexType = IndexType.HNSW
    ):
        self.dim = dim
        self.space = space
        self.index_type = index_type
        self.db_id = db_id
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.log_connection = sqlite3.connect(log_db_file)
        self.log_cursor = self.log_connection.cursor()

        self._init_index(max_elements, ef_construction, M)
        self._init_database()
        self._init_graph_database()
        self._init_log_database()

        self.id_map = {}
        self.next_id = 0
        self.backup_interval = 300
        self.last_backup_time = time.time()
        self.index_backup_file = f"{db_id}_index.{index_type.value}"
        self.sqlite_backup_file = f"{db_id}_vectrs_dbs_log.sqlite"
        self.graph = nx.DiGraph()

    def _init_index(self, max_elements: int, ef_construction: int, M: int):
        if self.index_type == IndexType.HNSW:
            self.index = hnswlib.Index(space=self.space.value, dim=self.dim)
            self.index.init_index(max_elements=max_elements, ef_construction=ef_construction, M=M)
        elif self.index_type == IndexType.IVF:
            # Implement IVF index initialization
            pass
        elif self.index_type == IndexType.FLAT:
            self.index = []

    def _init_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                vector_id TEXT PRIMARY KEY,
                vector BLOB,
                metadata TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata_index (
                key TEXT,
                value TEXT,
                vector_id TEXT,
                FOREIGN KEY(vector_id) REFERENCES vectors(vector_id)
            )
        """)
        self.connection.commit()

    def _init_graph_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                source_id TEXT,
                target_id TEXT,
                relation_type TEXT,
                FOREIGN KEY(source_id) REFERENCES vectors(vector_id),
                FOREIGN KEY(target_id) REFERENCES vectors(vector_id),
                PRIMARY KEY(source_id, target_id, relation_type)
            )
        """)
        self.connection.commit()

    def _init_log_database(self):
        self.log_cursor.execute("""
            CREATE TABLE IF NOT EXISTS history_logs (
                log_id TEXT PRIMARY KEY,
                db_id TEXT,
                action TEXT,
                vector_id TEXT,
                details TEXT,
                timestamp TEXT
            )
        """)
        self.log_connection.commit()

    def add(self, vector: np.ndarray, id: str, metadata: Dict[str, Any] = None, entity_type: str = None):
        if id not in self.id_map:
            self.id_map[id] = self.next_id
            self.next_id += 1
        numerical_id = self.id_map[id]

        vector = np.array(vector, dtype=np.float32)  # Ensure the vector is a numpy array
        if vector.shape != (self.dim,):
            raise ValueError(f"Vector dimension mismatch. Expected {self.dim}, got {vector.shape[0]}")

        if self.index_type == IndexType.HNSW:
            self.index.add_items(vector.reshape(1, -1), np.array([numerical_id]))
        elif self.index_type == IndexType.FLAT:
            self.index.append((numerical_id, vector))

        self._add_to_database(id, vector, metadata)
        self.log_action("add", id, f"Added vector with ID {id}")
        self.check_and_backup()
        self.graph.add_node(id, entity_type=entity_type)

    def _add_to_database(self, id: str, vector: np.ndarray, metadata: Dict[str, Any]):
        self.cursor.execute(
            "INSERT OR REPLACE INTO vectors (vector_id, vector, metadata) VALUES (?, ?, ?)",
            (id, vector.tobytes(), json.dumps(metadata) if metadata else None)
        )
        if metadata:
            self._index_metadata(id, metadata)
        self.connection.commit()

    def _index_metadata(self, vector_id: str, metadata: Dict[str, Any]):
        for key, value in metadata.items():
            self.cursor.execute(
                "INSERT INTO metadata_index (key, value, vector_id) VALUES (?, ?, ?)",
                (key, str(value), vector_id)
            )

    def get(self, id: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        self.cursor.execute("SELECT vector, metadata FROM vectors WHERE vector_id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            vector_data, metadata_json = result
            vector = np.frombuffer(vector_data, dtype=np.float32)
            if vector.shape[0] != self.dim:
                print(f"Warning: Vector dimension mismatch. Expected {self.dim}, got {vector.shape[0]}")
            metadata = json.loads(metadata_json) if metadata_json else None
            return vector, metadata
        raise ValueError(f"Vector ID {id} not found")

    def query(self, vector: np.ndarray, k: int = 10, filter: Dict[str, Any] = None) -> List[Tuple[str, float, Dict[str, Any]]]:
        if self.index_type == IndexType.HNSW:
            labels, distances = self.index.knn_query(vector, k=k)
        elif self.index_type == IndexType.FLAT:
            distances = [np.linalg.norm(v - vector) for _, v in self.index]
            sorted_indices = np.argsort(distances)[:k]
            labels, distances = zip(*[(self.index[i][0], distances[i]) for i in sorted_indices])

        results = []
        for label, distance in zip(labels[0], distances[0]):
            vector_id = self._get_vector_id_from_numerical_id(label)
            vector, metadata = self.get(vector_id)
            if filter is None or self._apply_filter(metadata, filter):
                results.append((vector_id, distance, metadata))

        return results

    def _apply_filter(self, metadata: Dict[str, Any], filter: Dict[str, Any]) -> bool:
        for key, value in filter.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True

    def update(self, id: str, new_vector: np.ndarray, metadata: Dict[str, Any] = None):
        if id in self.id_map:
            numerical_id = self.id_map[id]
            new_vector = np.array(new_vector, dtype=np.float32)  # Ensure the vector is a numpy array
            if new_vector.shape != (self.dim,):
                raise ValueError(f"Vector dimension mismatch. Expected {self.dim}, got {new_vector.shape[0]}")

            if self.index_type == IndexType.HNSW:
                self.index.mark_deleted(numerical_id)
                self.index.add_items(new_vector.reshape(1, -1), np.array([numerical_id]))
            elif self.index_type == IndexType.FLAT:
                for i, (idx, _) in enumerate(self.index):
                    if idx == numerical_id:
                        self.index[i] = (numerical_id, new_vector)
                        break

            self._update_database(id, new_vector, metadata)
            self.log_action("update", id, f"Updated vector for ID {id}")
            self.check_and_backup()
        else:
            raise ValueError("Error: ID not found for update")

    def _update_database(self, id: str, new_vector: np.ndarray, metadata: Dict[str, Any]):
        self.cursor.execute(
            "UPDATE vectors SET vector = ?, metadata = ? WHERE vector_id = ?",
            (new_vector.tobytes(), json.dumps(metadata), id)
        )
        self.cursor.execute("DELETE FROM metadata_index WHERE vector_id = ?", (id,))
        if metadata:
            self._index_metadata(id, metadata)
        self.connection.commit()

    def delete(self, id: str):
        if id in self.id_map:
            numerical_id = self.id_map[id]
            if self.index_type == IndexType.HNSW:
                self.index.mark_deleted(numerical_id)
            elif self.index_type == IndexType.FLAT:
                self.index = [item for item in self.index if item[0] != numerical_id]

            del self.id_map[id]
            self._delete_from_database(id)
            self.log_action("delete", id, f"Deleted vector with ID {id}")
            self.check_and_backup()
        else:
            raise ValueError("Error: ID not found for deletion")

    def _delete_from_database(self, id: str):
        self.cursor.execute("DELETE FROM vectors WHERE vector_id = ?", (id,))
        self.cursor.execute("DELETE FROM metadata_index WHERE vector_id = ?", (id,))
        self.connection.commit()

    def batch_add(self, vectors: List[np.ndarray], ids: List[str], metadata_list: List[Dict[str, Any]] = None):
        if metadata_list is None:
            metadata_list = [None] * len(vectors)
        for vector, id, metadata in zip(vectors, ids, metadata_list):
            self.add(vector, id, metadata)

    def batch_update(self, vectors: List[np.ndarray], ids: List[str], metadata_list: List[Dict[str, Any]] = None):
        if metadata_list is None:
            metadata_list = [None] * len(vectors)
        for vector, id, metadata in zip(vectors, ids, metadata_list):
            self.update(id, vector, metadata)

    def batch_delete(self, ids: List[str]):
        for id in ids:
            self.delete(id)

    def _get_vector_id_from_numerical_id(self, numerical_id: int) -> str:
        for vector_id, num_id in self.id_map.items():
            if num_id == numerical_id:
                return vector_id
        raise ValueError(f"Numerical ID {numerical_id} not found")

    def check_and_backup(self):
        if time.time() - self.last_backup_time >= self.backup_interval:
            self.backup_index()
            self.backup_sqlite_db()
            self.last_backup_time = time.time()

    def backup_index(self):
        self.index.save_index(self.index_backup_file)
        print(f"Index backed up to {self.index_backup_file}")

    def backup_sqlite_db(self):
        db_path = self.connection.execute("PRAGMA database_list;").fetchone()[2]
        backup_path = self.sqlite_backup_file
        shutil.copyfile(db_path, backup_path)
        print(f"SQLite database backed up to {backup_path}")

    def log_action(self, action, vector_id, details):
        log_id = str(uuid.uuid4())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.log_cursor.execute(
            "INSERT INTO history_logs (log_id, db_id, action, vector_id, details, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (log_id, self.db_id, action, vector_id, details, timestamp),
        )
        self.log_connection.commit()
        return log_id

    def set_ef(self, ef):
        """Sets the 'ef' parameter for the index, which controls the size of the dynamic candidate list during the query."""
        self.index.set_ef(ef)
        self.index_set_ef_before_query = True

    def get_logs(self):
        """Fetches and returns all history logs from the database."""
        self.log_cursor.execute(
            "SELECT log_id, action, vector_id, details, timestamp FROM history_logs WHERE db_id = ?",
            (self.db_id,),
        )
        logs = self.log_cursor.fetchall()
        return logs

    def get_logs_by_hash(self, hash_id):
        """Fetches and returns history logs for a specific hash ID."""
        self.log_cursor.execute(
            "SELECT log_id, action, vector_id, details, timestamp FROM history_logs WHERE db_id = ? AND vector_id = ?",
            (self.db_id, hash_id),
        )
        logs = self.log_cursor.fetchall()
        return logs

    def knn_query(self, vector: np.ndarray, k: int = 10) -> List[Tuple[str, float, Dict[str, Any]]]:
        vector = np.array(vector, dtype=np.float32)  # Ensure the vector is a numpy array
        if vector.shape != (self.dim,):
            raise ValueError(f"Query vector dimension mismatch. Expected {self.dim}, got {vector.shape[0]}")

        if self.index_type == IndexType.HNSW:
            labels, distances = self.index.knn_query(vector.reshape(1, -1), k=k)
        elif self.index_type == IndexType.FLAT:
            distances = [np.linalg.norm(v - vector) for _, v in self.index]
            sorted_indices = np.argsort(distances)[:k]
            labels, distances = zip(*[(self.index[i][0], distances[i]) for i in sorted_indices])

        results = []
        for label, distance in zip(labels[0], distances[0]):
            vector_id = self._get_vector_id_from_numerical_id(label)
            vector, metadata = self.get(vector_id)
            results.append((vector_id, distance, metadata))

        return results

    def add_metadata(self, vector_id, metadata):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO vector_metadata (vector_id, metadata)
            VALUES (?, ?)
        """,
            (vector_id, metadata),
        )
        self.connection.commit()

    def get_metadata(self, vector_id):
        self.cursor.execute(
            """
            SELECT metadata FROM vector_metadata WHERE vector_id = ?
        """,
            (vector_id,),
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_metadata(self, vector_id):
        self.cursor.execute(
            """
            DELETE FROM vector_metadata WHERE vector_id = ?
        """,
            (vector_id,),
        )
        self.connection.commit()

    def update_metadata(self, vector_id, metadata):
        self.add_metadata(vector_id, metadata)

    async def replicate(self, source_db_id: str, target_db_id: str) -> Dict[str, Any]:
        source_db = self.get_database(source_db_id)
        target_db = self.get_database(target_db_id)

        for vector_id in source_db.id_map.keys():
            vector, metadata = source_db.get(vector_id)
            target_db.add(vector, vector_id, metadata)

        return {"status": "success", "message": f"Replicated {source_db_id} to {target_db_id}"}

    def add_relationship(self, source_id: str, target_id: str, relation_type: str):
        self.cursor.execute(
            "INSERT OR REPLACE INTO relationships (source_id, target_id, relation_type) VALUES (?, ?, ?)",
            (source_id, target_id, relation_type)
        )
        self.connection.commit()
        self.graph.add_edge(source_id, target_id, relation=relation_type)

    def get_relationships(self, vector_id: str) -> List[Tuple[str, str, str]]:
        self.cursor.execute(
            "SELECT source_id, target_id, relation_type FROM relationships WHERE source_id = ? OR target_id = ?",
            (vector_id, vector_id)
        )
        return self.cursor.fetchall()

    def delete_relationship(self, source_id: str, target_id: str, relation_type: str):
        self.cursor.execute(
            "DELETE FROM relationships WHERE source_id = ? AND target_id = ? AND relation_type = ?",
            (source_id, target_id, relation_type)
        )
        self.connection.commit()
        self.graph.remove_edge(source_id, target_id)

    def query_with_graph(self, vector: np.ndarray, k: int = 10, max_depth: int = 2) -> List[Tuple[str, float, Dict[str, Any]]]:
        initial_results = self.knn_query(vector, k)
        expanded_results = set(r[0] for r in initial_results)
        
        for depth in range(max_depth):
            new_nodes = set()
            for node in expanded_results:
                neighbors = list(self.graph.neighbors(node))
                new_nodes.update(neighbors)
            expanded_results.update(new_nodes)
        
        final_results = []
        for vector_id in expanded_results:
            vector_data, metadata = self.get(vector_id)
            distance = np.linalg.norm(vector_data - vector)
            final_results.append((vector_id, distance, metadata))
        
        return sorted(final_results, key=lambda x: x[1])[:k]

    def search_vectors(self, query_vector, top_k=10):
        # Implementation of vector similarity search
        pass

    def _compute_graph_score(self, entity_id: str, relation_filter: Dict[str, str] = None) -> float:
        if not relation_filter:
            return 1.0
        
        matching_relations = sum(
            1 for neighbor in self.graph.neighbors(entity_id)
            if self.graph[entity_id][neighbor]['relation'] in relation_filter.values()
        )
        return matching_relations / len(relation_filter)

    def expand_search(self, initial_results: List[Tuple[str, float, Dict[str, Any]]], max_depth: int = 2, expansion_factor: float = 0.5) -> List[Tuple[str, float, Dict[str, Any]]]:
        if not initial_results:
            return []

        expanded_results = set(r[0] for r in initial_results)
        all_results = list(initial_results)
        
        for depth in range(1, max_depth + 1):
            new_entities = set()
            for entity_id in expanded_results:
                neighbors = list(self.graph.neighbors(entity_id))
                new_entities.update(neighbors)
            
            new_entities -= expanded_results
            expanded_results.update(new_entities)
            
            for new_entity in new_entities:
                vector, metadata = self.get(new_entity)
                score = max((r[1] for r in initial_results if r[0] == entity_id), default=1.0) * (expansion_factor ** depth)
                all_results.append((new_entity, score, metadata))
        
        return sorted(all_results, key=lambda x: x[1], reverse=True)

    def filter_results(self, results: List[Tuple[str, float, Dict[str, Any]]], filters: Dict[str, Any]) -> List[Tuple[str, float, Dict[str, Any]]]:
        return [result for result in results if all(result[2].get(k) == v for k, v in filters.items())]

    def get_entity_info(self, entity_id: str) -> Dict[str, Any]:
        node_data = self.graph.nodes[entity_id]
        vector, metadata = self.get(entity_id)
        relationships = list(self.graph.edges(entity_id, data=True))
        
        return {
            "entity_id": entity_id,
            "entity_type": node_data.get('entity_type'),
            "vector": vector.tolist(),
            "metadata": metadata,
            "relationships": [
                {"target": target, "relation": data['relation']}
                for _, target, data in relationships
            ]
        }

    def graphine_search(self, query_vector: np.ndarray, entity_type: str = None, relation_filter: Dict[str, str] = None, k: int = 10, alpha: float = 0.5) -> List[Tuple[str, float, Dict[str, Any]]]:
        vector_results = self.knn_query(query_vector, k=k*2)  # Increase initial results to ensure we have enough after filtering
        
        filtered_results = []
        for entity_id, distance, metadata in vector_results:
            if entity_type and self.graph.nodes[entity_id].get('entity_type') != entity_type:
                continue
            
            if relation_filter:
                relations_match = all(
                    any(self.graph[entity_id][neighbor]['relation'] == rel_type
                        for neighbor in self.graph.neighbors(entity_id))
                    for rel_type in relation_filter.values()
                )
                if not relations_match:
                    continue
            
            graph_score = self._compute_graph_score(entity_id, relation_filter)
            combined_score = alpha * (1 - distance) + (1 - alpha) * graph_score
            filtered_results.append((entity_id, combined_score, metadata))
        
        return sorted(filtered_results, key=lambda x: x[1], reverse=True)[:k]

def generate_hash_id(input_id):
    pass  # or add function body here

class VectorDBManager:
    def __init__(self, db_directory="vector_dbs", log_db_file="logs_db.sqlite"):
        self.db_directory = db_directory
        self.log_db_file = log_db_file
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
        self.connection = sqlite3.connect(self.log_db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vector_databases (
                db_id TEXT PRIMARY KEY,
                dim INTEGER,
                space TEXT,
                max_elements INTEGER,
                ef_construction INTEGER,
                M INTEGER,
                index_type TEXT
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history_logs (
                log_id TEXT PRIMARY KEY,
                db_id TEXT,
                action TEXT,
                vector_id TEXT,
                details TEXT,
                timestamp TEXT,
                FOREIGN KEY(db_id) REFERENCES vector_databases(db_id)
            )
        """
        )
        self.connection.commit()
        self.databases = {}

    def _get_db_path(self, db_id):
        return os.path.join(self.db_directory, f"{db_id}.sqlite")

    def create_database(
        self, 
        dim, 
        space=SimilarityMetric.L2, 
        max_elements=10000, 
        ef_construction=200, 
        M=16,
        index_type=IndexType.HNSW
    ):
        db_id = str(uuid.uuid4())
        db_path = self._get_db_path(db_id)
        connection = sqlite3.connect(db_path)
        new_db = VectorDB(
            dim,
            space,
            max_elements,
            ef_construction,
            M,
            db_id,
            connection,
            self.log_db_file,
            index_type
        )
        self.databases[db_id] = new_db
        self.cursor.execute(
            "INSERT INTO vector_databases (db_id, dim, space, max_elements, ef_construction, M, index_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (db_id, dim, space.value, max_elements, ef_construction, M, index_type.value),
        )
        self.connection.commit()
        return db_id

    def get_database(self, db_id):
        if db_id in self.databases:
            return self.databases[db_id]
        else:
            db_path = self._get_db_path(db_id)
            connection = sqlite3.connect(db_path)
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT dim, space, max_elements, ef_construction, M, index_type FROM vector_databases WHERE db_id = ?",
                (db_id,),
            )
            row = cursor.fetchone()
            if row:
                dim, space, max_elements, ef_construction, M, index_type = row
                new_db = VectorDB(
                    dim,
                    SimilarityMetric(space),
                    max_elements,
                    ef_construction,
                    M,
                    db_id,
                    connection,
                    self.log_db_file,
                    IndexType(index_type)
                )
                self.databases[db_id] = new_db
                return new_db
            else:
                raise ValueError("Database ID not found")

    def add_vector(self, db_id, vector_id, vector, metadata=None):
        db = self.get_database(db_id)
        db.add(vector, vector_id, metadata)
        print(f"Added vector with ID: {vector_id}, in database ID: {db_id}")

    def get_vector(self, db_id, vector_id):
        db = self.get_database(db_id)
        return db.get(vector_id)

    def get_log(self, db_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT log_id, action, vector_id, details, timestamp FROM history_logs WHERE db_id = ?",
            (db_id,),
        )
        logs = cursor.fetchall()
        return logs

    def print_database_ids(self):
        for db_id in self.databases:
            print(f"Database ID: {db_id}")

    def list_vectors(self, db_id):
        db = self.get_database(db_id)
        vectors = []
        for vector_id, numerical_id in db.id_map.items():
            vector = db.index.get_items([numerical_id])[0]
            vectors.append((vector_id, vector))
        return vectors

    async def replicate(self, source_db_id: str, target_db_id: str) -> Dict[str, Any]:
        source_db = self.get_database(source_db_id)
        target_db = self.get_database(target_db_id)

        if source_db.dim != target_db.dim:
            raise ValueError(f"Dimension mismatch between source ({source_db.dim}) and target ({target_db.dim}) databases")

        for vector_id in source_db.id_map.keys():
            try:
                vector, metadata = source_db.get(vector_id)
                target_db.add(vector, vector_id, metadata)
            except ValueError as e:
                print(f"Error replicating vector {vector_id}: {str(e)}")

        return {"status": "success", "message": f"Replicated {source_db_id} to {target_db_id}"}

    def add_relationship(self, db_id: str, source_id: str, target_id: str, relation_type: str):
        db = self.get_database(db_id)
        db.add_relationship(source_id, target_id, relation_type)

    def get_relationships(self, db_id: str, vector_id: str) -> List[Tuple[str, str, str]]:
        db = self.get_database(db_id)
        return db.get_relationships(vector_id)

    def delete_relationship(self, db_id: str, source_id: str, target_id: str, relation_type: str):
        db = self.get_database(db_id)
        db.delete_relationship(source_id, target_id, relation_type)

    def query_with_graph(self, db_id: str, vector: np.ndarray, k: int = 10, max_depth: int = 2) -> List[Tuple[str, float, Dict[str, Any]]]:
        db = self.get_database(db_id)
        return db.query_with_graph(vector, k, max_depth)