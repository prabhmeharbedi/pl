import os
import uuid
from typing import Dict, List, Optional, Any
from pathlib import Path

from agents import IssueDetectionAgent, TenancyFAQAgent, RouterAgent
from config import UPLOAD_DIR

class AgentManager:
    """Manager for coordinating multiple specialized agents."""
    
    def __init__(self):
        """Initialize the agent manager with specialized agents."""
        self.router = RouterAgent()
        self.issue_detection = IssueDetectionAgent()
        self.tenancy_faq = TenancyFAQAgent()
        
        # Dictionary to map agent names to their instances
        self.agents = {
            "router": self.router,
            "issue_detection": self.issue_detection,
            "tenancy_faq": self.tenancy_faq,
        }
    
    async def process_query(
        self, 
        message: str,
        session_id: Optional[str] = None,
        image_file = None,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a user query and route it to the appropriate agent.
        
        Args:
            message: The user message
            session_id: Optional session ID for memory continuity
            image_file: Optional uploaded image file
            location: Optional user location for tenancy questions
            
        Returns:
            A dictionary containing the response and metadata
        """
        # Generate a session ID if none provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Handle image upload if provided
        image_path = None
        if image_file:
            # Save the uploaded image
            image_path = await self._save_uploaded_image(image_file, session_id)
        
        # Determine which agent should handle this query
        route = await self.router.determine_route(
            message=message,
            has_image=bool(image_path),
            session_id=session_id
        )
        
        target_agent_name = route["agent"]
        explanation = route["explanation"]
        
        # Get the target agent
        target_agent = self.agents[target_agent_name]
        
        # Process the query with the appropriate agent
        if target_agent_name == "issue_detection" and image_path:
            # Process with image for the issue detection agent
            response = await self.issue_detection.process_with_image(
                message=message,
                image_path=image_path,
                session_id=session_id
            )
        elif target_agent_name == "tenancy_faq" and location:
            # Add location context for the tenancy FAQ agent
            response = await self.tenancy_faq.process(
                message=message,
                session_id=session_id,
                location=location
            )
        else:
            # Standard processing for other cases
            response = await target_agent.process(
                message=message,
                session_id=session_id
            )
        
        # Add routing information to the response
        response.update({
            "router": {
                "target_agent": target_agent_name,
                "explanation": explanation,
            }
        })
        
        return response
    
    async def _save_uploaded_image(self, image_file, session_id: str) -> str:
        """Save an uploaded image to the uploads directory.
        
        Args:
            image_file: The uploaded image file
            session_id: Session ID for organizing uploads
            
        Returns:
            The path to the saved image
        """
        # Create a directory for this session's uploads
        session_dir = UPLOAD_DIR / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Generate a unique filename for the image
        file_ext = Path(image_file.filename).suffix
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = session_dir / filename
        
        # Save the file
        with open(file_path, "wb") as f:
            contents = await image_file.read()
            f.write(contents)
        
        return str(file_path) 