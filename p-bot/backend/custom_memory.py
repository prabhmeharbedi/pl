from typing import Dict, List, Optional, Any, Callable
from memory_store import get_memory_store

class CustomSessionMemory:
    """
    Custom memory provider that uses the SessionMemoryStore to ensure
    complete isolation between different conversations.
    """
    
    def __init__(self, max_messages: int = 20):
        """Initialize the custom session memory provider.
        
        Args:
            max_messages: Maximum number of messages to remember per session
        """
        self.store = get_memory_store()
        self.max_messages = max_messages
        
    async def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            List of messages in the session history
        """
        return self.store.get_messages(session_id, self.max_messages)
    
    async def add_to_history(self, session_id: str, message: Dict[str, Any]) -> None:
        """Add a message to the session history.
        
        Args:
            session_id: The session identifier
            message: The message to add
        """
        self.store.add_message(session_id, message)
    
    async def clear_history(self, session_id: str) -> None:
        """Clear the history for a specific session.
        
        Args:
            session_id: The session identifier
        """
        self.store.clear_session(session_id)
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert the memory provider to a dictionary.
        
        Returns:
            Dictionary representation of the memory provider
        """
        return {
            "type": "custom_session_memory",
            "max_messages": self.max_messages
        }
        
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CustomSessionMemory':
        """Create a memory provider from a dictionary.
        
        Args:
            data: Dictionary representation of the memory provider
            
        Returns:
            A new CustomSessionMemory instance
        """
        return CustomSessionMemory(max_messages=data.get("max_messages", 20)) 