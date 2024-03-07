import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// if debug mode set HTTP_ACCEPT_LANGUAGE header to es
if (process.env.NODE_ENV === 'development') {
  axios.defaults.headers.common['Accept-Language'] = 'es';
}

// Get Jokometian by id
export const fetchJokometian = async (id) => {
  try {
    return await axios.get(`${API_BASE_URL}/jokometians/${id}/`);
  } catch (error) {
    return error.response;
  }
};