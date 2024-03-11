import { axiosInstance, API_BASE_URL} from './axios_instance';

// Get Jokometians ranking
export const fetchJokometiansRanking = async (id) => {
  try {
    return await axiosInstance.get(`${API_BASE_URL}/jokometian-rankings/`);
  } catch (error) {
    return error.response;
  }
};