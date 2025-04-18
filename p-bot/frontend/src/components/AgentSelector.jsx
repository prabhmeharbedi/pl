import React, { useState, useEffect } from 'react';
import { FiTool, FiMessageCircle } from 'react-icons/fi';
import chatApi from '../api/chatApi';

const AgentSelector = ({ onAgentSelect, selectedAgent }) => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const agentsList = await chatApi.getAvailableAgents();
        setAgents(agentsList);
        setLoading(false);
      } catch (err) {
        setError('Failed to load available agents');
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  if (loading) {
    return <div className="text-sm text-gray-500">Loading agents...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-500">{error}</div>;
  }

  const getAgentIcon = (agentId) => {
    switch (agentId) {
      case 'issue_detection':
        return <FiTool className="w-5 h-5" />;
      case 'tenancy_faq':
        return <FiMessageCircle className="w-5 h-5" />;
      default:
        return null;
    }
  };

  const getAgentColor = (agentId) => {
    switch (agentId) {
      case 'issue_detection':
        return 'issue-agent';
      case 'tenancy_faq':
        return 'tenancy-agent';
      default:
        return 'gray-500';
    }
  };

  return (
    <div className="mb-4">
      <div className="text-sm font-medium text-gray-700 mb-2">
        Choose a specialized agent:
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className={`border rounded-lg p-3 cursor-pointer transition-colors
              ${selectedAgent === agent.id 
                ? `border-${getAgentColor(agent.id)} bg-${getAgentColor(agent.id)}-light` 
                : 'border-gray-200 hover:border-blue-300'}`}
            onClick={() => onAgentSelect(agent.id)}
          >
            <div className="flex items-center mb-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center bg-${getAgentColor(agent.id)} text-white mr-2`}>
                {getAgentIcon(agent.id)}
              </div>
              <div className="font-medium">{agent.name}</div>
            </div>
            <p className="text-sm text-gray-600">{agent.description}</p>
            
            <div className="mt-2">
              <div className="text-xs text-gray-500 mb-1">Example queries:</div>
              <ul className="text-xs text-gray-600 pl-4 list-disc">
                {agent.examples.slice(0, 2).map((example, index) => (
                  <li key={index}>{example}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentSelector; 