import os
import uuid
from typing import Dict, List, Optional, Any
from pathlib import Path

from agents import IssueDetectionAgent, RouterAgent
from config import UPLOAD_DIR, DEFAULT_MODEL, CONTEXT_TURNS, CONTEXT_CHAR_LIMIT
from memory_store import get_memory_store

class ConversationHistoryManager:
    """Manages conversation history for sessions."""
    
    def __init__(self):
        """Initialize the conversation history manager."""
        self.memory_store = get_memory_store()
    
    def get_formatted_history(self, session_id: str, max_messages: int = 5) -> str:
        """Get formatted conversation history for a session.
        
        Args:
            session_id: The session ID to retrieve history for
            max_messages: Maximum number of previous messages to include
            
        Returns:
            A formatted string containing the conversation history
        """
        try:
            # Get messages with a smaller limit to avoid performance issues
            messages = self.memory_store.get_messages(session_id, max_messages)
            if not messages:
                return ""
            
            formatted_history = "\n--- Previous Conversation History ---\n"
            for msg in messages:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if role == "user":
                    formatted_history += f"User: {content}\n"
                elif role == "assistant":
                    formatted_history += f"Assistant: {content}\n"
            formatted_history += "--- End of History ---\n\n"
            
            return formatted_history
        except Exception as e:
            print(f"Error getting conversation history: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return empty history on error to avoid blocking
            return ""
    
    def add_message(self, session_id: str, message: str, is_user: bool = True, image_path: str = None) -> None:
        """Add a message to the conversation history.
        
        Args:
            session_id: The session ID
            message: The message content
            is_user: Whether this is a user message (True) or assistant message (False)
            image_path: Optional image path to associate with this message
        """
        try:
            role = "user" if is_user else "assistant"
            import datetime
            
            # Truncate very long messages to avoid storage issues
            max_message_length = 2000  # Reasonable limit for message length
            if len(message) > max_message_length:
                message = message[:max_message_length] + " [...truncated...]"
            
            msg = {
                "role": role,
                "content": message,
                "timestamp": datetime.datetime.now().isoformat()
            }
            if image_path:
                msg["image_path"] = image_path
            self.memory_store.add_message(session_id, msg)
        except Exception as e:
            print(f"Error adding message to history: {str(e)}")
            import traceback
            traceback.print_exc()

# Import the real TenancyFAQAgent
try:
    from agents import TenancyFAQAgent
    print("Successfully imported TenancyFAQAgent class")
except ImportError as e:
    print(f"Failed to import TenancyFAQAgent: {str(e)}")

class AgentManager:
    """Manager for coordinating multiple specialized agents."""
    
    def __init__(self):
        """Initialize the agent manager with specialized agents."""
        self.router = RouterAgent()
        self.issue_detection = IssueDetectionAgent()
        
        # Always use the real TenancyFAQAgent
        from agents import TenancyFAQAgent
        self.tenancy_faq = TenancyFAQAgent()
        print("Successfully loaded TenancyFAQAgent")
        
        # Dictionary to map agent names to their instances
        self.agents = {
            "router": self.router,
            "issue_detection": self.issue_detection,
            "tenancy_faq": self.tenancy_faq,
        }
        
        # Store the last image path for retrieval
        self.last_image_path = None
        
        # Track active sessions for debugging
        self.active_sessions = set()
        
        # Initialize the conversation history manager
        self.history_manager = ConversationHistoryManager()
    
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
        try:
            # Generate a session ID if none provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Track this session
            self.active_sessions.add(session_id)
            print(f"Processing message for session: {session_id}")
            
            # Handle image upload if provided
            image_path = None
            if image_file:
                print(f"Processing image upload for session: {session_id}")
                # Save the uploaded image
                image_path = await self._save_uploaded_image(image_file, session_id)
                # Store the last image path
                self.last_image_path = image_path
                print(f"Image saved at: {image_path}")
                # Add the user message to conversation history, with image_path
                try:
                    print(f"Adding user message to history for session: {session_id} (with image)")
                    self.history_manager.add_message(session_id, message, is_user=True, image_path=image_path)
                    print(f"Successfully added user message to history (with image)")
                except Exception as history_error:
                    print(f"Error adding message to history: {str(history_error)}")
                    import traceback
                    traceback.print_exc()
            else:
                # Add the user message to conversation history (no image)
                try:
                    print(f"Adding user message to history for session: {session_id}")
                    self.history_manager.add_message(session_id, message, is_user=True)
                    print(f"Successfully added user message to history")
                except Exception as history_error:
                    print(f"Error adding message to history: {str(history_error)}")
                    import traceback
                    traceback.print_exc()
            
            # Get conversation history with a shorter limit and timeout protection
            conversation_history = ""
            try:
                print(f"Getting formatted history for session: {session_id}")
                # Use a smaller limit for history to avoid performance issues
                conversation_history = self.history_manager.get_formatted_history(session_id, max_messages=3)
                print(f"History retrieved, length: {len(conversation_history)}")
            except Exception as history_error:
                print(f"Error getting history: {str(history_error)}")
                conversation_history = ""
                import traceback
                traceback.print_exc()
            
            # Create the enhanced message with conversation history
            # Always include at least the last CONTEXT_TURNS user+assistant turns, or up to CONTEXT_CHAR_LIMIT chars
            history_messages = self.history_manager.memory_store.get_messages(session_id, limit=CONTEXT_TURNS*2)
            history_text = ""
            char_count = 0
            turns = 0
            for msg in reversed(history_messages):
                if msg["role"] == "user":
                    turns += 1
                line = f'{msg["role"].capitalize()}: {msg["content"]}\n'
                if char_count + len(line) > CONTEXT_CHAR_LIMIT and turns >= CONTEXT_TURNS:
                    break
                history_text = line + history_text
                char_count += len(line)
            enhanced_message = f"{history_text}Current message: {message}"
            print(f"Added truncated conversation history to message for session: {session_id}")
            
            # Only set has_image=True if the user just uploaded a new image
            last_image_path = None
            if not image_file:
                # Look for the last image in the session history
                history = self.history_manager.memory_store.get_messages(session_id, limit=10)
                for msg in reversed(history):
                    if msg.get("image_path"):
                        last_image_path = msg["image_path"]
                        break
            # Only set has_image True if this message has a new image
            has_image = bool(image_path)

            print(f"Determining route for message: {message[:50]}...")
            
            # Determine which agent should handle this query
            route = await self.router.determine_route(
                message=enhanced_message,
                has_image=has_image,
                session_id=session_id
            )
            
            target_agent_name = route["agent"]
            explanation = route["explanation"]
            
            print(f"Router determined agent: {target_agent_name}, explanation: {explanation}")
            
        except Exception as router_error:
            # If router fails, default to tenancy_faq for text and issue_detection for images
            print(f"Error in router: {str(router_error)}")
            if image_path:
                target_agent_name = "issue_detection"
                explanation = "Default routing (router error) - image detected"
            else:
                target_agent_name = "tenancy_faq"
                explanation = "Default routing (router error) - text only"
            
            print(f"Falling back to agent: {target_agent_name}")
        
        # Get the target agent
        target_agent = self.agents[target_agent_name]
        
        print(f"Routing to agent '{target_agent_name}' with session_id: {session_id}")
        
        # Process the query with the appropriate agent
        try:
            if target_agent_name == "issue_detection" and (image_path or last_image_path):
                # Process with image for the issue detection agent (pass last image if available)
                response = await self.issue_detection.process_with_image(
                    message=enhanced_message,
                    image_path=image_path or last_image_path,
                    session_id=session_id
                )
            elif target_agent_name == "tenancy_faq" and location:
                # Add location context for the tenancy FAQ agent
                response = await self.tenancy_faq.process(
                    message=enhanced_message,
                    session_id=session_id,
                    location=location
                )
            else:
                # Standard processing for other cases
                response = await target_agent.process(
                    message=enhanced_message,
                    session_id=session_id
                )
                
            # Extract just the response text and normalize it
            print(f"Processing response from agent: {target_agent_name}")
            response_text = ""
            if isinstance(response, dict):
                # If it's a dictionary, try to get the 'response' field
                response_text = response.get("response", str(response))
                print(f"Got dictionary response with keys: {', '.join(response.keys())}")
            elif hasattr(response, 'content'):
                # If it's an object with content attribute
                response_text = response.content
                print(f"Got response object with content attribute")
            elif hasattr(response, 'response'):
                # If it's an object with response attribute
                response_text = response.response
                print(f"Got response object with response attribute")
            else:
                # Fallback to string conversion
                response_text = str(response)
                print(f"Got response of type: {type(response)}")
            
            # Ensure response_text is a string
            if not isinstance(response_text, str):
                response_text = str(response_text)
            
            # Add the assistant's response to conversation history
            try:
                print(f"Adding assistant response to history for session: {session_id}")
                self.history_manager.add_message(session_id, response_text, is_user=False)
                print(f"Successfully added assistant response to history")
            except Exception as history_error:
                print(f"Error adding assistant response to history: {str(history_error)}")
                import traceback
                traceback.print_exc()
            
            # Add routing information to the response
            clean_response = {
                "response": response_text,
                "session_id": session_id,
                "agent": target_agent_name,
                "model": getattr(response, "model", DEFAULT_MODEL),
                "router": {
                    "target_agent": target_agent_name,
                    "explanation": explanation,
                }
            }
            
            # Add tool calls if they exist
            if hasattr(response, "tool_calls") and response.tool_calls:
                clean_response["tool_calls"] = response.tool_calls
            elif isinstance(response, dict) and "tool_calls" in response:
                clean_response["tool_calls"] = response["tool_calls"]
            
            print(f"Successfully processed message for session: {session_id}")
            return clean_response
            
        except Exception as agent_error:
            # Handle agent processing errors
            print(f"Error processing with agent {target_agent_name}: {str(agent_error)}")
            import traceback
            traceback.print_exc()
            
            # Create an error response
            return {
                "response": f"I'm sorry, I encountered an error while processing your request with the {target_agent_name} agent. Please try again later.",
                "session_id": session_id,
                "agent": target_agent_name,
                "model": DEFAULT_MODEL,
                "router": {
                    "target_agent": target_agent_name,
                    "explanation": explanation + " (error occurred)",
                }
            }
    
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