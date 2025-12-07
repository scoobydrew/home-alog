"""Graph operations for managing the home inventory knowledge graph."""

from typing import Any, Optional

from .connection import get_connection
from .schema import NodeType, RelationType


class GraphOperations:
    """Operations for managing nodes and relationships in the knowledge graph."""
    
    def __init__(self):
        self.db = get_connection()
    
    # ===== Node Operations =====
    
    def create_item(
        self,
        name: str,
        description: str = "",
        purchase_date: Optional[str] = None,
        value: Optional[float] = None,
        quantity: int = 1,
        notes: str = ""
    ) -> dict[str, Any]:
        """Create a new Item node.
        
        Args:
            name: Item name (unique)
            description: Item description
            purchase_date: Purchase date (ISO format)
            value: Monetary value
            quantity: Number of items
            notes: Additional notes
            
        Returns:
            Created node properties
        """
        query = """
        CREATE (i:Item {
            name: $name,
            description: $description,
            purchase_date: $purchase_date,
            value: $value,
            quantity: $quantity,
            notes: $notes
        })
        RETURN i
        """
        result = self.db.execute_query(query, {
            "name": name,
            "description": description,
            "purchase_date": purchase_date,
            "value": value,
            "quantity": quantity,
            "notes": notes
        })
        return result[0]["i"] if result else {}
    
    def create_location(self, name: str, location_type: str = "room", description: str = "") -> dict[str, Any]:
        """Create a new Location node.
        
        Args:
            name: Location name (unique)
            location_type: Type of location (room, shelf, box, etc.)
            description: Location description
            
        Returns:
            Created node properties
        """
        query = """
        CREATE (l:Location {
            name: $name,
            type: $location_type,
            description: $description
        })
        RETURN l
        """
        result = self.db.execute_query(query, {
            "name": name,
            "location_type": location_type,
            "description": description
        })
        return result[0]["l"] if result else {}
    
    def create_category(self, name: str, description: str = "") -> dict[str, Any]:
        """Create a new Category node.
        
        Args:
            name: Category name (unique)
            description: Category description
            
        Returns:
            Created node properties
        """
        query = """
        CREATE (c:Category {
            name: $name,
            description: $description
        })
        RETURN c
        """
        result = self.db.execute_query(query, {
            "name": name,
            "description": description
        })
        return result[0]["c"] if result else {}
    
    def create_person(self, name: str) -> dict[str, Any]:
        """Create a new Person node.
        
        Args:
            name: Person name (unique)
            
        Returns:
            Created node properties
        """
        query = """
        CREATE (p:Person {name: $name})
        RETURN p
        """
        result = self.db.execute_query(query, {"name": name})
        return result[0]["p"] if result else {}
    
    # ===== Relationship Operations =====
    
    def link_item_to_location(self, item_name: str, location_name: str) -> bool:
        """Create LOCATED_IN relationship between item and location.
        
        Args:
            item_name: Name of the item
            location_name: Name of the location
            
        Returns:
            True if relationship was created
        """
        query = """
        MATCH (i:Item {name: $item_name})
        MATCH (l:Location {name: $location_name})
        MERGE (i)-[:LOCATED_IN]->(l)
        RETURN i, l
        """
        result = self.db.execute_query(query, {
            "item_name": item_name,
            "location_name": location_name
        })
        return len(result) > 0
    
    def link_item_to_category(self, item_name: str, category_name: str) -> bool:
        """Create BELONGS_TO relationship between item and category.
        
        Args:
            item_name: Name of the item
            category_name: Name of the category
            
        Returns:
            True if relationship was created
        """
        query = """
        MATCH (i:Item {name: $item_name})
        MATCH (c:Category {name: $category_name})
        MERGE (i)-[:BELONGS_TO]->(c)
        RETURN i, c
        """
        result = self.db.execute_query(query, {
            "item_name": item_name,
            "category_name": category_name
        })
        return len(result) > 0
    
    def link_item_to_owner(self, item_name: str, person_name: str) -> bool:
        """Create OWNED_BY relationship between item and person.
        
        Args:
            item_name: Name of the item
            person_name: Name of the person
            
        Returns:
            True if relationship was created
        """
        query = """
        MATCH (i:Item {name: $item_name})
        MATCH (p:Person {name: $person_name})
        MERGE (i)-[:OWNED_BY]->(p)
        RETURN i, p
        """
        result = self.db.execute_query(query, {
            "item_name": item_name,
            "person_name": person_name
        })
        return len(result) > 0
    
    # ===== Query Operations =====
    
    def find_items_in_location(self, location_name: str) -> list[dict[str, Any]]:
        """Find all items in a specific location.
        
        Args:
            location_name: Name of the location
            
        Returns:
            List of item properties
        """
        query = """
        MATCH (i:Item)-[:LOCATED_IN]->(l:Location {name: $location_name})
        RETURN i
        """
        result = self.db.execute_query(query, {"location_name": location_name})
        return [record["i"] for record in result]
    
    def find_items_by_category(self, category_name: str) -> list[dict[str, Any]]:
        """Find all items in a specific category.
        
        Args:
            category_name: Name of the category
            
        Returns:
            List of item properties
        """
        query = """
        MATCH (i:Item)-[:BELONGS_TO]->(c:Category {name: $category_name})
        RETURN i
        """
        result = self.db.execute_query(query, {"category_name": category_name})
        return [record["i"] for record in result]
    
    def get_item_details(self, item_name: str) -> Optional[dict[str, Any]]:
        """Get detailed information about an item including relationships.
        
        Args:
            item_name: Name of the item
            
        Returns:
            Item details with location, category, and owner information
        """
        query = """
        MATCH (i:Item {name: $item_name})
        OPTIONAL MATCH (i)-[:LOCATED_IN]->(l:Location)
        OPTIONAL MATCH (i)-[:BELONGS_TO]->(c:Category)
        OPTIONAL MATCH (i)-[:OWNED_BY]->(p:Person)
        RETURN i, l.name as location, c.name as category, p.name as owner
        """
        result = self.db.execute_query(query, {"item_name": item_name})
        if not result:
            return None
        
        record = result[0]
        details = dict(record["i"])
        details["location"] = record.get("location")
        details["category"] = record.get("category")
        details["owner"] = record.get("owner")
        return details
    
    def list_all_locations(self) -> list[dict[str, Any]]:
        """List all locations in the graph."""
        query = "MATCH (l:Location) RETURN l ORDER BY l.name"
        result = self.db.execute_query(query)
        return [record["l"] for record in result]
    
    def list_all_categories(self) -> list[dict[str, Any]]:
        """List all categories in the graph."""
        query = "MATCH (c:Category) RETURN c ORDER BY c.name"
        result = self.db.execute_query(query)
        return [record["c"] for record in result]
