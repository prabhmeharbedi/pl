import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
import io
from PIL import Image
import os
import traceback

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat
from agno.media import Image as AgnoImage

from .base_agent import BaseAgent
from config import ISSUE_DETECTION_AGENT, UPLOAD_DIR

class IssueDetectionAgent(BaseAgent):
    """Agent that can detect issues in property images and provide troubleshooting advice."""
    
    def __init__(self):
        # Set up additional tools for this agent
        tools = [
            DuckDuckGoTools(),  # For searching information about property issues
        ]
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
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
            print(f"Processing image at path: {image_path}")
            
            # Encode the image as base64
            img_path = Path(image_path)
            if not img_path.exists():
                print(f"Image file does not exist: {image_path}")
                return {
                    "agent": self.name,
                    "response": "I couldn't process the image. The file appears to be missing.",
                    "session_id": session_id or "default",
                    "model": self.model_id,
                }
            
            # Open and resize the image if needed (to reduce token usage)
            with Image.open(img_path) as img:
                print(f"Opened image: {img.format}, size: {img.size}, mode: {img.mode}")
                
                # Resize if the image is too large
                max_size = 1024
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.LANCZOS)
                    print(f"Resized image to: {new_size}")
                
                # Convert RGBA to RGB if needed (JPEG doesn't support alpha channel)
                if img.mode == 'RGBA':
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    # Paste the image using alpha as mask
                    background.paste(img, mask=img.split()[3])
                    img = background
                    print("Converted RGBA to RGB")
                elif img.mode != 'RGB':
                    # Convert any other mode to RGB
                    img = img.convert('RGB')
                    print(f"Converted {img.mode} to RGB")
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=90)
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                print(f"Encoded image to base64, length: {len(img_base64)}")
            
            # Create a message with the image
            formatted_message = f"{message}\n\nI'm sharing an image of the property issue."
            
            # Create an Agno Image object with the base64 data
            image_data_uri = f"data:image/jpeg;base64,{img_base64}"
            image = AgnoImage(url=image_data_uri)
            
            print(f"Sending image to processing")
            
            # Process with the base agent's method, passing the proper Agno Image object
            return await super().process(
                message=formatted_message, 
                session_id=session_id,
                images=[image]
            )
            
        except Exception as e:
            error_traceback = traceback.format_exc()
            print(f"Error processing image: {str(e)}\n{error_traceback}")
            
            return {
                "agent": self.name,
                "response": f"I encountered an error processing the image: {str(e)}. Please try again with a different image or provide a detailed description of the issue instead.",
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