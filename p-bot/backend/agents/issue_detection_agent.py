import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
import io
from PIL import Image

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat

from .base_agent import BaseAgent
from config import ISSUE_DETECTION_AGENT, UPLOAD_DIR

class IssueDetectionAgent(BaseAgent):
    """Agent that can detect issues in property images and provide troubleshooting advice."""
    
    def __init__(self):
        # Set up additional tools for this agent
        tools = [
            DuckDuckGoTools(),  # For searching information about property issues
        ]
        
        # Initialize the base agent with the vision-capable model
        super().__init__(
            name=ISSUE_DETECTION_AGENT["name"],
            description=ISSUE_DETECTION_AGENT["description"],
            model_id=ISSUE_DETECTION_AGENT["model"],
            instructions=ISSUE_DETECTION_AGENT["instructions"],
            tools=tools,
        )
    
    async def process_with_image(
        self, 
        message: str, 
        image_path: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a user message along with an image.
        
        Args:
            message: The user message
            image_path: Path to the uploaded image
            session_id: Optional session ID for memory continuity
            
        Returns:
            A dictionary containing the response and additional metadata
        """
        try:
            # Encode the image as base64
            img_path = Path(image_path)
            if not img_path.exists():
                return {
                    "agent": self.name,
                    "response": "I couldn't process the image. The file appears to be missing.",
                    "session_id": session_id or "default",
                    "model": self.model_id,
                }
            
            # Open and resize the image if needed (to reduce token usage)
            with Image.open(img_path) as img:
                # Resize if the image is too large
                max_size = 1024
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format=img.format or "JPEG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Create a message with the image
            formatted_message = f"{message}\n\nI'm sharing an image of the property issue."
            
            # Add image to the context
            image_context = {
                "images": [img_base64]
            }
            
            # Process with the base agent's method
            return await super().process(
                message=formatted_message, 
                session_id=session_id,
                **image_context
            )
            
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"I encountered an error processing the image: {str(e)}",
                "session_id": session_id or "default",
                "model": self.model_id,
            }
    
    async def process(self, message: str, session_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Process a text-only message (no image).
        
        Args:
            message: The user message
            session_id: Optional session ID for memory continuity
            
        Returns:
            A dictionary containing the response and additional metadata
        """
        # For text-only messages, we'll use the standard processing method
        return await super().process(message, session_id, **kwargs) 