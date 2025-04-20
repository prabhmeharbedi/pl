#!/usr/bin/env python3
"""
Test script for conversation history implementation.
"""

import asyncio
import uuid
from agent_manager import ConversationHistoryManager
from memory_store import get_memory_store

async def test_conversation_history():
    """Test the conversation history implementation."""
    
    # Create a unique session ID for testing
    session_id = str(uuid.uuid4())
    print(f"Testing with session ID: {session_id}")
    
    # Create an instance of ConversationHistoryManager
    history_manager = ConversationHistoryManager()
    
    # Add some test messages
    history_manager.add_message(session_id, "Hello, I have a question about a brick wall.", is_user=True)
    history_manager.add_message(session_id, "I can help with that. What's your question?", is_user=False)
    history_manager.add_message(session_id, "The wall has some damaged bricks, see the image.", is_user=True)
    history_manager.add_message(session_id, "I can see the damaged brick wall. It looks like mortar deterioration.", is_user=False)
    
    # Retrieve and print the formatted history
    formatted_history = history_manager.get_formatted_history(session_id)
    print("\nFormatted History:\n" + formatted_history)
    
    # Check the raw messages in the store
    memory_store = get_memory_store()
    raw_messages = memory_store.get_messages(session_id)
    print("\nRaw messages from store:")
    for msg in raw_messages:
        print(f"- Role: {msg.get('role')}, Content: {msg.get('content')[:30]}...")
    
    # Simulate a new message in the conversation
    new_message = "What's wrong with the wall?"
    enhanced_message = history_manager.get_formatted_history(session_id)
    if enhanced_message:
        enhanced_message = f"{enhanced_message}Current message: {new_message}"
    else:
        enhanced_message = new_message
    
    print(f"\nEnhanced message with history:\n{enhanced_message}")
    
    # Clean up test data
    memory_store.delete_session(session_id)
    print(f"\nCleaned up test session: {session_id}")

if __name__ == "__main__":
    asyncio.run(test_conversation_history()) 