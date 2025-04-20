#!/usr/bin/env python3
"""
Simple test for conversation history mechanism.
"""

import os
import uuid
import json
from pathlib import Path

# Define a simple session storage mechanism
def add_to_history(session_id, message, is_user=True):
    """Add a message to the session history."""
    # Ensure directory exists
    os.makedirs("session_memory", exist_ok=True)
    
    # Get or create session file
    session_file = Path(f"session_memory/{session_id}.json")
    
    # Read existing data or create new
    if session_file.exists():
        with open(session_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"messages": []}
    else:
        data = {"messages": []}
    
    # Add new message
    role = "user" if is_user else "assistant"
    data["messages"].append({
        "role": role,
        "content": message
    })
    
    # Save back to file
    with open(session_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return data

def get_history(session_id, max_messages=10):
    """Get formatted conversation history."""
    # Check if session file exists
    session_file = Path(f"session_memory/{session_id}.json")
    if not session_file.exists():
        return ""
    
    # Read data
    with open(session_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return ""
    
    # Format history
    messages = data.get("messages", [])
    if not messages:
        return ""
    
    # Limit number of messages if needed
    if max_messages > 0:
        messages = messages[-max_messages:]
    
    # Format history
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

def main():
    """Run the test."""
    # Create a unique session ID
    session_id = str(uuid.uuid4())
    print(f"Testing with session ID: {session_id}")
    
    # Add some messages
    print("Adding messages to history...")
    add_to_history(session_id, "Hello, I have a question about a brick wall.", is_user=True)
    add_to_history(session_id, "I can help with that. What's your question?", is_user=False)
    add_to_history(session_id, "The wall has some damaged bricks, see the image.", is_user=True)
    add_to_history(session_id, "I can see the damaged brick wall. It looks like mortar deterioration.", is_user=False)
    
    # Get and display history
    history = get_history(session_id)
    print("\nFormatted History:")
    print(history)
    
    # Simulate a new message with history
    new_message = "What's wrong with the wall?"
    enhanced_message = f"{history}Current message: {new_message}"
    
    print("\nEnhanced message with history:")
    print(enhanced_message)
    
    # Clean up after test
    try:
        os.remove(f"session_memory/{session_id}.json")
        print(f"\nCleaned up test session: {session_id}")
    except Exception as e:
        print(f"Error cleaning up: {str(e)}")

if __name__ == "__main__":
    main() 