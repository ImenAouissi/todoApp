import axios from 'axios';
import { authService } from './auth.service';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token aux requêtes
api.interceptors.request.use(
  (config) => {
    const token = authService.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = authService.getRefreshToken();
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/users/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          });
          
          if (response.data.access_token) {
            authService.updateAccessToken(response.data.access_token);
            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
            return api(originalRequest);
          }
        }
      } catch (refreshError) {
        // Si le refresh échoue, déconnecter l'utilisateur
        authService.logout();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;