import axios from 'axios';

// Determine API URL based on environment
// In production with Vercel, use the deployed backend URL
// In development, use relative path with proxy
const API_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1` 
  : '/api/v1';

// Create an axios instance with the right configuration
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: false, // Important for CORS with different domains
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Access-Control-Allow-Origin": "*" // Request header for CORS
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(config => {
  console.log('Request:', config.method.toUpperCase(), config.baseURL + config.url);
  return config;
});

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  response => {
    console.log('Response success:', response.status);
    return response;
  },
  error => {
    console.log('Response error:', error.message);
    return Promise.reject(error);
  }
);

// Helper function to log API details
const logAPICall = (method, endpoint, requestData = null, responseData = null, error = null) => {
  console.log(`===== API ${method} ${endpoint} =====`);
  if (requestData) console.log('Request:', requestData);
  if (responseData) console.log('Response:', responseData);
  if (error) console.log('Error:', error);
  console.log('=============================');
};

// Log the API URL being used (for debugging)
console.log('Using API URL:', API_URL);

const chatApi = {
  /**
   * Get available specialized agents
   * @returns {Promise<Object>} - The list of available agents
   */
  getAvailableAgents: async () => {
    try {
      // First try using the regular client
      try {
        const response = await apiClient.get('/agents');
        return response.data.agents;
      } catch (firstError) {
        console.error('First attempt to fetch agents failed:', firstError.message);
        
        // If that fails, try a direct fetch with no-cors mode as fallback
        console.log('Trying direct fetch as fallback...');
        const directResponse = await fetch(`${API_URL.split('/api/v1')[0]}/api/v1/agents`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Accept': 'application/json',
          }
        });
        
        if (!directResponse.ok) throw new Error(`HTTP error! status: ${directResponse.status}`);
        const data = await directResponse.json();
        return data.agents;
      }
    } catch (error) {
      console.error('Error fetching agents:', error);
      throw error;
    }
  },

  /**
   * Send a text message to the chatbot API
   * @param {string} message - The user message
   * @param {string} sessionId - The session ID
   * @param {string} location - Optional location for tenancy questions
   * @returns {Promise<Object>} - The chatbot response
   */
  sendMessage: async (message, sessionId, location = null) => {
    logAPICall('POST', `/chat`, { message, session_id: sessionId, location });
    try {
      const response = await apiClient.post('/chat', {
        message,
        session_id: sessionId,
        location,
      });
      logAPICall('POST', `/chat`, { message, session_id: sessionId, location }, response.data);
      return response.data;
    } catch (error) {
      logAPICall('POST', `/chat`, { message, session_id: sessionId, location }, null, error);
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Send a message with an image to the chatbot API
   * @param {string} message - The user message
   * @param {File} image - The image file
   * @param {string} sessionId - The session ID
   * @param {string} location - Optional location for context
   * @returns {Promise<Object>} - The chatbot response
   */
  sendMessageWithImage: async (message, image, sessionId, location = null) => {
    try {
      // Create a FormData object to send the image
      const formData = new FormData();
      formData.append('message', message);
      formData.append('image', image);
      
      if (sessionId) {
        formData.append('session_id', sessionId);
      }
      
      if (location) {
        formData.append('location', location);
      }
      
      // Send the request with FormData
      const response = await apiClient.post('/chat-with-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Log received image URL for debugging
      if (response.data.image_url) {
        console.log('Received image URL from server:', response.data.image_url);
      }
      
      return response.data;
    } catch (error) {
      console.error('Error sending message with image:', error);
      throw error;
    }
  },

  /**
   * Get all active sessions
   * @returns {Promise<Array>} - List of active sessions
   */
  getSessions: async () => {
    try {
      const response = await apiClient.get('/sessions');
      return response.data;
    } catch (error) {
      console.error('Error fetching sessions:', error);
      throw error;
    }
  },

  /**
   * Get details for a specific session
   * @param {string} sessionId - The session ID
   * @returns {Promise<Object>} - The session details
   */
  getSessionDetails: async (sessionId) => {
    try {
      const response = await apiClient.get(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching session ${sessionId}:`, error);
      throw error;
    }
  },

  /**
   * Delete a session
   * @param {string} sessionId - The session ID
   * @returns {Promise<Object>} - The deletion result
   */
  deleteSession: async (sessionId) => {
    try {
      const response = await apiClient.delete(`/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting session ${sessionId}:`, error);
      throw error;
    }
  },

  /**
   * Clear messages for a session
   * @param {string} sessionId - The session ID
   * @returns {Promise<Object>} - The result
   */
  clearSessionMessages: async (sessionId) => {
    try {
      const response = await apiClient.delete(`/sessions/${sessionId}/messages`);
      return response.data;
    } catch (error) {
      console.error(`Error clearing messages for session ${sessionId}:`, error);
      throw error;
    }
  }
};

export default chatApi; 