from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.memory import ThreadMemory
from typing import Dict, List, Optional, Any

from config import OPENAI_API_KEY, ANTHROPIC_API_KEY, DEFAULT_MODEL, ALTERNATIVE_MODEL, VECTOR_DB_PATH


class PBot:
    """P-Bot agent implementation using Agno framework."""

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL,
        use_memory: bool = True,
        use_reasoning: bool = True,
        use_search: bool = True,
        instructions: Optional[List[str]] = None,
    ):
        """Initialize the P-Bot agent.
        
        Args:
            model_id: The model ID to use (default: configured DEFAULT_MODEL)
            use_memory: Whether to use memory (default: True)
            use_reasoning: Whether to use reasoning tools (default: True)
            use_search: Whether to use search tools (default: True)
            instructions: Custom instructions for the agent
        """
        self.model_id = model_id
        self.use_memory = use_memory
        self.use_reasoning = use_reasoning
        self.use_search = use_search
        
        # Set up tools
        tools = []
        if use_reasoning:
            tools.append(ReasoningTools(add_instructions=True))
        if use_search:
            tools.append(DuckDuckGoTools())
        
        # Set up model
        if "gpt" in model_id.lower():
            model = OpenAIChat(id=model_id, api_key=OPENAI_API_KEY)
        elif "claude" in model_id.lower():
            model = Claude(id=model_id, api_key=ANTHROPIC_API_KEY)
        else:
            # Default to OpenAI if model not recognized
            model = OpenAIChat(id=DEFAULT_MODEL, api_key=OPENAI_API_KEY)
        
        # Set up default instructions if none provided
        default_instructions = [
            "You are P-Bot, a helpful and knowledgeable AI assistant.",
            "Provide accurate and helpful responses to user queries.",
            "If you don't know the answer, be honest about it.",
            "When searching for information, use your tools effectively.",
        ]
        
        final_instructions = instructions if instructions else default_instructions
        
        # Set up memory
        memory = ThreadMemory() if use_memory else None
        
        # Set up vector database for knowledge (to be used later)
        vector_db = LanceDb(
            uri=str(VECTOR_DB_PATH),
            table_name="p_bot_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=OPENAI_API_KEY),
        )
        
        # Create the agent
        self.agent = Agent(
            model=model,
            description="P-Bot is a helpful AI assistant that provides accurate and insightful responses.",
            instructions=final_instructions,
            tools=tools,
            memory=memory,
            markdown=True,
            show_tool_calls=True,
        )
    
    async def chat(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a chat message and return the response.
        
        Args:
            message: The user message
            session_id: Optional session ID for memory continuity
            
        Returns:
            A dictionary containing the response and additional metadata
        """
        # Create context with session ID if provided
        context = {"session_id": session_id} if session_id else {}
        
        # Get response from agent
        response = await self.agent.get_async_response(message, context=context)
        
        # Format and return the response
        return {
            "response": response.response,
            "tool_calls": response.tool_calls if hasattr(response, "tool_calls") else [],
            "session_id": session_id or "default",
            "model": self.model_id,
        } 