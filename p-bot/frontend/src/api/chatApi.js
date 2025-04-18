import axios from 'axios';

const API_URL = '/api/v1';

const chatApi = {
  /**
   * Send a text message to the chatbot API
   * @param {string} message - The user message
   * @param {string} sessionId - The session ID
   * @param {string} location - Optional location for tenancy questions
   * @returns {Promise<Object>} - The chatbot response
   */
  sendMessage: async (message, sessionId, location = null) => {
    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message,
        session_id: sessionId,
        location,
      });
      return response.data;
    } catch (error) {
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
  }
};

export default chatApi; 