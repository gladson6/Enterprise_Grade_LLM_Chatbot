// import axios from 'axios';

// // The backend API is expected to be running on port 8000
// const API_URL = 'http://127.0.0.1:8000/api/v1';

// const apiClient = axios.create({
//   baseURL: API_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// /**
//  * Sends a chat message to the backend.
//  * @param {string} message - The user's message.
//  * @param {Array} history - The chat history.
//  * @returns {Promise<Object>} - The API response data.
//  */
// export const sendMessage = async (message, history) => {
//   try {
//     const response = await apiClient.post('/chat', {
//       message,
//       history,
//     });
//     return response.data;
//   } catch (error) {
//     console.error('Error sending message:', error.response ? error.response.data : error.message);
//     throw error;
//   }
// };

// /**
//  * Sends lead capture data to the backend.
//  * @param {Object} leadData - The lead's information.
//  * @returns {Promise<Object>} - The API response data.
//  */
// export const sendLead = async (leadData) => {
//   try {
//     const response = await apiClient.post('/lead', leadData);
//     return response.data;
//   } catch (error) {
//     console.error('Error sending lead:', error.response ? error.response.data : error.message);
//     throw error;
//   }
// };

import axios from 'axios';

// The backend API is expected to be running on port 8000
const API_URL = 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Sends a chat message to the backend.
 * @param {string} message - The user's message.
 * @param {Array} history - The chat history.
 * @returns {Promise<Object>} - The API response data.
 */
export const sendMessage = async (message, history) => {
  try {
    // The payload uses { message, history } to match your backend
    const response = await apiClient.post('/chat', {
      question: message, // Assuming backend expects 'question' based on previous context
      history,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error.response ? error.response.data : error.message);
    throw error;
  }
};

/**
 * Sends lead capture data to the backend.
 * @param {Object} leadData - The lead's information (e.g., { name, email, query }).
 * @returns {Promise<Object>} - The API response data.
 */
export const sendLead = async (leadData) => {
  try {
    const response = await apiClient.post('/lead', leadData);
    return response.data;
  } catch (error) {
    console.error('Error sending lead:', error.response ? error.response.data : error.message);
    throw error;
  }
};

