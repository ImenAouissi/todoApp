import api from './api';
import toast from 'react-hot-toast';

class AuthService {
  async register(name, email, password) {
    try {
      const response = await api.post('/users/register', {
        name,
        email,
        password
      });

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      toast.success('Inscription réussie !');
      return response.data;
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur lors de l\'inscription';
      toast.error(message);
      throw error;
    }
  }

  async login(email, password) {
    try {
      const response = await api.post('/users/login', {
        email,
        password
      });

      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      toast.success('Connexion réussie !');
      return response.data;
    } catch (error) {
      const message = error.response?.data?.error || 'Erreur de connexion';
      toast.error(message);
      throw error;
    }
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    toast.success('Déconnexion réussie');
  }

  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  }

  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  updateAccessToken(token) {
    localStorage.setItem('access_token', token);
  }

  isAuthenticated() {
    return !!this.getAccessToken();
  }
}

export const authService = new AuthService();