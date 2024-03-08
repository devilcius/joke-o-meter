import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Get Jokometians ranking
export const fetchJokometiansRanking = async (id) => {
  try {
    return await axios.get(`${API_BASE_URL}/jokometian-rankings/`);
  } catch (error) {
    return error.response;
  }
};