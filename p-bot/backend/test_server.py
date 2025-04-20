import requests
import json
import os
import sys
from time import sleep

def test_server_connection():
    """Test if the server is running"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print(f"✅ Server is running: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with 'uvicorn main:app --reload'")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a simple message"""
    try:
        data = {
            "message": "What are the typical notice periods for ending a tenancy?",
            "session_id": "test_session"
        }
        response = requests.post("http://localhost:8000/api/v1/chat", json=data)
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Chat endpoint working")
            print(f"Agent: {result['agent']}")
            print(f"Response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat endpoint returned status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {str(e)}")
        return False

def test_agents_endpoint():
    """Test the agents endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/v1/agents")
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Agents endpoint working")
            print(f"Available agents: {', '.join([a['id'] for a in result['agents']])}")
            return True
        else:
            print(f"❌ Agents endpoint returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing agents endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing P-Bot backend server...\n")
    
    # Test server connection
    server_running = test_server_connection()
    if not server_running:
        sys.exit(1)
    
    # Wait a moment before testing endpoints
    sleep(1)
    
    # Test the endpoints
    test_agents_endpoint()
    test_chat_endpoint()
    
    print("\n�� Tests completed.") 