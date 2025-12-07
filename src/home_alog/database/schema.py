"""Home inventory knowledge graph schema definitions."""

from enum import Enum
from typing import TypedDict


class NodeType(str, Enum):
    """Types of nodes in the knowledge graph."""
    ITEM = "Item"
    LOCATION = "Location"
    CATEGORY = "Category"
    PERSON = "Person"


class RelationType(str, Enum):
    """Types of relationships in the knowledge graph."""
    LOCATED_IN = "LOCATED_IN"
    BELONGS_TO = "BELONGS_TO"
    OWNED_BY = "OWNED_BY"
    CONTAINS = "CONTAINS"


class ItemProperties(TypedDict, total=False):
    """Properties for Item nodes."""
    name: str
    description: str
    purchase_date: str
    value: float
    quantity: int
    notes: str


class LocationProperties(TypedDict, total=False):
    """Properties for Location nodes."""
    name: str
    type: str  # room, shelf, box, etc.
    description: str


class CategoryProperties(TypedDict, total=False):
    """Properties for Category nodes."""
    name: str
    description: str


class PersonProperties(TypedDict, total=False):
    """Properties for Person nodes."""
    name: str
