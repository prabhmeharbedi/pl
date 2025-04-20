import asyncio
import os
import sys
from pathlib import Path

# Add the framework path to PYTHONPATH
framework_path = Path(__file__).resolve().parent.parent.parent / "framework" / "agno" / "libs" / "agno"
sys.path.insert(0, str(framework_path))

# Import required modules
from dotenv import load_dotenv
from agent_manager import AgentManager
from config import DEFAULT_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY

# Load environment variables
load_dotenv()
print(f"OpenAI API Key: {OPENAI_API_KEY[:5]}...")
print(f"Anthropic API Key: {ANTHROPIC_API_KEY[:5]}...")

async def test_chat():
    """Test the chat functionality directly."""
    try:
        # Initialize the agent manager
        print("Initializing agent manager...")
        agent_manager = AgentManager()
        
        # Test a simple chat message
        print("\nSending test message to router agent...")
        message = "Hello, can you help me with a tenancy question?"
        
        try:
            # Process with router agent
            print("Processing with router agent...")
            router_result = await agent_manager.router.determine_route(
                message=message,
                has_image=False,
                session_id="test_session"
            )
            print(f"Router result: {router_result}")
            
            # Get the target agent
            target_agent_name = router_result["agent"]
            target_agent = agent_manager.agents[target_agent_name]
            print(f"Selected target agent: {target_agent_name}")
            
            # Process with target agent
            print(f"Processing with {target_agent_name} agent...")
            response = await target_agent.process(
                message=message,
                session_id="test_session"
            )
            
            print("\nResponse:")
            print(f"Agent: {response.get('agent', 'unknown')}")
            print(f"Response: {response.get('response', '')[:100]}...")
            
        except Exception as e:
            print(f"Error in agent processing: {str(e)}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat()) 