import uvicorn
from fastapi import FastAPI, Body, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
import datetime

from api import router as api_router
from config import API_PREFIX, ALLOW_ORIGINS, UPLOAD_DIR, VECTOR_DB_PATH, KNOWLEDGE_DIR
from memory_store import get_memory_store

# Create directory structure if it doesn't exist
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="P-Bot API",
    description="API for the P-Bot real estate chatbot with multiple specialized agents",
    version="0.2.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Include API router
app.include_router(api_router, prefix=API_PREFIX)

@app.get("/api/v1/test")
async def direct_test_endpoint():
    """Direct test endpoint for API routing."""
    return {"status": "ok", "message": "Direct API test endpoint is accessible"}

@app.get("/api/v1/agents")
async def direct_agents_endpoint():
    """Direct implementation of the agents endpoint."""
    print("Direct /api/v1/agents endpoint called")
    return {
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

@app.post("/api/v1/chat")
async def direct_chat_endpoint(req: dict = Body(...)):
    """Direct implementation of the chat endpoint."""
    try:
        # Log the full request
        print(f"==== CHAT REQUEST RECEIVED ====")
        print(f"Request body: {req}")
        
        # Extract request parameters
        message = req.get("message", "")
        session_id = req.get("session_id", "unknown-session")
        location = req.get("location")
        
        print(f"Message: '{message}'")
        print(f"Session ID: '{session_id}'")
        print(f"Location: '{location}'")
        
        # Import the agent manager and call process_query
        try:
            from agent_manager import AgentManager
            
            # Create the agent manager
            manager = AgentManager()
            print("AgentManager created successfully")
            
            # Process the query
            result = await manager.process_query(
                message=message,
                session_id=session_id,
                location=location
            )
            
            print(f"Query processed successfully: {result}")
            return result
            
        except ImportError as import_err:
            print(f"Error importing agent_manager: {str(import_err)}")
            import traceback
            traceback.print_exc()
            
            # Return a simple error response
            return {
                "response": f"I'm sorry, I couldn't process your request due to a system error: {str(import_err)}",
                "session_id": session_id,
                "agent": "router",
                "model": "error-handler",
                "router": {"target_agent": "router", "explanation": "Import error"}
            }
            
    except Exception as e:
        # Log the full error
        print(f"==== CHAT ENDPOINT ERROR ====")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return a simple error response
        return {
            "response": "I'm sorry, I encountered an error processing your message. Technical team has been notified.",
            "session_id": req.get("session_id", "unknown-session"),
            "agent": "router",
            "model": "error-handler",
            "router": {"target_agent": "router", "explanation": "Error handling"}
        }

@app.get("/api/v1/sessions")
async def direct_sessions_endpoint():
    """Direct implementation of the sessions endpoint."""
    print("Direct /api/v1/sessions endpoint called")
    try:
        memory_store = get_memory_store()
        return memory_store.list_sessions()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in direct sessions endpoint: {str(e)}")
        return []

@app.get("/api/v1/sessions/{session_id}")
async def direct_session_detail_endpoint(session_id: str):
    """Direct implementation of the session detail endpoint."""
    print(f"Direct /api/v1/sessions/{session_id} endpoint called")
    try:
        memory_store = get_memory_store()
        
        # Check if session exists
        if session_id not in memory_store.sessions:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        session = memory_store.get_session(session_id)
        messages = memory_store.get_messages(session_id)
        
        return {
            "session_id": session_id,
            "created_at": session.get("created_at", ""),
            "last_updated": session.get("last_updated", ""),
            "messages": messages
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in direct session detail endpoint: {str(e)}")
        return {"error": str(e)}

@app.delete("/api/v1/sessions/{session_id}")
async def direct_delete_session_endpoint(session_id: str):
    """Direct implementation of the delete session endpoint."""
    print(f"Direct DELETE /api/v1/sessions/{session_id} endpoint called")
    try:
        memory_store = get_memory_store()
        
        # Check if session exists
        if session_id not in memory_store.sessions:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        memory_store.delete_session(session_id)
        return {"status": "success", "message": f"Session {session_id} deleted"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in direct delete session endpoint: {str(e)}")
        return {"error": str(e)}

@app.delete("/api/v1/sessions/{session_id}/messages")
async def direct_clear_session_messages_endpoint(session_id: str):
    """Direct implementation of the clear session messages endpoint."""
    print(f"Direct DELETE /api/v1/sessions/{session_id}/messages endpoint called")
    try:
        memory_store = get_memory_store()
        
        # Check if session exists
        if session_id not in memory_store.sessions:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        memory_store.clear_session(session_id)
        return {"status": "success", "message": f"Messages for session {session_id} cleared"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in direct clear session messages endpoint: {str(e)}")
        return {"error": str(e)}

@app.post("/api/v1/chat-with-image")
async def direct_chat_with_image_endpoint(
    message: str = Form(...),
    session_id: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(...)
):
    """Direct implementation of the chat-with-image endpoint."""
    print(f"Direct /api/v1/chat-with-image endpoint called with message: {message}, session_id: {session_id}")
    try:
        from agent_manager import AgentManager
        from uuid import uuid4
        import os
        
        # Ensure session ID
        if not session_id:
            session_id = str(uuid4())
            
        # Create a new agent manager
        manager = AgentManager()
        
        # Process the query with the image
        result = await manager.process_query(
            message=message,
            session_id=session_id,
            image_file=image,
            location=location
        )
        
        # Ensure result contains required fields
        if not isinstance(result, dict):
            result = {
                "response": str(result),
                "agent": "issue_detection",
                "model": "unknown",
                "session_id": session_id,
                "router": {"target_agent": "issue_detection", "explanation": "Image processing"}
            }
        
        # Get the saved image path from the agent_manager if available
        image_path = getattr(manager, "last_image_path", None)
        image_url = None
        
        if image_path:
            # Convert absolute path to URL path
            from config import UPLOAD_DIR
            rel_path = os.path.relpath(image_path, UPLOAD_DIR)
            image_url = f"/uploads/{rel_path.replace(os.sep, '/')}"
        
        # Construct a valid response
        response = {
            "response": result.get("response", "No response content"),
            "session_id": result.get("session_id", session_id),
            "agent": result.get("agent", "issue_detection"),
            "model": result.get("model", "unknown"),
            "router": result.get("router", {"target_agent": "issue_detection", "explanation": "Image processing"}),
            "tool_calls": result.get("tool_calls", []),
            "image_url": image_url
        }
        
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in direct chat-with-image endpoint: {str(e)}")
        return {
            "response": "I'm sorry, I encountered an error processing your image. Please try again with a different image or send a text-only query.",
            "session_id": session_id or str(uuid4()),
            "agent": "issue_detection",
            "model": "unknown",
            "router": {"target_agent": "issue_detection", "explanation": "Error processing image"}
        }

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok", 
        "message": "P-Bot API is running",
        "version": "0.2.0",
        "features": ["multi-agent", "image-processing", "tenancy-faq"]
    }

@app.get("/api-status")
async def api_status():
    """API status endpoint for troubleshooting."""
    return {
        "status": "ok",
        "message": "API status endpoint is accessible",
        "time": str(datetime.datetime.now()),
        "endpoints": {
            "agents": "/api/v1/agents",
            "chat": "/api/v1/chat",
            "chat_with_image": "/api/v1/chat-with-image",
            "sessions": "/api/v1/sessions"
        }
    }

@app.get("/api/v1/diagnostics")
async def check_agent_manager():
    """Diagnostic endpoint to check if AgentManager and agents are loading properly."""
    try:
        from agent_manager import AgentManager
        manager = AgentManager()
        
        # Check if we can access the agents
        agents_info = {}
        for agent_name, agent in manager.agents.items():
            agents_info[agent_name] = {
                "name": agent_name,
                "type": type(agent).__name__,
                "attributes": [attr for attr in dir(agent) if not attr.startswith('_')],
                "status": "loaded"
            }
        
        # Check if the router is initialized
        router_status = {
            "exists": hasattr(manager, 'router'),
            "type": type(manager.router).__name__ if hasattr(manager, 'router') else None
        }
        
        # Try to load the memory store
        try:
            memory_store = get_memory_store()
            memory_status = {
                "loaded": True,
                "type": type(memory_store).__name__,
                "sessions": list(memory_store.sessions.keys()) if hasattr(memory_store, 'sessions') else []
            }
        except Exception as memory_err:
            memory_status = {"loaded": False, "error": str(memory_err)}
        
        # Diagnostic info
        return {
            "status": "ok",
            "agent_manager": {
                "loaded": True,
                "type": type(manager).__name__,
                "agents": agents_info,
                "router": router_status
            },
            "memory_store": memory_status,
            "system_info": {
                "python_path": os.environ.get("PYTHONPATH", "Not set"),
                "current_dir": os.getcwd()
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# Load some initial tenancy knowledge if available
try:
    from utils.knowledge_loader import load_initial_knowledge
    load_initial_knowledge()
except Exception as e:
    print(f"Warning: Failed to load initial knowledge: {str(e)}")

@app.post("/api/v1/debug/router")
async def debug_router_endpoint(req: dict = Body(...)):
    """Debug endpoint specifically for the router agent."""
    try:
        # Extract message and session
        message = req.get("message", "test message")
        session_id = req.get("session_id", "debug-session")
        
        # Try to import and initialize only the RouterAgent
        from agents import RouterAgent
        router = RouterAgent()
        
        # Try to determine the route
        route = await router.determine_route(
            message=message,
            has_image=False,
            session_id=session_id
        )
        
        # Return diagnostics
        return {
            "status": "success",
            "router_response": route,
            "message": message,
            "session_id": session_id
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    try:
        # Check memory store functionality
        memory_store = get_memory_store()
        sessions = memory_store.list_sessions()
        
        return {
            "status": "ok",
            "timestamp": datetime.datetime.now().isoformat(),
            "session_count": len(sessions),
            "memory_store_initialized": memory_store is not None
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }

if __name__ == "__main__":
    port = 8000
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True) 