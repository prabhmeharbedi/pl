import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import AgentSelector from './components/AgentSelector';
import chatApi from './api/chatApi';
import { FiHome } from 'react-icons/fi';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [selectedAgent, setSelectedAgent] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Generate a session ID when the component mounts
    setSessionId(uuidv4());
    
    // Add welcome message
    setMessages([
      {
        text: "Welcome to P-Bot Real Estate Assistant! I have two specialized agents to help you:\n\n" +
              "1. **Issue Detection & Troubleshooting Agent**: Upload images of property issues for analysis and troubleshooting advice.\n\n" +
              "2. **Tenancy FAQ Agent**: Get answers about rental agreements, tenant rights, and landlord responsibilities.\n\n" +
              "How can I assist you today?",
        isUser: false,
        agent: "router",
        router: { explanation: "Welcome message" }
      },
    ]);
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message, location = null) => {
    if (!message.trim()) return;

    // Add user message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, isUser: true },
    ]);
    
    // Start loading state
    setIsLoading(true);
    
    try {
      // Send message to API
      const response = await chatApi.sendMessage(message, sessionId, location);
      
      // Add bot response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: response.response, 
          isUser: false, 
          agent: response.agent,
          router: response.router
        },
      ]);
      
      // Update the selected agent based on the response
      if (response.agent && !selectedAgent) {
        setSelectedAgent(response.agent);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: "I'm sorry, I encountered an error. Please try again later.", 
          isUser: false,
          agent: "router",
          router: { explanation: "Error response" }
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessageWithImage = async (message, image, location = null) => {
    if (!message.trim() || !image) return;

    // Add user message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { 
        text: message + "\n\n*[Image attached]*", 
        isUser: true 
      },
    ]);
    
    // Start loading state
    setIsLoading(true);
    
    try {
      // Send message with image to API
      const response = await chatApi.sendMessageWithImage(message, image, sessionId, location);
      
      // Add bot response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: response.response, 
          isUser: false, 
          agent: response.agent,
          router: response.router
        },
      ]);
      
      // Update the selected agent to issue detection
      setSelectedAgent('issue_detection');
    } catch (error) {
      console.error('Error sending message with image:', error);
      
      // Add error message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: "I'm sorry, I encountered an error processing your image. Please try again with a different image or send a text-only query.", 
          isUser: false,
          agent: "issue_detection",
          router: { explanation: "Error processing image" }
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAgentSelect = (agentId) => {
    setSelectedAgent(agentId);
    
    // Add a message about the selected agent
    let agentMessage = "";
    
    if (agentId === 'issue_detection') {
      agentMessage = "You've selected the **Issue Detection & Troubleshooting Agent**. I can help identify property issues from images and provide solutions. Feel free to upload an image of the issue you're facing.";
    } else if (agentId === 'tenancy_faq') {
      agentMessage = "You've selected the **Tenancy FAQ Agent**. I can answer questions about rental agreements, tenant rights, and landlord responsibilities. For more accurate answers, consider providing your location.";
    }
    
    if (agentMessage) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: agentMessage, 
          isUser: false, 
          agent: agentId,
          router: { explanation: "Agent selection" }
        },
      ]);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-md">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <FiHome className="mr-2 h-6 w-6" />
            <h1 className="text-2xl font-bold">P-Bot Real Estate Assistant</h1>
          </div>
          <p className="text-sm bg-white bg-opacity-20 px-3 py-1 rounded-full">
            Session ID: {sessionId.slice(0, 8)}
          </p>
        </div>
      </header>
      
      <main className="container mx-auto flex-1 p-4 flex flex-col">
        <div className="bg-white rounded-lg shadow-md p-4 mb-4">
          <AgentSelector onAgentSelect={handleAgentSelect} selectedAgent={selectedAgent} />
        </div>
        
        <div className="flex-1 bg-white rounded-lg shadow-md p-4 overflow-y-auto mb-4">
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <ChatMessage 
                key={index} 
                message={msg.text} 
                isUser={msg.isUser}
                agent={msg.agent}
                router={msg.router}
              />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-4">
          <ChatInput 
            onSendMessage={handleSendMessage} 
            onSendMessageWithImage={handleSendMessageWithImage}
            isLoading={isLoading}
          />
        </div>
      </main>
      
      <footer className="bg-gray-800 text-white text-center p-2 text-sm">
        <p>P-Bot Real Estate Assistant © {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App; 