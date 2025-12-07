#!/usr/bin/env python3
"""Example script to populate the knowledge graph with sample data."""

from home_alog.database import GraphOperations, get_connection


def populate_sample_data():
    """Populate the graph with sample home inventory data."""
    graph = GraphOperations()
    
    print("Creating locations...")
    graph.create_location("Living Room", "room", "Main living area")
    graph.create_location("Kitchen", "room", "Cooking and dining area")
    graph.create_location("Garage", "room", "Storage and workshop")
    graph.create_location("Tool Box", "box", "Red metal tool box in garage")
    graph.create_location("Kitchen Drawer", "drawer", "Top drawer next to stove")
    
    print("Creating categories...")
    graph.create_category("Electronics", "Electronic devices and gadgets")
    graph.create_category("Tools", "Hand tools and power tools")
    graph.create_category("Kitchen", "Kitchen utensils and appliances")
    graph.create_category("Furniture", "Furniture items")
    
    print("Creating items...")
    graph.create_item(
        name="Samsung TV",
        description="55-inch 4K Smart TV",
        purchase_date="2023-01-15",
        value=799.99,
        quantity=1,
        notes="Warranty expires 2026-01-15"
    )
    
    graph.create_item(
        name="Cordless Drill",
        description="DeWalt 20V MAX cordless drill",
        purchase_date="2022-06-10",
        value=129.99,
        quantity=1,
        notes="Includes 2 batteries and charger"
    )
    
    graph.create_item(
        name="Screwdriver Set",
        description="24-piece precision screwdriver set",
        value=29.99,
        quantity=1
    )
    
    graph.create_item(
        name="Coffee Maker",
        description="Cuisinart programmable coffee maker",
        purchase_date="2021-11-20",
        value=89.99,
        quantity=1
    )
    
    graph.create_item(
        name="Kitchen Knives",
        description="Set of 6 chef knives",
        value=149.99,
        quantity=1
    )
    
    graph.create_item(
        name="Sofa",
        description="Gray sectional sofa",
        purchase_date="2020-03-15",
        value=1299.99,
        quantity=1
    )
    
    print("Creating relationships...")
    # Link items to locations
    graph.link_item_to_location("Samsung TV", "Living Room")
    graph.link_item_to_location("Cordless Drill", "Tool Box")
    graph.link_item_to_location("Screwdriver Set", "Tool Box")
    graph.link_item_to_location("Coffee Maker", "Kitchen")
    graph.link_item_to_location("Kitchen Knives", "Kitchen Drawer")
    graph.link_item_to_location("Sofa", "Living Room")
    
    # Link items to categories
    graph.link_item_to_category("Samsung TV", "Electronics")
    graph.link_item_to_category("Cordless Drill", "Tools")
    graph.link_item_to_category("Screwdriver Set", "Tools")
    graph.link_item_to_category("Coffee Maker", "Kitchen")
    graph.link_item_to_category("Kitchen Knives", "Kitchen")
    graph.link_item_to_category("Sofa", "Furniture")
    
    print("\nSample data populated successfully!")
    
    # Run some example queries
    print("\n=== Example Queries ===")
    
    print("\nItems in Tool Box:")
    items = graph.find_items_in_location("Tool Box")
    for item in items:
        print(f"  - {item['name']}: {item['description']}")
    
    print("\nAll Tools:")
    items = graph.find_items_by_category("Tools")
    for item in items:
        print(f"  - {item['name']}: {item['description']}")
    
    print("\nDetails for Samsung TV:")
    details = graph.get_item_details("Samsung TV")
    if details:
        print(f"  Name: {details['name']}")
        print(f"  Description: {details['description']}")
        print(f"  Location: {details['location']}")
        print(f"  Category: {details['category']}")
        print(f"  Value: ${details['value']}")
        print(f"  Notes: {details['notes']}")


if __name__ == "__main__":
    # Initialize database connection and constraints
    db = get_connection()
    db.initialize_constraints()
    
    # Populate sample data
    populate_sample_data()
