# Home Inventory Knowledge Graph

An experiment with MCP and knowledge graphs for tracking items in your home.

## Features

- **Neo4j Knowledge Graph**: Store items, locations, categories, and their relationships
- **MCP Server**: Expose the knowledge graph through the Model Context Protocol
- **Flexible Schema**: Track items with properties like purchase date, value, quantity, and notes
- **Rich Queries**: Find items by location, category, or get detailed item information

## Prerequisites

1. **Neo4j Database**: Install and run Neo4j
   - Download from [neo4j.com/download](https://neo4j.com/download/)
   - Or use Docker: `docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_password neo4j:latest`

2. **Python 3.14+**: Required for this project

## Setup

1. **Clone and navigate to the project**:
   ```bash
   cd /run/media/drews/src/home-alog/home-alog
   ```
### 1. Setup Neo4j

**Option A: Docker (Easiest)**
```bash
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

**Option B: Download**
- Visit [neo4j.com/download](https://neo4j.com/download/)
- Install Neo4j Desktop or Community Edition

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Neo4j password
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Populate Sample Data

```bash
python examples/populate_sample_data.py
```

This creates:
- 5 locations (Living Room, Kitchen, Garage, Tool Box, Kitchen Drawer)
- 4 categories (Electronics, Tools, Kitchen, Furniture)
- 6 items with relationships

### 5. Run the MCP Server

```bash
python -m home_alog.server.mcp_server
```

### 6. Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "home-alog": {
      "command": "python",
      "args": ["-m", "home_alog.server.mcp_server"],
      "cwd": "/run/media/drews/src/home-alog/home-alog/src",
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your_password"
      }
    }
  }
}
```

## Project Structure

```
home-alog/
├── src/home_alog/
│   ├── database/
│   │   ├── __init__.py          # Database package exports
│   │   ├── connection.py        # Neo4j connection manager
│   │   ├── operations.py        # Graph CRUD operations
│   │   └── schema.py            # Graph schema definitions
│   ├── server/
│   │   ├── __init__.py          # Server package exports
│   │   └── mcp_server.py        # MCP server implementation
│   └── __init__.py              # Main package exports
├── examples/
│   └── populate_sample_data.py  # Sample data script
├── .env.example                 # Environment template
├── pyproject.toml               # Project dependencies
└── README.md                    # This file
```

## Available Tools

The MCP server provides these tools:

- `create_item` - Add a new item to inventory
- `create_location` - Create a location (room, shelf, box, etc.)
- `create_category` - Create an item category
- `link_item_to_location` - Place an item in a location
- `link_item_to_category` - Assign an item to a category
- `find_items_in_location` - Find all items in a location
- `find_items_by_category` - Find all items in a category
- `get_item_details` - Get detailed item information

## Example Usage

See `examples/populate_sample_data.py` for a complete example of populating the graph with sample data.

## Graph Schema

### Node Types
- **Item**: name, description, purchase_date, value, quantity, notes
- **Location**: name, type (room/shelf/box), description
- **Category**: name, description
- **Person**: name

### Relationship Types
- **LOCATED_IN**: Item → Location
- **BELONGS_TO**: Item → Category
- **OWNED_BY**: Item → Person
- **CONTAINS**: Location → Item (inverse of LOCATED_IN)

## Development

To explore the graph directly:
1. Open Neo4j Browser at http://localhost:7474
2. Run Cypher queries, e.g.:
   ```cypher
   MATCH (i:Item)-[:LOCATED_IN]->(l:Location)
   RETURN i.name, l.name
   ```
