#!/usr/bin/env python3
"""
Test script for checking basic backend functionality.
"""

import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"Error testing health check: {str(e)}")
        return None

def test_chat_endpoint():
    """Test the chat endpoint with conversation history."""
    print("\nTesting chat endpoint...")
    
    # Create a session ID
    session_id = str(uuid.uuid4())
    print(f"Using session ID: {session_id}")
    
    # Send first message
    try:
        print("Sending first message...")
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": "I have a question about a damaged wall in my property",
                "session_id": session_id,
                "streaming": False
            }
        )
        response.raise_for_status()
        data = response.json()
        print(f"Response from first message:\n{data['response']}\n")
        
        # Wait a moment
        time.sleep(1)
        
        # Send second message
        print("Sending second message...")
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "message": "What might cause the damage?",
                "session_id": session_id,
                "streaming": False
            }
        )
        response.raise_for_status()
        data = response.json()
        print(f"Response from second message:\n{data['response']}\n")
        
        return True
    except Exception as e:
        print(f"Error testing chat endpoint: {str(e)}")
        if hasattr(e, "response") and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return False

def test_sessions_endpoint():
    """Test the sessions endpoint."""
    print("\nTesting sessions endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sessions")
        response.raise_for_status()
        data = response.json()
        print(f"Found {len(data)} sessions:")
        for session in data:
            print(f"- Session ID: {session['session_id']}, Messages: {session['message_count']}")
        return data
    except Exception as e:
        print(f"Error testing sessions endpoint: {str(e)}")
        return None

def main():
    """Run all tests."""
    # Test health check
    health_data = test_health_check()
    if not health_data or health_data.get("status") != "ok":
        print("Health check failed!")
        return
    
    # Test chat endpoint
    chat_success = test_chat_endpoint()
    if not chat_success:
        print("Chat endpoint test failed!")
    
    # Test sessions endpoint
    sessions_data = test_sessions_endpoint()
    if sessions_data is None:
        print("Sessions endpoint test failed!")

if __name__ == "__main__":
    main() 