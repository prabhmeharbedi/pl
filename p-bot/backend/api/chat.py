from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import uuid4

from agent_manager import AgentManager

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

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    agent: str
    model: str
    router: Dict[str, Any]
    tool_calls: List[Dict[str, Any]] = []

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, agent_manager: AgentManager = Depends(get_agent_manager)) -> ChatResponse:
    """Process a text-only chat message and return the response."""
    try:
        # Create a new session ID if none provided
        session_id = req.session_id or str(uuid4())
        
        # Process the query
        result = await agent_manager.process_query(
            message=req.message,
            session_id=session_id,
            location=req.location
        )
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

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
        
        # Process the query with the image
        result = await agent_manager.process_query(
            message=message,
            session_id=session_id,
            image_file=image,
            location=location
        )
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message with image: {str(e)}")

@router.get("/agents")
def get_available_agents():
    """Get the list of available specialized agents."""
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