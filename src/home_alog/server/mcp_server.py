#!/usr/bin/env python3
"""MCP server for home inventory knowledge graph."""

import json
from typing import Any

from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from home_alog.database import GraphOperations, get_connection


# Initialize MCP server
app = Server("home-alog")

# Initialize graph operations
graph = GraphOperations()


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources in the knowledge graph."""
    return [
        Resource(
            uri="graph://locations",
            name="All Locations",
            mimeType="application/json",
            description="List of all locations in the home"
        ),
        Resource(
            uri="graph://categories",
            name="All Categories",
            mimeType="application/json",
            description="List of all item categories"
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource from the knowledge graph."""
    if uri == "graph://locations":
        locations = graph.list_all_locations()
        return json.dumps(locations, indent=2)
    elif uri == "graph://categories":
        categories = graph.list_all_categories()
        return json.dumps(categories, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for managing the knowledge graph."""
    return [
        Tool(
            name="create_item",
            description="Create a new item in the inventory",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Item name (unique)"},
                    "description": {"type": "string", "description": "Item description"},
                    "purchase_date": {"type": "string", "description": "Purchase date (ISO format)"},
                    "value": {"type": "number", "description": "Monetary value"},
                    "quantity": {"type": "integer", "description": "Number of items", "default": 1},
                    "notes": {"type": "string", "description": "Additional notes"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="create_location",
            description="Create a new location (room, shelf, box, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Location name (unique)"},
                    "location_type": {"type": "string", "description": "Type (room, shelf, box, etc.)", "default": "room"},
                    "description": {"type": "string", "description": "Location description"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="create_category",
            description="Create a new item category",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Category name (unique)"},
                    "description": {"type": "string", "description": "Category description"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="link_item_to_location",
            description="Place an item in a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item"},
                    "location_name": {"type": "string", "description": "Name of the location"},
                },
                "required": ["item_name", "location_name"],
            },
        ),
        Tool(
            name="link_item_to_category",
            description="Assign an item to a category",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item"},
                    "category_name": {"type": "string", "description": "Name of the category"},
                },
                "required": ["item_name", "category_name"],
            },
        ),
        Tool(
            name="find_items_in_location",
            description="Find all items in a specific location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_name": {"type": "string", "description": "Name of the location"},
                },
                "required": ["location_name"],
            },
        ),
        Tool(
            name="find_items_by_category",
            description="Find all items in a specific category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category_name": {"type": "string", "description": "Name of the category"},
                },
                "required": ["category_name"],
            },
        ),
        Tool(
            name="get_item_details",
            description="Get detailed information about an item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item"},
                },
                "required": ["item_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a tool operation."""
    try:
        if name == "create_item":
            result = graph.create_item(**arguments)
            return [TextContent(type="text", text=f"Created item: {json.dumps(result, indent=2)}")]
        
        elif name == "create_location":
            result = graph.create_location(**arguments)
            return [TextContent(type="text", text=f"Created location: {json.dumps(result, indent=2)}")]
        
        elif name == "create_category":
            result = graph.create_category(**arguments)
            return [TextContent(type="text", text=f"Created category: {json.dumps(result, indent=2)}")]
        
        elif name == "link_item_to_location":
            success = graph.link_item_to_location(**arguments)
            if success:
                return [TextContent(type="text", text=f"Linked {arguments['item_name']} to {arguments['location_name']}")]
            else:
                return [TextContent(type="text", text="Failed to create link. Check that both item and location exist.")]
        
        elif name == "link_item_to_category":
            success = graph.link_item_to_category(**arguments)
            if success:
                return [TextContent(type="text", text=f"Linked {arguments['item_name']} to category {arguments['category_name']}")]
            else:
                return [TextContent(type="text", text="Failed to create link. Check that both item and category exist.")]
        
        elif name == "find_items_in_location":
            items = graph.find_items_in_location(arguments["location_name"])
            return [TextContent(type="text", text=json.dumps(items, indent=2))]
        
        elif name == "find_items_by_category":
            items = graph.find_items_by_category(arguments["category_name"])
            return [TextContent(type="text", text=json.dumps(items, indent=2))]
        
        elif name == "get_item_details":
            details = graph.get_item_details(arguments["item_name"])
            if details:
                return [TextContent(type="text", text=json.dumps(details, indent=2))]
            else:
                return [TextContent(type="text", text=f"Item '{arguments['item_name']}' not found")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    # Initialize database constraints
    db = get_connection()
    db.initialize_constraints()
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
