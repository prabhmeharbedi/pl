import asyncio
from agent import PBot

async def main():
    """Run a simple conversation with P-Bot."""
    # Create the agent
    pbot = PBot(use_reasoning=True, use_search=True)
    
    # Sample questions
    questions = [
        "What is artificial intelligence?",
        "How can AI be used in education?",
        "What are the ethical concerns around AI?",
    ]
    
    # Start a conversation
    session_id = "example-session"
    
    print("Starting conversation with P-Bot...\n")
    
    for question in questions:
        print(f"User: {question}")
        response = await pbot.chat(question, session_id)
        print(f"P-Bot: {response['response']}\n")

if __name__ == "__main__":
    asyncio.run(main()) 