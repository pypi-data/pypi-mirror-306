import asyncio
import logging
from kademlia.network import Server
from ..load_balancer import LoadBalancer
from ..replication_manager import ReplicationManager
from ..database import VectorDBManager
from ..database.vectrbase import IndexType, SimilarityMetric
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KademliaNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = Server()
        self.local_db_manager = None
        self.load_balancer = None
        self.replication_manager = None

    async def start(self):
        await self.server.listen(self.port)
        logger.info(f"Node started at {self.host}:{self.port}")
        asyncio.create_task(self.periodic_tasks())

    async def stop(self):
        self.server.stop()
        logger.info("Node has been stopped")

    async def bootstrap(self, bootstrap_host, bootstrap_port):
        await self.server.bootstrap([(bootstrap_host, bootstrap_port)])
        logger.info(f"Node bootstrapped to {bootstrap_host}:{bootstrap_port}")

    async def set_value(self, key, value):
        if isinstance(value, tuple):
            value = f"{value[0]}:{value[1]}"
        await self.server.set(key, value)
        logger.info(f"Set key {key} to value {value}")

    async def get_value(self, key):
        value = await self.server.get(key)
        if value and ":" in value:
            host, port = value.split(":")
            logger.info(f"Get key {key} returned value {value}")
            return host, int(port)
        logger.info(f"Get key {key} returned value {value}")
        return value

    async def query_vector(self, db_id, vector_id, k=10, filter=None):
        logger.info(f"Querying vector with db_id: {db_id}, vector_id: {vector_id}, k: {k}, filter: {filter}")

        try:
            # Check local storage first
            if self.local_db_manager:
                try:
                    db = self.local_db_manager.get_database(db_id)
                    vector, metadata = db.get(vector_id)
                    results = db.query(vector, k=k, filter=filter)
                    logger.info(f"Vector found locally: {vector}, Metadata: {metadata}")
                    return results
                except ValueError as e:
                    logger.warning(f"Vector not found locally: {e}")

            # If not found locally, query the DHT
            host_port = await self.get_value(db_id)
            if host_port:
                host, port = host_port
                logger.info(f"Host: {host}, Port: {port} for db_id: {db_id}")
                if (host, port) == (self.host, self.port):
                    logger.info(f"Vector is local for db_id {db_id}")
                    return "Local"
                else:
                    logger.info(f"Vector should be remote for db_id {db_id}, at {host}:{port}")
                    remote_node = KademliaNode(host, port)
                    await remote_node.start()
                    try:
                        results = await remote_node.query_vector(db_id, vector_id, k, filter)
                        if results is None:
                            logger.warning(f"Remote node returned None for vector_id: {vector_id}")
                        return results
                    finally:
                        await remote_node.stop()
            else:
                logger.warning(f"Host and port not found for db_id {db_id}")
        except Exception as e:
            logger.error(f"Error querying vector: {str(e)}", exc_info=True)
        
        return None

    def set_local_db_manager(self, db_manager):
        self.local_db_manager = db_manager

    def set_load_balancer(self, load_balancer):
        self.load_balancer = load_balancer

    def set_replication_manager(self, replication_manager):
        self.replication_manager = replication_manager

    async def add_vector(self, db_id, vector_id, vector, metadata=None):
        logger.info(f"Adding vector with db_id: {db_id}, vector_id: {vector_id}")
        
        # Add vector to local database
        if self.local_db_manager:
            db = self.local_db_manager.get_database(db_id)
            db.add(vector, vector_id, metadata)
            logger.info(f"Vector added locally: {vector_id}")
        
        # Propagate vector information to the DHT
        await self.set_value(db_id, (self.host, self.port))
        logger.info(f"Vector metadata added to DHT: {vector_id}")

        # Replicate the vector
        if self.replication_manager:
            await self.replication_manager.replicate_vector(db_id, vector_id, vector, metadata)

    async def update_vector(self, db_id, vector_id, vector, metadata=None):
        logger.info(f"Updating vector with db_id: {db_id}, vector_id: {vector_id}")
        
        # Update vector in local database
        if self.local_db_manager:
            db = self.local_db_manager.get_database(db_id)
            db.update(vector_id, vector, metadata)
            logger.info(f"Vector updated locally: {vector_id}")
        
        # Update vector information in the DHT
        await self.set_value(db_id, (self.host, self.port))
        logger.info(f"Vector metadata updated in DHT: {vector_id}")

        # Update replicas
        if self.replication_manager:
            await self.replication_manager.update_replicas(db_id, vector_id, vector, metadata)

    async def delete_vector(self, db_id, vector_id):
        logger.info(f"Deleting vector with db_id: {db_id}, vector_id: {vector_id}")
        
        # Delete vector from local database
        if self.local_db_manager:
            db = self.local_db_manager.get_database(db_id)
            db.delete(vector_id)
            logger.info(f"Vector deleted locally: {vector_id}")
        
        # Update DHT to reflect deletion
        await self.set_value(db_id, (self.host, self.port))
        logger.info(f"Vector metadata deleted from DHT: {vector_id}")

        # Delete replicas
        if self.replication_manager:
            await self.replication_manager.delete_replicas(db_id, vector_id)

    async def get_bootstrap_nodes(self):
        # In a real implementation, this would query the DHT for known nodes
        # For now, we'll return a hardcoded list of bootstrap nodes
        return [("localhost", 8468), ("localhost", 8469)]

    async def periodic_tasks(self):
        while True:
            await asyncio.sleep(300)  # Run every 5 minutes
            if self.load_balancer:
                await self.load_balancer.update_known_nodes()
            if self.replication_manager:
                # Ensure replication factor for all vectors
                for db_id in self.local_db_manager.databases:
                    db = self.local_db_manager.get_database(db_id)
                    for vector_id in db.id_map:
                        await self.replication_manager.ensure_replication_factor(db_id, vector_id)

    async def remote_add_vector(self, db_id, vector_id, vector, metadata=None):
        # This method would be called by other nodes to add a vector to this node
        await self.add_vector(db_id, vector_id, vector, metadata)

    async def remote_update_vector(self, db_id, vector_id, vector, metadata=None):
        # This method would be called by other nodes to update a vector on this node
        await self.update_vector(db_id, vector_id, vector, metadata)

    async def remote_delete_vector(self, db_id, vector_id):
        # This method would be called by other nodes to delete a vector from this node
        await self.delete_vector(db_id, vector_id)

    async def get_node_stats(self):
        # In a real implementation, this would return actual node statistics
        # For now, we'll return dummy values
        return {
            'cpu_usage': 50,
            'memory_usage': 60,
            'storage_usage': 40,
            'network_latency': 10
        }