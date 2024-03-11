import axiosInstance from './axios_instance';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Get Jokometian by id
export const fetchJokometian = async (id) => {
  try {
    return await axiosInstance.get(`${API_BASE_URL}/jokometians/${id}/`);
  } catch (error) {
    return error.response;
  }
};