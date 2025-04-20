import axios from 'axios';

// Use relative path for API URL to work with the proxy configuration
const API_URL = '/api/v1';

// Helper function to log API details
const logAPICall = (method, endpoint, requestData = null, responseData = null, error = null) => {
  console.log(`===== API ${method} ${endpoint} =====`);
  if (requestData) console.log('Request:', requestData);
  if (responseData) console.log('Response:', responseData);
  if (error) console.log('Error:', error);
  console.log('=============================');
};

const chatApi = {
  /**
   * Send a text message to the chatbot API
   * @param {string} message - The user message
   * @param {string} sessionId - The session ID
   * @param {string} location - Optional location for tenancy questions
   * @returns {Promise<Object>} - The chatbot response
   */
  sendMessage: async (message, sessionId, location = null) => {
    logAPICall('POST', `${API_URL}/chat`, { message, session_id: sessionId, location });
    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message,
        session_id: sessionId,
        location,
      });
      logAPICall('POST', `${API_URL}/chat`, { message, session_id: sessionId, location }, response.data);
      return response.data;
    } catch (error) {
      logAPICall('POST', `${API_URL}/chat`, { message, session_id: sessionId, location }, null, error);
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
      const response = await axios.post(`${API_URL}/chat-with-image`, formData, {
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
   * Get available specialized agents
   * @returns {Promise<Object>} - The list of available agents
   */
  getAvailableAgents: async () => {
    try {
      const response = await axios.get(`${API_URL}/agents`);
      return response.data.agents;
    } catch (error) {
      console.error('Error fetching agents:', error);
      throw error;
    }
  },

  /**
   * Get all active sessions
   * @returns {Promise<Array>} - List of active sessions
   */
  getSessions: async () => {
    try {
      const response = await axios.get(`${API_URL}/sessions`);
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
      const response = await axios.get(`${API_URL}/sessions/${sessionId}`);
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
      const response = await axios.delete(`${API_URL}/sessions/${sessionId}`);
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
      const response = await axios.delete(`${API_URL}/sessions/${sessionId}/messages`);
      return response.data;
    } catch (error) {
      console.error(`Error clearing messages for session ${sessionId}:`, error);
      throw error;
    }
  }
};

export default chatApi; 