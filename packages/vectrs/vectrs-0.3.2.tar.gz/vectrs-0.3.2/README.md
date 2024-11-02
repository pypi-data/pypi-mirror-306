# Vectrs - Decentralized & Distributed Vector Database   [![Downloads](https://static.pepy.tech/badge/vectrs)](https://pepy.tech/project/vectrs)

## Overview   
**Vectrs** is a decentralized & distributed vector database designed for efficient storage and retrieval of vector embeddings. It combines P2P networking with advanced vector operations, RAG capabilities, and graph-based relationships, making it ideal for AI-powered distributed applications.

## Features   
- **Distributed Architecture**
  - P2P network with load balancing
  - Data replication for fault tolerance
  - Horizontal scalability
  
- **Vector Operations**
  - Multiple similarity metrics (L2, cosine, etc.)
  - Different index types (HNSW, Graphine)
  - Batch vector operations
  - Vector metadata support
  
- **Graph Capabilities**
  - Vector relationships management
  - Graph-based queries
  - Customizable relationship types
  
- **AI Integration**
  - RAG (Retrieval-Augmented Generation) workflow
  - Custom agent creation and management
  - Task analysis capabilities

## Installation   
```bash
pip install vectrs
```

## Usage

### Basic Operations

1. **Initialize and Start a Node**
```python
import asyncio
from vectrs.network import KademliaNode
from vectrs.database import VectorDBManager

async def start_node():
    # Initialize node
    node = KademliaNode(host='127.0.0.1', port=8468)
    db_manager = VectorDBManager()
    node.set_local_db_manager(db_manager)
    
    # Start node
    await node.start()
    
    # Optional: Connect to existing network
    await node.bootstrap('bootstrap_host', 8468)
    return node

# Run the node
node = asyncio.run(start_node())
```

2. **Create Database**
```python
from vectrs.database.vectrbase import SimilarityMetric, IndexType

async def create_database(node):
    db_manager = VectorDBManager()
    # Create database with HNSW index
    db_id = db_manager.create_database(
        dim=384,  # Dimension of your vectors
        space=SimilarityMetric.COSINE,  # COSINE, L2, or other metrics
        max_elements=10000,
        index_type=IndexType.HNSW
    )
    return db_id

db_id = asyncio.run(create_database(node))
```

3. **Vector Operations**
```python
import numpy as np

async def vector_operations(node, db_id):
    # Add single vector
    vector = np.random.rand(384).astype(np.float32)
    metadata = {"description": "example vector"}
    await node.add_vector(db_id, "vector1", vector, metadata)

    # Query vector
    results = await node.query_vector(db_id, "vector1", k=10)
    
    # Batch add vectors
    vectors = {
        "vec1": np.random.rand(384).astype(np.float32),
        "vec2": np.random.rand(384).astype(np.float32)
    }
    metadata_list = [{"desc": "vec1"}, {"desc": "vec2"}]
    await node.batch_add_vectors(db_id, vectors, metadata_list)
    
    # Update vector
    new_vector = np.random.rand(384).astype(np.float32)
    await node.update_vector(db_id, "vector1", new_vector, {"updated": True})
    
    # Delete vector
    await node.delete_vector(db_id, "vector1")
```

### Graph Operations
```python
async def graph_operations(node, db_id):
    # Add relationship between vectors
    await node.add_relationship(
        db_id, 
        "vector1", 
        "vector2", 
        relationship_type="similar_to"
    )
    
    # Get relationships
    relationships = await node.get_relationships(db_id, "vector1")
    
    # Graph-based query with depth
    results = await node.query_with_graph(
        db_id,
        "vector1",
        k=10,
        max_depth=2  # How deep to traverse relationships
    )
```

### AI and RAG Features
```python
from vectrs.swarms import Swarms

async def ai_operations(node):
    # Initialize Swarms with your Claude API key
    api_key = "your-anthropic-api-key"  # or use environment variable ANTHROPIC_API_KEY
    swarms = Swarms(
        node.db_manager, 
        host='127.0.0.1', 
        port=8468,
        anthropic_api_key=api_key
    )
    await swarms.initialize()
    
    # Run RAG workflow with a query
    result = await swarms.run_rag_workflow(
        query="What is the relationship between these vectors?"
    )
    # Result contains: query, retrieved_context, plan, generated_answer, reflection
    
    # Create and manage AI agent
    agent = await swarms.create_custom_agent(
        agent_type="reflection",  # Available types: reflection, tool, planning
        agent_id="agent1"
    )
    
    # Check agent status
    status = await swarms.get_agent_status("agent1")
    
    # Analyze complex task
    analysis = await swarms.analyze_task({
        "type": "complex_task",
        "data": "Analyze the economic impact of climate change"
    })
    # Analysis contains: required_skills, complexity, dependencies, estimated_duration
```

You can provide your Claude API key in three ways:
1. Pass it directly to the Swarms constructor
2. Set it as an environment variable: `export ANTHROPIC_API_KEY=your-api-key`
3. Use the CLI argument: `python -m vectrs start-node --anthropic_api_key your-api-key`

### Advanced Features

#### Graphine Search
```python
async def graphine_search(node, db_id):
    # Advanced graph-based similarity search
    results = await node.graphine_search(
        db_id=db_id,
        vector_id="vector1",
        k=10,  # Number of results
        ef=50   # Size of dynamic list for search
    )
    return results
```

### Command Line Interface
```bash
# Start a node
python -m vectrs start-node --host 127.0.0.1 --port 8468

# Create a database
python -m vectrs create-db --dim 384 --space cosine --index_type hnsw

# Add a vector
python -m vectrs add-vector --db_id <db_id> --vector_id "vec1" --vector "0.1,0.2,0.3" --metadata '{"desc":"test"}'

# Query vectors
python -m vectrs query-vector --db_id <db_id> --vector_id "vec1" --query_k 10

# Run RAG workflow
python -m vectrs run-rag --query "What is the relationship between these vectors?"

# Create an AI agent
python -m vectrs create-agent --agent_type reflection --agent_id "agent1"
```

## API Reference

For detailed API documentation, visit our [documentation](https://github.com/ParalexLabs/Vectrs-beta/docs).

## Contributing
Contributions are welcome! Please check our [contribution guidelines](CONTRIBUTING.md).

## License   
Apache License 2.0. See [LICENSE](LICENSE) for details.

## Support   
- GitHub Issues: [Vectrs-beta Issues](https://github.com/ParalexLabs/Vectrs-beta/issues)
- Email: sakib@paralex.tech
- Version: 0.3.1
