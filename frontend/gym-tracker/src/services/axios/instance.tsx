import axios, { AxiosInstance } from 'axios';

const axiosClient = (): AxiosInstance => {
    const token = localStorage.getItem('token');

    const defaultOptions = {
    baseURL: 'http://127.0.0.1:8000/',
    headers: {
      'Content-Type': 'application/json',
      'Authorization':  token ? `Token ${token}` : ''
    },
  };

  // Create instance
  const instance = axios.create(defaultOptions);

  return instance;
}

export default axiosClient();
