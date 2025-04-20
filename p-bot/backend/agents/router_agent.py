from typing import Dict, List, Optional, Any, Literal, Union

from .base_agent import BaseAgent
from config import ROUTER_AGENT

class RouterAgent(BaseAgent):
    """Agent that routes user queries to the appropriate specialized agent."""
    
    def __init__(self):
        # Initialize the base agent
        super().__init__(
            name=ROUTER_AGENT["name"],
            description=ROUTER_AGENT["description"],
            model_id=ROUTER_AGENT["model"],
            instructions=ROUTER_AGENT["instructions"],
            use_reasoning=True,
        )
    
    async def determine_route(
        self, 
        message: str, 
        has_image: bool = False,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Determine which agent should handle this query.
        
        Args:
            message: The user message
            has_image: Whether the request includes an image
            session_id: Optional session ID for memory continuity
            
        Returns:
            A dictionary containing the routing decision and explanation
        """
        # If the message has an image, route to the issue detection agent
        if has_image:
            return {
                "agent": "issue_detection",
                "confidence": 1.0,
                "explanation": "Query includes an image, routing to Issue Detection Agent",
            }
        
        # Create a context with the routing task
        routing_context = {
            "task": "routing",
            "options": ["issue_detection", "tenancy_faq"],
        }
        
        # Prepare a message for the router to classify
        routing_message = (
            f"I need to decide which specialist agent should handle this query: '{message}'\n\n"
            "Options:\n"
            "1. issue_detection - For property damage, maintenance issues, troubleshooting\n"
            "2. tenancy_faq - For tenancy laws, rental agreements, tenant rights, landlord responsibilities\n\n"
            "Reply ONLY with the name of the agent that should handle this query (issue_detection or tenancy_faq) "
            "followed by a brief explanation of why."
        )
        
        try:
            # Get response from the router agent
            response = await super().process(routing_message, session_id, **routing_context)
            
            # Extract the text content from the response
            response_text = ""
            if isinstance(response, dict) and "response" in response:
                response_text = response["response"]
            elif hasattr(response, "content") and response.content:
                response_text = response.content
            elif hasattr(response, "response") and response.response:
                response_text = response.response
            else:
                response_text = str(response)
            
            # Make sure we have a string
            if not isinstance(response_text, str):
                response_text = str(response_text)
                
            # Convert to lowercase for easier matching
            response_text = response_text.lower()
            
            # Check which agent is mentioned first in the response
            if "issue_detection" in response_text and "tenancy_faq" in response_text:
                # Both are mentioned, check which comes first
                idx_issue = response_text.find("issue_detection")
                idx_tenancy = response_text.find("tenancy_faq")
                
                if idx_issue < idx_tenancy and idx_issue != -1:
                    target_agent = "issue_detection"
                else:
                    target_agent = "tenancy_faq"
            elif "issue_detection" in response_text:
                target_agent = "issue_detection"
            elif "tenancy_faq" in response_text or "tenancy" in response_text:
                target_agent = "tenancy_faq"
            else:
                # Default to the issue detection agent if unclear
                target_agent = "issue_detection"
            
            # Extract the explanation from the response
            explanation_parts = response_text.split(target_agent, 1)
            explanation = explanation_parts[1].strip() if len(explanation_parts) > 1 else "Based on query content"
            
            # Clean up explanation
            explanation = explanation.lstrip(" -:.")
            
            return {
                "agent": target_agent,
                "confidence": 0.9,  # We're fairly confident in the router's decision
                "explanation": explanation
            }
        
        except Exception as e:
            print(f"Error in router: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Default to issue detection as fallback
            return {
                "agent": "issue_detection",
                "confidence": 0.5,
                "explanation": "Defaulting to Issue Detection Agent due to routing error"
            } 