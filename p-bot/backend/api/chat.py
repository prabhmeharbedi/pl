from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, AsyncGenerator
from uuid import uuid4
import json
import asyncio
import os

from agent_manager import AgentManager
from config import UPLOAD_DIR

router = APIRouter()

# Singleton instance of the agent manager
_agent_manager = None

def get_agent_manager() -> AgentManager:
    """Get or create a singleton instance of the agent manager."""
    global _agent_manager
    if _agent_manager is None:
        _agent_manager = AgentManager()
    return _agent_manager

class ChatRequest(BaseModel):
    """Chat request model for text-only queries."""
    message: str
    session_id: Optional[str] = None
    location: Optional[str] = None
    streaming: Optional[bool] = False

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    agent: str
    model: Optional[str] = "unknown"
    router: Optional[Dict[str, Any]] = {"target_agent": "unknown", "explanation": ""}
    tool_calls: Optional[List[Dict[str, Any]]] = []
    image_url: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, agent_manager: AgentManager = Depends(get_agent_manager)) -> ChatResponse:
    """Process a text-only chat message and return the response."""
    try:
        # Create a new session ID if none provided
        session_id = req.session_id or str(uuid4())
        
        print(f"Processing chat request: message='{req.message[:50]}...', session_id={session_id}")
        
        # Check if streaming is requested
        if req.streaming:
            # Redirect to streaming endpoint by raising an exception
            raise HTTPException(
                status_code=307,  # Temporary redirect
                headers={"Location": f"/api/v1/chat/stream?message={req.message}&session_id={session_id}"}
            )
        
        # Process the query
        result = await agent_manager.process_query(
            message=req.message,
            session_id=session_id,
            location=req.location
        )
        
        print(f"Got result: {str(result)[:100]}...")
        
        # Ensure result contains required fields
        if not isinstance(result, dict):
            print(f"Result is not a dict: {type(result)}")
            result = {
                "response": str(result),
                "agent": "unknown",
                "model": "unknown",
                "session_id": session_id,
                "router": {"target_agent": "unknown", "explanation": ""}
            }
        
        # Construct a valid ChatResponse
        response = {
            "response": result.get("response", "No response content"),
            "session_id": result.get("session_id", session_id),
            "agent": result.get("agent", "unknown"),
            "model": result.get("model", "unknown"),
            "router": result.get("router", {"target_agent": "unknown", "explanation": ""}),
            "tool_calls": result.get("tool_calls", [])
        }
        
        return ChatResponse(**response)
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

async def stream_response(message: str, session_id: str, location: Optional[str] = None) -> AsyncGenerator[str, None]:
    """Stream a response as server-sent events."""
    try:
        agent_manager = get_agent_manager()
        
        # First, determine the route
        route = await agent_manager.router.determine_route(
            message=message,
            has_image=False,
            session_id=session_id
        )
        
        target_agent_name = route["agent"]
        explanation = route["explanation"]
        
        # Yield the initial routing information
        routing_info = {
            "event": "routing",
            "data": {
                "agent": target_agent_name,
                "explanation": explanation
            }
        }
        yield f"data: {json.dumps(routing_info)}\n\n"
        await asyncio.sleep(0.1)  # Short delay for client processing
        
        # Get the target agent
        target_agent = agent_manager.agents[target_agent_name]
        
        # Start the streaming process
        response_text = ""
        chunk_size = 10  # Adjust based on your needs
        
        # Process with the agent
        response = await target_agent.process(
            message=message,
            session_id=session_id,
            location=location
        )
        
        # Extract the response text
        if isinstance(response, dict) and "response" in response:
            response_text = response.get("response", "")
        elif hasattr(response, "content") and response.content:
            response_text = response.content
        elif hasattr(response, "response") and response.response:
            response_text = response.response
        else:
            response_text = str(response)
        
        # Stream the response in chunks
        words = response_text.split()
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunk_data = {
                "event": "chunk",
                "data": {
                    "text": chunk,
                    "done": i + chunk_size >= len(words)
                }
            }
            yield f"data: {json.dumps(chunk_data)}\n\n"
            await asyncio.sleep(0.1)  # Short delay for realistic streaming
        
        # Send the complete message at the end
        final_data = {
            "event": "complete",
            "data": {
                "response": response_text,
                "agent": target_agent_name,
                "session_id": session_id,
                "model": getattr(response, "model", "unknown")
            }
        }
        yield f"data: {json.dumps(final_data)}\n\n"
    
    except Exception as e:
        error_data = {
            "event": "error",
            "data": {
                "message": str(e)
            }
        }
        yield f"data: {json.dumps(error_data)}\n\n"

@router.get("/chat/stream")
async def chat_stream(message: str, session_id: Optional[str] = None, location: Optional[str] = None):
    """Streaming endpoint for chat responses."""
    if not session_id:
        session_id = str(uuid4())
        
    return StreamingResponse(
        stream_response(message, session_id, location),
        media_type="text/event-stream"
    )

@router.post("/chat-with-image", response_model=ChatResponse)
async def chat_with_image(
    message: str = Form(...),
    session_id: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    image: UploadFile = File(...),
    agent_manager: AgentManager = Depends(get_agent_manager)
) -> ChatResponse:
    """Process a chat message with an image and return the response."""
    try:
        # Create a new session ID if none provided
        session_id = session_id or str(uuid4())
        
        print(f"Processing chat-with-image request: message='{message[:50]}...', session_id={session_id}")
        
        # Process the query with the image
        result = await agent_manager.process_query(
            message=message,
            session_id=session_id,
            image_file=image,
            location=location
        )
        
        print(f"Got result: {str(result)[:100]}...")
        
        # Ensure result contains required fields
        if not isinstance(result, dict):
            print(f"Result is not a dict: {type(result)}")
            result = {
                "response": str(result),
                "agent": "unknown",
                "model": "unknown",
                "session_id": session_id,
                "router": {"target_agent": "unknown", "explanation": ""}
            }
        
        # Get the saved image path from the agent_manager if available
        image_path = getattr(agent_manager, "last_image_path", None)
        image_url = None
        
        if image_path:
            # Convert absolute path to URL path
            rel_path = os.path.relpath(image_path, UPLOAD_DIR)
            image_url = f"/uploads/{rel_path.replace(os.sep, '/')}"
        
        # Construct a valid ChatResponse
        response = {
            "response": result.get("response", "No response content"),
            "session_id": result.get("session_id", session_id),
            "agent": result.get("agent", "unknown"),
            "model": result.get("model", "unknown"),
            "router": result.get("router", {"target_agent": "unknown", "explanation": ""}),
            "tool_calls": result.get("tool_calls", []),
            "image_url": image_url  # Add the image URL to the response
        }
        
        return ChatResponse(**response)
    except Exception as e:
        error_msg = f"Error processing message with image: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/agents")
def get_available_agents(agent_manager: AgentManager = Depends(get_agent_manager)):
    """Get the list of available specialized agents."""
    print(f"GET /agents endpoint called")
    try:
        response = {
            "agents": [
                {
                    "id": "issue_detection",
                    "name": "Issue Detection & Troubleshooting Agent",
                    "description": "Analyzes property images and descriptions to identify issues and provide troubleshooting advice.",
                    "capabilities": ["image_analysis", "text_analysis"],
                    "examples": [
                        "What's wrong with this wall? [+ image]",
                        "How do I fix this leaky faucet? [+ image]",
                        "Is this mold or just a stain? [+ image]"
                    ]
                },
                {
                    "id": "tenancy_faq",
                    "name": "Tenancy FAQ Agent",
                    "description": "Answers questions about tenancy laws, rental agreements, and landlord/tenant responsibilities.",
                    "capabilities": ["text_analysis"],
                    "examples": [
                        "How much notice do I need to give before moving out?",
                        "Can my landlord increase rent during the lease term?",
                        "What should I do if my landlord won't return my deposit?"
                    ]
                }
            ]
        }
        print(f"Returning agents: {len(response['agents'])}")
        return response
    except Exception as e:
        print(f"Error in GET /agents endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "agents": [
                {
                    "id": "issue_detection",
                    "name": "Issue Detection & Troubleshooting Agent (Fallback)",
                    "description": "Analyzes property images and descriptions to identify issues and provide troubleshooting advice.",
                    "capabilities": ["image_analysis", "text_analysis"],
                    "examples": ["Upload an image of property issues"]
                },
                {
                    "id": "tenancy_faq",
                    "name": "Tenancy FAQ Agent (Fallback)",
                    "description": "Answers questions about tenancy laws, rental agreements, and landlord/tenant responsibilities.",
                    "capabilities": ["text_analysis"],
                    "examples": ["Ask about tenant rights"]
                }
            ]
        } 