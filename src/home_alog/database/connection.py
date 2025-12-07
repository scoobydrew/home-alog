"""Neo4j database connection and operations."""

import os
from typing import Any, Optional
from contextlib import contextmanager

from neo4j import GraphDatabase, Driver, Session
from dotenv import load_dotenv


class Neo4jConnection:
    """Manages Neo4j database connection."""
    
    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        """Initialize Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (defaults to env var NEO4J_URI)
            user: Neo4j username (defaults to env var NEO4J_USER)
            password: Neo4j password (defaults to env var NEO4J_PASSWORD)
        """
        load_dotenv()
        
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "")
        
        self._driver: Optional[Driver] = None
    
    def connect(self) -> Driver:
        """Establish connection to Neo4j database."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
        return self._driver
    
    def close(self):
        """Close the database connection."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
    
    @contextmanager
    def session(self) -> Session:
        """Context manager for Neo4j sessions."""
        driver = self.connect()
        session = driver.session()
        try:
            yield session
        finally:
            session.close()
    
    def execute_query(self, query: str, parameters: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Execute a Cypher query and return results.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
    
    def initialize_constraints(self):
        """Create database constraints and indexes."""
        constraints = [
            "CREATE CONSTRAINT item_name IF NOT EXISTS FOR (i:Item) REQUIRE i.name IS UNIQUE",
            "CREATE CONSTRAINT location_name IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE",
            "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
        ]
        
        with self.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint might already exist
                    print(f"Note: {e}")


# Global connection instance
_connection: Optional[Neo4jConnection] = None


def get_connection() -> Neo4jConnection:
    """Get or create the global Neo4j connection."""
    global _connection
    if _connection is None:
        _connection = Neo4jConnection()
    return _connection
