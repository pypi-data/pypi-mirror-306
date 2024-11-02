import argparse
import asyncio
import numpy as np
import logging
import json
from network import KademliaNode
from database import VectorDBManager
from load_balancer import LoadBalancer
from replication_manager import ReplicationManager
from database.vectrbase import IndexType, SimilarityMetric, VectorDB, GraphineIndex
from swarms.main import Swarms
from swarms.knowledge_base.vector_db import VectorDB as SwarmVectorDB
from swarms.utils.task_analyzer import TaskAnalyzer
from networking.message_broker import MessageBroker
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="P2P Vector Database Node")
    parser.add_argument("mode", choices=[
        "start-node", "create-db", "add-vector", "query-vector", "view-log", "stop-node", "list-vectors",
        "run-rag", "analyze-task", "create-agent", "agent-status", "add-relationship", "get-relationships",
        "query-with-graph", "batch-add-vectors", "update-vector", "delete-vector", "graphine-search"
    ], help="Mode of operation.")
    parser.add_argument("--host", default="0.0.0.0", help="Host address for the node.")
    parser.add_argument("--port", type=int, default=8468, help="Port number for the node.")
    parser.add_argument("--bootstrap_host", default=None, help="Bootstrap node host address.")
    parser.add_argument("--bootstrap_port", type=int, default=8468, help="Bootstrap node port number.")
    parser.add_argument("--dim", type=int, help="Dimension of the vector space for the database.")
    parser.add_argument("--space", default="l2", choices=[m.value for m in SimilarityMetric], help="Metric space type.")
    parser.add_argument("--index_type", default="hnsw", choices=[t.value for t in IndexType], help="Index type.")
    parser.add_argument("--max_elements", type=int, default=10000, help="Maximum number of elements in the database.")
    parser.add_argument("--db_id", help="ID of the database.")
    parser.add_argument("--vector_id", help="ID of the vector.")
    parser.add_argument("--vector", help="Vector data as a comma-separated string.")
    parser.add_argument("--metadata", help="Metadata for the vector as a JSON string.")
    parser.add_argument("--replication_factor", type=int, default=3, help="Number of replicas for each vector.")
    parser.add_argument("--query_k", type=int, default=10, help="Number of nearest neighbors to return in a query.")
    parser.add_argument("--filter", help="Filter criteria as a JSON string.")
    parser.add_argument("--query", help="Query for RAG workflow")
    parser.add_argument("--task_type", help="Type of task for analysis")
    parser.add_argument("--task_data", help="Data for task analysis")
    parser.add_argument("--agent_type", help="Type of agent to create")
    parser.add_argument("--agent_id", help="ID for the agent")
    parser.add_argument("--agent_kwargs", type=dict, default={}, help="Additional kwargs for agent creation")
    parser.add_argument("--relationship_type", help="Type of relationship between vectors")
    parser.add_argument("--max_depth", type=int, default=1, help="Maximum depth for graph-based queries")
    parser.add_argument("--vectors", help="List of vectors for batch addition, as a JSON string")
    parser.add_argument("--data_list", help="List of metadata for batch addition, as a JSON string")
    parser.add_argument("--new_vector", help="New vector data for update, as a comma-separated string")
    parser.add_argument("--new_metadata", help="New metadata for update, as a JSON string")
    parser.add_argument("--graphine_k", type=int, default=10, help="Number of nearest neighbors to return in a Graphine query.")
    parser.add_argument("--graphine_ef", type=int, default=50, help="Size of the dynamic list for the Graphine search.")
    parser.add_argument("--anthropic_api_key", help="Anthropic API key for Claude")
    return parser.parse_args()

async def start_node(host, port, bootstrap_host, bootstrap_port, replication_factor, anthropic_api_key=None):
    try:
        node = KademliaNode(host=host, port=port)
        await node.start()
        if bootstrap_host:
            await node.bootstrap(bootstrap_host, bootstrap_port)
        
        load_balancer = LoadBalancer(node)
        replication_manager = ReplicationManager(node, replication_factor)
        message_broker = MessageBroker(node)
        
        node.set_load_balancer(load_balancer)
        node.set_replication_manager(replication_manager)
        node.set_message_broker(message_broker)
        
        # Initialize Swarm with API key
        db_manager = VectorDBManager()
        vector_db = SwarmVectorDB(db_manager, node)
        swarm = Swarms(
            db_manager, 
            host, 
            port, 
            bootstrap_host, 
            bootstrap_port,
            anthropic_api_key=anthropic_api_key
        )
        await swarm.initialize()
        
        logger.info(f"Node started successfully at {host}:{port}")
        return node, swarm
    except Exception as e:
        logger.error(f"Error starting node: {str(e)}", exc_info=True)
        raise

async def create_vector_database(host, port, dim, space, index_type, max_elements, bootstrap_host, bootstrap_port, replication_factor):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)
    
    load_balancer = LoadBalancer(node)
    replication_manager = ReplicationManager(node, replication_factor)
    
    node.set_load_balancer(load_balancer)
    node.set_replication_manager(replication_manager)
    
    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    db_id = db_manager.create_database(dim, SimilarityMetric(space), max_elements, index_type=IndexType(index_type))
    await node.set_value(db_id, (host, port))
    logger.info(f"Database created with ID: {db_id}")

    await node.stop()

async def add_vector(host, port, db_id, vector_id, vector, metadata, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    vector = np.array([float(x) for x in vector.split(',')], dtype=np.float32)
    
    logger.debug(f"Adding vector: ID={vector_id}, DB_ID={db_id}, Vector={vector}, Metadata={metadata}")
    
    # Use load balancer to determine the best node for storing the vector
    target_node = await node.load_balancer.get_best_node_for_storage()
    
    # Add vector to the target node
    await target_node.add_vector(db_id, vector_id, vector, metadata)
    
    # Replicate the vector
    await node.replication_manager.replicate_vector(db_id, vector_id, vector, metadata)
    
    logger.info(f"Vector added with ID: {vector_id}")

    await node.stop()

async def query_vector(host, port, db_id, vector_id, bootstrap_host, bootstrap_port, k, filter):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    logger.debug(f"Querying vector: ID={vector_id}, DB_ID={db_id}, K={k}, Filter={filter}")
    
    # Use load balancer to determine the best node for querying
    target_node = await node.load_balancer.get_best_node_for_query()
    
    logger.info(f"Querying vector with ID: {vector_id} in database: {db_id}")
    result = await target_node.query_vector(db_id, vector_id, k, filter)
    if result == "Local":
        vector, metadata = db_manager.get_vector(db_id, vector_id)
        logger.info(f"Retrieved Vector: {vector}, Metadata: {metadata}")
    elif result is None:
        logger.warning(f"Vector not found for ID: {vector_id}")
    else:
        logger.info(f"Retrieved Vector from remote node: {result}")

    await node.stop()

async def view_log(db_id):
    db_manager = VectorDBManager()
    log = db_manager.get_log(db_id)
    logger.info(f"Log for database {db_id}:")
    for entry in log:
        logger.info(entry)

async def stop_node(host, port):
    node = KademliaNode(host=host, port=port)
    await node.stop()
    logger.info("Node has been stopped")

async def list_vectors(host, port, db_id, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    logger.info(f"Listing all vectors in database: {db_id}")
    vectors = db_manager.list_vectors(db_id)
    for vector_id, vector in vectors:
        logger.info(f"Vector ID: {vector_id}, Vector: {vector}")

    await node.stop()

async def run_rag_workflow(swarm, query):
    result = await swarm.run_rag_workflow(query)
    logger.info(f"RAG Workflow Result: {result}")
    return result

async def analyze_task(swarm, task):
    task_analyzer = TaskAnalyzer()
    analysis = task_analyzer.analyze_task(task)
    logger.info(f"Task Analysis: {analysis}")
    return analysis

async def create_custom_agent(swarm, agent_type, agent_id, **kwargs):
    agent = await swarm.create_custom_agent(agent_type, agent_id, **kwargs)
    logger.info(f"Custom Agent Created: {agent}")
    return agent

async def get_agent_status(swarm, agent_id):
    status = await swarm.get_agent_status(agent_id)
    logger.info(f"Agent Status: {status}")
    return status

async def add_relationship(host, port, db_id, vector_id1, vector_id2, relationship_type, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    db_manager.add_relationship(db_id, vector_id1, vector_id2, relationship_type)
    logger.info(f"Added relationship: {vector_id1} -{relationship_type}-> {vector_id2}")

    await node.stop()

async def get_relationships(host, port, db_id, vector_id, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    relationships = db_manager.get_relationships(db_id, vector_id)
    logger.info(f"Relationships for vector {vector_id}: {relationships}")

    await node.stop()

async def query_with_graph(host, port, db_id, vector_id, k, max_depth, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    results = db_manager.query_with_graph(db_id, vector_id, k, max_depth)
    logger.info(f"Graph-based query results: {results}")

    await node.stop()

async def batch_add_vectors(host, port, db_id, vectors, data_list, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    vector_ids = db_manager.batch_add_vectors(db_id, vectors, data_list)
    logger.info(f"Batch added vectors with IDs: {vector_ids}")

    await node.stop()

async def update_vector(host, port, db_id, vector_id, new_vector, new_metadata, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    success = db_manager.update_vector(db_id, vector_id, new_vector, new_metadata)
    logger.info(f"Vector update {'successful' if success else 'failed'} for ID: {vector_id}")

    await node.stop()

async def delete_vector(host, port, db_id, vector_id, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    success = db_manager.delete_vector(db_id, vector_id)
    logger.info(f"Vector deletion {'successful' if success else 'failed'} for ID: {vector_id}")

    await node.stop()

async def graphine_search(host, port, db_id, vector_id, k, ef, bootstrap_host, bootstrap_port):
    node = KademliaNode(host=host, port=port)
    await node.start()
    if bootstrap_host:
        await node.bootstrap(bootstrap_host, bootstrap_port)

    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    vector_db = db_manager.get_database(db_id)
    if not isinstance(vector_db.index, GraphineIndex):
        logger.error(f"Database {db_id} does not use a Graphine index.")
        await node.stop()
        return

    query_vector = vector_db.get_vector(vector_id)
    results = vector_db.index.search(query_vector, k=k, ef=ef)
    logger.info(f"Graphine search results for vector {vector_id}: {results}")

    await node.stop()

async def main():
    args = parse_args()
    
    # Get API key from args or environment
    anthropic_api_key = args.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    
    node, swarm = await start_node(
        args.host, 
        args.port, 
        args.bootstrap_host, 
        args.bootstrap_port, 
        args.replication_factor,
        anthropic_api_key=anthropic_api_key
    )
    
    if args.mode == "start-node":
        await asyncio.Future()  # Keep the node running indefinitely
    elif args.mode == "create-db":
        await create_vector_database(args.host, args.port, args.dim, args.space, args.index_type, args.max_elements, args.bootstrap_host, args.bootstrap_port, args.replication_factor)
    elif args.mode == "add-vector":
        await add_vector(args.host, args.port, args.db_id, args.vector_id, args.vector, args.metadata, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "query-vector":
        await query_vector(args.host, args.port, args.db_id, args.vector_id, args.bootstrap_host, args.bootstrap_port, args.query_k, args.filter)
    elif args.mode == "view-log":
        await view_log(args.db_id)
    elif args.mode == "stop-node":
        await stop_node(args.host, args.port)
    elif args.mode == "list-vectors":
        await list_vectors(args.host, args.port, args.db_id, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "run-rag":
        await run_rag_workflow(swarm, args.query)
    elif args.mode == "analyze-task":
        await analyze_task(swarm, {"type": args.task_type, "data": args.task_data})
    elif args.mode == "create-agent":
        await create_custom_agent(swarm, args.agent_type, args.agent_id, **args.agent_kwargs)
    elif args.mode == "agent-status":
        await get_agent_status(swarm, args.agent_id)
    elif args.mode == "add-relationship":
        await add_relationship(args.host, args.port, args.db_id, args.vector_id, args.vector, args.relationship_type, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "get-relationships":
        await get_relationships(args.host, args.port, args.db_id, args.vector_id, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "query-with-graph":
        await query_with_graph(args.host, args.port, args.db_id, args.vector_id, args.query_k, args.max_depth, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "batch-add-vectors":
        vectors = json.loads(args.vectors)
        data_list = json.loads(args.data_list)
        await batch_add_vectors(args.host, args.port, args.db_id, vectors, data_list, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "update-vector":
        new_vector = np.array([float(x) for x in args.new_vector.split(',')], dtype=np.float32)
        new_metadata = json.loads(args.new_metadata)
        await update_vector(args.host, args.port, args.db_id, args.vector_id, new_vector, new_metadata, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "delete-vector":
        await delete_vector(args.host, args.port, args.db_id, args.vector_id, args.bootstrap_host, args.bootstrap_port)
    elif args.mode == "graphine-search":
        await graphine_search(args.host, args.port, args.db_id, args.vector_id, args.graphine_k, args.graphine_ef, args.bootstrap_host, args.bootstrap_port)

if __name__ == "__main__":
    asyncio.run(main())
