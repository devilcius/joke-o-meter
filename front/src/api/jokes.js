import { axiosInstance, API_BASE_URL} from './axios_instance';

// Get all jokes
export const fetchJokes = async () => {
  try {

    return await axiosInstance.get(`${API_BASE_URL}/jokes/`);
  } catch (error) {

    return error.response;
  }
};

// Post joke batch
export const postJokes = async (jokes) => {
  try {
    return await axiosInstance.post(`${API_BASE_URL}/evaluate-jokes/`, jokes);
  } catch (error) {
    return error.response;
  }
};
