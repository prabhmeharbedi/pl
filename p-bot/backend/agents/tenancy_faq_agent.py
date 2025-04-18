from typing import Dict, List, Optional, Any

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.text import TextKnowledgeBase

from .base_agent import BaseAgent
from config import TENANCY_FAQ_AGENT, VECTOR_DB_PATH, KNOWLEDGE_DIR, OPENAI_API_KEY

class TenancyFAQAgent(BaseAgent):
    """Agent that handles tenancy FAQ questions related to laws, agreements, and responsibilities."""
    
    def __init__(self):
        # Set up additional tools for this agent
        tools = [
            DuckDuckGoTools(),  # For searching information about tenancy laws
        ]
        
        # Set up knowledge base for tenancy information
        vector_db = LanceDb(
            uri=str(VECTOR_DB_PATH),
            table_name="tenancy_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=OPENAI_API_KEY),
        )
        
        # Initialize the knowledge base
        self.knowledge = TextKnowledgeBase(
            path=KNOWLEDGE_DIR / "tenancy",
            vector_db=vector_db,
        )
        
        # Initialize the base agent
        super().__init__(
            name=TENANCY_FAQ_AGENT["name"],
            description=TENANCY_FAQ_AGENT["description"],
            model_id=TENANCY_FAQ_AGENT["model"],
            instructions=TENANCY_FAQ_AGENT["instructions"],
            tools=tools,
        )
        
        # Add knowledge to the agent
        self.agent.knowledge = self.knowledge
    
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
        """Add knowledge text by creating a file in the knowledge directory.
        
        Args:
            id: Unique identifier for the text
            title: Title of the document
            content: Content of the document
        """
        # Create a text file with the content in the knowledge directory
        file_path = KNOWLEDGE_DIR / "tenancy" / f"{id}.txt"
        with open(file_path, "w") as f:
            f.write(f"{title}\n\n{content}")
    
    def load_knowledge(self) -> None:
        """Load knowledge into the vector database."""
        self.knowledge.load() 