import React, { useState, useRef, useEffect } from 'react';
import AgentSelector from './components/AgentSelector';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import chatApi from './api/chatApi';
import './index.css';

const BOT_NAME = 'Loopot';

function App() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      message: `Welcome to **Loopot Real Estate Assistant**! I have two specialized agents to help you:\n\n1. **Issue Detection & Troubleshooting Agent:** Upload images of property issues for analysis and troubleshooting advice.\n2. **Tenancy FAQ Agent:** Get answers about rental agreements, tenant rights, and landlord responsibilities.\n\n*How can I assist you today?*`,
      agent: null,
      imageUrl: null,
    },
  ]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message, location) => {
    if (!message.trim()) return;
    setIsLoading(true);
    setMessages((msgs) => [
      ...msgs,
      { sender: 'user', message, agent: selectedAgent, imageUrl: null },
    ]);
    try {
      const response = await chatApi.sendMessage(message, sessionId, location);
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', message: response.response, agent: response.agent, imageUrl: response.image_url || null },
      ]);
    } catch (e) {
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', message: 'Sorry, something went wrong.', agent: selectedAgent, imageUrl: null },
      ]);
    }
    setIsLoading(false);
  };

  const handleSendMessageWithImage = async (message, image, location) => {
    setIsLoading(true);
    setMessages((msgs) => [
      ...msgs,
      { sender: 'user', message, agent: selectedAgent, imageUrl: URL.createObjectURL(image) },
    ]);
    try {
      const response = await chatApi.sendMessageWithImage(message, image, sessionId, location);
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', message: response.response, agent: response.agent, imageUrl: response.image_url || null },
      ]);
    } catch (e) {
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', message: 'Sorry, something went wrong.', agent: selectedAgent, imageUrl: null },
      ]);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--background-color)' }}>
      <header className="flex items-center px-6 py-4" style={{ background: 'var(--header-bg)' }}>
        <img src="/logo.svg" alt="Loopot Logo" className="w-10 h-10 mr-3 rounded-lg" />
        <h1 className="text-2xl font-bold tracking-tight" style={{ color: 'var(--primary-color)' }}>Loopot Real Estate Assistant</h1>
      </header>
      <main className="flex-1 flex flex-col items-center justify-start py-6 px-2">
        <div className="w-full max-w-2xl">
          <AgentSelector selectedAgent={selectedAgent} onAgentSelect={setSelectedAgent} />
          <div className="rounded-xl p-4 mb-4 min-h-[350px] flex flex-col" style={{ background: 'var(--card-bg)', border: '1px solid var(--bubble-border)' }}>
            {messages.map((msg, idx) => (
              <ChatMessage
                key={idx}
                message={msg.message}
                isUser={msg.sender === 'user'}
                agent={msg.agent}
                imageUrl={msg.imageUrl}
              />
            ))}
            <div ref={chatEndRef} />
          </div>
          <div className="rounded-xl p-3 mt-2" style={{ background: 'var(--input-bg)', border: '1px solid var(--input-border)' }}>
            <ChatInput
              onSendMessage={handleSendMessage}
              onSendMessageWithImage={handleSendMessageWithImage}
              isLoading={isLoading}
            />
          </div>
        </div>
      </main>
      <footer className="w-full text-center py-4 text-sm border-t" style={{ background: 'var(--footer-bg)', color: 'var(--primary-color)' }}>
        &copy; {new Date().getFullYear()} <b>Loopot</b> Real Estate Assistant
      </footer>
    </div>
  );
}

export default App; 