from typing import Dict, List, Optional, Any
import os
import json
from pathlib import Path
import datetime
import time
import threading

class SessionMemoryStore:
    """
    A dedicated storage system for managing conversation history across multiple sessions.
    This ensures complete isolation between different conversations.
    """
    
    def __init__(self, storage_dir: str = "session_memory"):
        """Initialize the session memory store.
        
        Args:
            storage_dir: Directory to store session data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.sessions = {}
        self._lock = threading.RLock()  # Use a reentrant lock to avoid deadlocks
        self._load_existing_sessions()
        
    def _load_existing_sessions(self):
        """Load existing session data from disk."""
        for file_path in self.storage_dir.glob("*.json"):
            try:
                session_id = file_path.stem
                with open(file_path, "r") as f:
                    session_data = json.load(f)
                    self.sessions[session_id] = session_data
            except Exception as e:
                print(f"Error loading session {file_path}: {str(e)}")
                
    def _acquire_lock(self, timeout=2.0):
        """Try to acquire the lock with a timeout.
        
        Args:
            timeout: Maximum time to wait for the lock in seconds
            
        Returns:
            True if the lock was acquired, False otherwise
        """
        start_time = time.time()
        while True:
            if self._lock.acquire(blocking=False):
                return True
            
            if time.time() - start_time > timeout:
                print("Warning: Lock acquisition timed out!")
                return False
            
            # Small sleep to avoid CPU spinning
            time.sleep(0.01)
        
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get conversation history for a specific session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            The session data including conversation history
        """
        try:
            if not self._acquire_lock(timeout=2.0):
                # If lock acquisition fails, return a new empty session without saving
                return {
                    "created_at": datetime.datetime.now().isoformat(),
                    "last_updated": datetime.datetime.now().isoformat(),
                    "messages": []
                }
            
            try:
                if session_id not in self.sessions:
                    self.sessions[session_id] = {
                        "created_at": datetime.datetime.now().isoformat(),
                        "last_updated": datetime.datetime.now().isoformat(),
                        "messages": []
                    }
                    self._save_session(session_id)
                return self.sessions[session_id]
            finally:
                self._lock.release()
                
        except Exception as e:
            # In case of any errors, return a new empty session
            print(f"Error getting session: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "created_at": datetime.datetime.now().isoformat(),
                "last_updated": datetime.datetime.now().isoformat(),
                "messages": []
            }
    
    def add_message(self, session_id: str, message: Dict[str, Any]) -> None:
        """Add a message to a session's conversation history.
        
        Args:
            session_id: The session identifier
            message: The message to add with role, content, etc.
        """
        try:
            if not self._acquire_lock(timeout=2.0):
                print(f"Warning: Failed to add message to session {session_id} due to lock timeout")
                return
            
            try:
                session = self.get_session(session_id)
                session["messages"].append(message)
                session["last_updated"] = datetime.datetime.now().isoformat()
                self._save_session(session_id)
            finally:
                self._lock.release()
        except Exception as e:
            print(f"Error adding message: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get messages for a specific session, with optional limit.
        
        Args:
            session_id: The session identifier
            limit: Optional maximum number of messages to return
            
        Returns:
            List of messages in chronological order
        """
        try:
            session = self.get_session(session_id)
            messages = session.get("messages", [])
            if limit is not None and limit > 0 and len(messages) > limit:
                return messages[-limit:]
            return messages
        except Exception as e:
            print(f"Error getting messages: {str(e)}")
            import traceback
            traceback.print_exc()
            return []  # Return empty list on error
    
    def clear_session(self, session_id: str) -> None:
        """Clear a session's conversation history.
        
        Args:
            session_id: The session identifier
        """
        try:
            if not self._acquire_lock(timeout=2.0):
                print(f"Warning: Failed to clear session {session_id} due to lock timeout")
                return
            
            try:
                if session_id in self.sessions:
                    self.sessions[session_id]["messages"] = []
                    self.sessions[session_id]["last_updated"] = datetime.datetime.now().isoformat()
                    self._save_session(session_id)
            finally:
                self._lock.release()
        except Exception as e:
            print(f"Error clearing session: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session completely.
        
        Args:
            session_id: The session identifier
        """
        try:
            if not self._acquire_lock(timeout=2.0):
                print(f"Warning: Failed to delete session {session_id} due to lock timeout")
                return
            
            try:
                if session_id in self.sessions:
                    del self.sessions[session_id]
                    session_file = self.storage_dir / f"{session_id}.json"
                    if session_file.exists():
                        session_file.unlink()
            finally:
                self._lock.release()
        except Exception as e:
            print(f"Error deleting session: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _save_session(self, session_id: str) -> None:
        """Save session data to disk.
        
        Args:
            session_id: The session identifier
        """
        try:
            session_file = self.storage_dir / f"{session_id}.json"
            with open(session_file, "w") as f:
                json.dump(self.sessions[session_id], f, indent=2)
        except Exception as e:
            print(f"Error saving session: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions with metadata.
        
        Returns:
            List of session metadata
        """
        try:
            result = []
            if not self._acquire_lock(timeout=2.0):
                print("Warning: Failed to list sessions due to lock timeout")
                return result
            
            try:
                for session_id, data in self.sessions.items():
                    result.append({
                        "session_id": session_id,
                        "created_at": data.get("created_at"),
                        "last_updated": data.get("last_updated"),
                        "message_count": len(data.get("messages", []))
                    })
                return result
            finally:
                self._lock.release()
        except Exception as e:
            print(f"Error listing sessions: {str(e)}")
            import traceback
            traceback.print_exc()
            return []  # Return empty list on error

# Create a singleton instance
_memory_store = None

def get_memory_store() -> SessionMemoryStore:
    """Get the global session memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = SessionMemoryStore()
    return _memory_store 