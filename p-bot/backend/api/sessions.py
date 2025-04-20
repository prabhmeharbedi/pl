from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel
from memory_store import get_memory_store

router = APIRouter()

class SessionInfo(BaseModel):
    """Information about a session."""
    session_id: str
    created_at: str
    last_updated: str
    message_count: int

class SessionDetail(BaseModel):
    """Detailed session information including messages."""
    session_id: str
    created_at: str
    last_updated: str
    messages: List[Dict]

@router.get("/sessions", response_model=List[SessionInfo])
def list_sessions():
    """List all active sessions."""
    memory_store = get_memory_store()
    return memory_store.list_sessions()

@router.get("/sessions/{session_id}", response_model=SessionDetail)
def get_session(session_id: str):
    """Get detailed information about a specific session."""
    memory_store = get_memory_store()
    
    # Check if session exists
    if session_id not in memory_store.sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    session = memory_store.get_session(session_id)
    messages = memory_store.get_messages(session_id)
    
    return {
        "session_id": session_id,
        "created_at": session.get("created_at", ""),
        "last_updated": session.get("last_updated", ""),
        "messages": messages
    }

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """Delete a session and all its messages."""
    memory_store = get_memory_store()
    
    # Check if session exists
    if session_id not in memory_store.sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    memory_store.delete_session(session_id)
    return {"status": "success", "message": f"Session {session_id} deleted"}

@router.delete("/sessions/{session_id}/messages")
def clear_session_messages(session_id: str):
    """Clear all messages in a session but keep the session itself."""
    memory_store = get_memory_store()
    
    # Check if session exists
    if session_id not in memory_store.sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    memory_store.clear_session(session_id)
    return {"status": "success", "message": f"Messages for session {session_id} cleared"} 