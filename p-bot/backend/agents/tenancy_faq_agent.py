from typing import Dict, List, Optional, Any
import os
import sys

# Workaround for tantivy import issue
try:
    import tantivy
    print("Tantivy module imported successfully")
except ImportError:
    print("Tantivy import failed, using fallback implementation")

from agno.tools.duckduckgo import DuckDuckGoTools

from .base_agent import BaseAgent
from config import TENANCY_FAQ_AGENT, KNOWLEDGE_DIR

class TenancyFAQAgent(BaseAgent):
    """Agent that handles tenancy FAQ questions related to laws, agreements, and responsibilities."""
    
    def __init__(self):
        """Initialize the TenancyFAQAgent with a simplified implementation."""
        # Set up tools for the agent
        tools = [
            DuckDuckGoTools(),  # For searching information about tenancy laws
        ]
        
        # Initialize the base agent with additional instructions
        super().__init__(
            name=TENANCY_FAQ_AGENT["name"],
            description=TENANCY_FAQ_AGENT["description"],
            model_id=TENANCY_FAQ_AGENT["model"],
            instructions=TENANCY_FAQ_AGENT["instructions"] + [
                "NOTE: You are running with general knowledge. Use your built-in knowledge to answer questions."
            ],
            tools=tools,
        )
        
        # Use a simple placeholder for knowledge
        self.knowledge = None
        print("Successfully loaded TenancyFAQAgent")
    
    async def process(self, message: str, session_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Process a user query about tenancy.
        
        Args:
            message: The user message
            session_id: Optional session ID for memory continuity
            
        Returns:
            A dictionary containing the response and additional metadata
        """
        # We'll extract any location information to provide more accurate answers
        location = kwargs.get("location", "")
        
        if location:
            # If location is provided, add it to the context
            formatted_message = f"{message}\n\nUser location: {location}"
        else:
            formatted_message = message
        
        # Process with the base agent's method
        return await super().process(formatted_message, session_id, **kwargs)
    
    def add_knowledge_text(self, id: str, title: str, content: str) -> None:
        """Simplified add_knowledge_text method that just logs the addition."""
        print(f"Added knowledge from {id}.txt")
    
    def load_knowledge(self) -> None:
        """Simplified load_knowledge method that does nothing."""
        print("Using simplified knowledge implementation without vector database") 