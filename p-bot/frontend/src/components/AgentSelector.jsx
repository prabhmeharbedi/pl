import React, { useState, useEffect } from 'react';
import { FiTool, FiMessageCircle, FiRefreshCw } from 'react-icons/fi';
import chatApi from '../api/chatApi';
import axios from 'axios';

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
      // Try with direct Axios call to bypass any issues with the chatApi abstraction
      const response = await axios.get('/api/v1/agents');
      console.log("Agents response:", response.data);
      if (response.data && response.data.agents) {
        setAgents(response.data.agents);
        setError(null);
      } else {
        setError('Received invalid response format from agents endpoint');
        console.error('Invalid response format:', response.data);
      }
    } catch (err) {
      console.error('Error fetching agents:', err);
      setError('Failed to load available agents: ' + (err.message || 'Unknown error'));
      // Try to access the diagnostic endpoint
      try {
        const statusResponse = await axios.get('/api-status');
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
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Default agents if API fetch fails */}
        {(agents.length === 0 && !loading) ? (
          <>
            <div
              className={`border rounded-lg p-3 cursor-pointer transition-colors
                ${selectedAgent === 'issue_detection' 
                  ? 'border-issue-agent bg-issue-agent-light' 
                  : 'border-gray-200 hover:border-blue-300'}`}
              onClick={() => onAgentSelect('issue_detection')}
            >
              <div className="flex items-center mb-2">
                <div className="w-8 h-8 rounded-full flex items-center justify-center bg-issue-agent text-white mr-2">
                  <FiTool className="w-5 h-5" />
                </div>
                <div className="font-medium">Issue Detection & Troubleshooting Agent</div>
              </div>
              <p className="text-sm text-gray-600">Analyzes property images and descriptions to identify issues and provide troubleshooting advice.</p>
            </div>
            
            <div
              className={`border rounded-lg p-3 cursor-pointer transition-colors
                ${selectedAgent === 'tenancy_faq' 
                  ? 'border-tenancy-agent bg-tenancy-agent-light' 
                  : 'border-gray-200 hover:border-blue-300'}`}
              onClick={() => onAgentSelect('tenancy_faq')}
            >
              <div className="flex items-center mb-2">
                <div className="w-8 h-8 rounded-full flex items-center justify-center bg-tenancy-agent text-white mr-2">
                  <FiMessageCircle className="w-5 h-5" />
                </div>
                <div className="font-medium">Tenancy FAQ Agent</div>
              </div>
              <p className="text-sm text-gray-600">Answers questions about tenancy laws, rental agreements, and landlord/tenant responsibilities.</p>
            </div>
          </>
        ) : (
          agents.map((agent) => (
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
          ))
        )}
      </div>
    </div>
  );
};

export default AgentSelector; 