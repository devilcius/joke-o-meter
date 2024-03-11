import { axiosInstance, API_BASE_URL} from './axios_instance';

// Get Jokometian by id
export const fetchJokometian = async (id) => {
  try {
    return await axiosInstance.get(`${API_BASE_URL}/jokometians/${id}/`);
  } catch (error) {
    return error.response;
  }
};