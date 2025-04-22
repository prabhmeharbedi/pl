import React, { useState, useEffect } from 'react';
import { FiTool, FiMessageCircle, FiRefreshCw } from 'react-icons/fi';
import chatApi from '../api/chatApi';
import axios from 'axios';

// Determine API URL based on environment, same as in chatApi.js
const API_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1` 
  : '/api/v1';

// Create an axios instance with the right configuration (same as in chatApi.js)
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: false, // Important for CORS with different domains
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
});

const AgentSelector = ({ onAgentSelect, selectedAgent }) => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [diagnosticInfo, setDiagnosticInfo] = useState(null);
  const [showDiagnostics, setShowDiagnostics] = useState(false);

  const fetchAgents = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching agents...");
      // Use the chatApi method instead of direct axios
      const agents = await chatApi.getAvailableAgents();
      console.log("Agents response:", agents);
      if (agents && agents.length > 0) {
        setAgents(agents);
        setError(null);
      } else {
        setError('Received invalid response format from agents endpoint');
        console.error('Invalid response format:', agents);
      }
    } catch (err) {
      console.error('Error fetching agents:', err);
      setError('Failed to load available agents: ' + (err.message || 'Unknown error'));
      // Try to access the diagnostic endpoint
      try {
        const statusEndpoint = import.meta.env.VITE_API_URL 
          ? `${import.meta.env.VITE_API_URL}/api-status`
          : '/api-status';
        const statusResponse = await apiClient.get(statusEndpoint);
        setDiagnosticInfo(statusResponse.data);
      } catch (statusErr) {
        console.error('Error accessing diagnostic endpoint:', statusErr);
        setDiagnosticInfo({ error: statusErr.message });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  // If there are no agents but we have an error, show default agents
  const shouldShowDefaultAgents = error && (agents.length === 0);

  if (loading) {
    return <div className="text-sm text-gray-500">Loading agents...</div>;
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

  // Default agents to show if API fails
  const defaultAgents = [
    {
      id: 'issue_detection',
      name: 'Issue Detection & Troubleshooting Agent',
      description: 'Analyzes property images and descriptions to identify issues and provide troubleshooting advice.'
    },
    {
      id: 'tenancy_faq',
      name: 'Tenancy FAQ Agent', 
      description: 'Answers questions about tenancy laws, rental agreements, and landlord/tenant responsibilities.'
    }
  ];

  // Use actual agents if available, otherwise use default agents
  const displayAgents = shouldShowDefaultAgents ? defaultAgents : agents;

  return (
    <div className="mb-4">
      <div className="text-sm font-medium text-gray-700 mb-2 flex justify-between items-center">
        <span>Choose a specialized agent:</span>
        <button 
          onClick={() => { fetchAgents(); setShowDiagnostics(!showDiagnostics); }}
          className="text-blue-500 hover:text-blue-700 text-xs flex items-center"
        >
          <FiRefreshCw className="w-3 h-3 mr-1" />
          {loading ? 'Loading...' : 'Retry'}
        </button>
      </div>
      
      {error && (
        <div className="mb-4">
          <div className="text-sm text-red-500 mb-2">{error}</div>
          <button 
            onClick={() => setShowDiagnostics(!showDiagnostics)}
            className="text-xs text-blue-500 hover:underline"
          >
            {showDiagnostics ? 'Hide diagnostics' : 'Show diagnostics'}
          </button>
          
          {showDiagnostics && diagnosticInfo && (
            <div className="mt-2 p-2 bg-gray-100 rounded text-xs">
              <pre className="whitespace-pre-wrap">{JSON.stringify(diagnosticInfo, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
      
      <div className="grid grid-cols-2 gap-2">
        {displayAgents.map((agent) => (
          <button
            key={agent.id}
            onClick={() => onAgentSelect(agent.id)}
            className={`border rounded-xl p-3 text-left transition-all ${
              selectedAgent === agent.id
                ? `bg-${getAgentColor(agent.id)}-100 border-${getAgentColor(agent.id)}-300 text-${getAgentColor(agent.id)}-700`
                : 'bg-white hover:bg-gray-50 border-gray-200'
            }`}
          >
            <div className="flex items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-2 ${
                selectedAgent === agent.id
                  ? `text-${getAgentColor(agent.id)}-500`
                  : 'text-gray-500'
              }`}>
                {getAgentIcon(agent.id)}
              </div>
              <div>
                <div className="font-medium">{agent.name}</div>
                <div className="text-xs text-gray-500">{agent.description}</div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default AgentSelector; 