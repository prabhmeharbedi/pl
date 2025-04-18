import React, { useState, useEffect } from 'react';
import chatApi from '../api/chatApi';

const ModelSelector = ({ onModelChange, currentModel }) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const modelsList = await chatApi.getAvailableModels();
        setModels(modelsList);
        setLoading(false);
      } catch (err) {
        setError('Failed to load models');
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  if (loading) {
    return <div className="text-sm text-gray-500">Loading models...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-500">{error}</div>;
  }

  return (
    <div className="mb-4">
      <label htmlFor="model-selector" className="block text-sm font-medium text-gray-700 mb-1">
        Select AI Model
      </label>
      <select
        id="model-selector"
        value={currentModel || (models.length > 0 ? models[0].id : '')}
        onChange={(e) => onModelChange(e.target.value)}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      >
        {models.map((model) => (
          <option key={model.id} value={model.id}>
            {model.provider} - {model.id}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector; 