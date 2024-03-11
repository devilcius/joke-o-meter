// src/api/axiosInstance.js
import axios from 'axios';
import i18n from '../i18n';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

// Setting the Accept-Language header globally
axiosInstance.interceptors.request.use((config) => {
  config.headers['Accept-Language'] = i18n.language;
  return config;
});

export default axiosInstance;
