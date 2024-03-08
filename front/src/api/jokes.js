import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
// Get all jokes
export const fetchJokes = async () => {
  try {

    return await axios.get(`${API_BASE_URL}/jokes/`);
  } catch (error) {

    return error.response;
  }
};

// Post joke batch
export const postJokes = async (jokes) => {
  try {
    return await axios.post(`${API_BASE_URL}/evaluate-jokes/`, jokes);
  } catch (error) {
    return error.response;
  }
};
