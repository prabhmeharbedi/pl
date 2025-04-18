from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.memory import AgentMemory
from typing import Dict, List, Optional, Any

from config import OPENAI_API_KEY, ANTHROPIC_API_KEY

class BaseAgent:
    """Base agent class that all specialized agents will inherit from."""
    
    def __init__(
        self,
        name: str,
        description: str,
        model_id: str,
        instructions: List[str],
        use_memory: bool = True,
        use_reasoning: bool = True,
        tools: Optional[List[Any]] = None,
    ):
        """Initialize the base agent.
        
        Args:
            name: Agent name
            description: Agent description
            model_id: The model ID to use
            instructions: List of instructions for the agent
            use_memory: Whether to use memory
            use_reasoning: Whether to use reasoning tools
            tools: Additional tools for the agent
        """
        self.name = name
        self.description = description
        self.model_id = model_id
        self.instructions = instructions
        self.use_memory = use_memory
        self.use_reasoning = use_reasoning
        
        # Set up tools
        self.tools = tools or []
        if use_reasoning:
            self.tools.append(ReasoningTools(add_instructions=True))
        
        # Set up model
        if "gpt" in model_id.lower():
            self.model = OpenAIChat(id=model_id, api_key=OPENAI_API_KEY)
        elif "claude" in model_id.lower():
            self.model = Claude(id=model_id, api_key=ANTHROPIC_API_KEY)
        else:
            # Default to OpenAI if model not recognized
            self.model = OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY)
        
        # Set up memory using AgentMemory
        self.memory = AgentMemory() if use_memory else None
        
        # Create the agent
        self.agent = Agent(
            model=self.model,
            description=self.description,
            instructions=self.instructions,
            tools=self.tools,
            memory=self.memory,
            markdown=True,
            show_tool_calls=True,
        )
    
    async def process(self, message: str, session_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Process a message and return the response.
        
        Args:
            message: The user message
            session_id: Optional session ID for memory continuity
            **kwargs: Additional context to pass to the agent
            
        Returns:
            A dictionary containing the response and additional metadata
        """
        # Create context with session ID and additional data
        context = {"session_id": session_id}
        context.update(kwargs)
        
        # Get response from agent
        response = await self.agent.get_async_response(message, context=context)
        
        # Format and return the response
        return {
            "agent": self.name,
            "response": response.response,
            "tool_calls": response.tool_calls if hasattr(response, "tool_calls") else [],
            "session_id": session_id or "default",
            "model": self.model_id,
        } 