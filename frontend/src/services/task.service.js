import api from './api';
import toast from 'react-hot-toast';

class TaskService {
  async getAllTasks() {
    try {
      const response = await api.get('/tasks/');
      console.log('API Response getAllTasks:', response.data);
      return response.data;
    } catch (error) {
      console.error('API Error getAllTasks:', error);
      const message = error.response?.data?.error || 'Erreur lors du chargement des tâches';
      toast.error(message);
      throw error;
    }
  }

  async createTask(taskData) {
    try {
      const response = await api.post('/tasks/', taskData);
      console.log('API Response createTask:', response.data);
      toast.success('Tâche créée avec succès !');
      return response.data;
    } catch (error) {
      console.error('API Error createTask:', error);
      const message = error.response?.data?.error || 'Erreur lors de la création';
      toast.error(message);
      throw error;
    }
  }

  async updateTask(id, taskData) {
    try {
      console.log('updateTask appelé avec ID:', id);
      console.log('updateTask données:', taskData);
      
      if (!id) {
        throw new Error('ID de tâche manquant');
      }

      const response = await api.put(`/tasks/${id}`, taskData);
      console.log('API Response updateTask:', response.data);
      toast.success('Tâche mise à jour avec succès !');
      return response.data;
    } catch (error) {
      console.error('API Error updateTask:', error);
      const message = error.response?.data?.error || 'Erreur lors de la mise à jour';
      toast.error(message);
      throw error;
    }
  }

  async deleteTask(id) {
    try {
      console.log('deleteTask appelé avec ID:', id);
      
      if (!id) {
        throw new Error('ID de tâche manquant');
      }

      await api.delete(`/tasks/${id}`);
      console.log('API Response deleteTask: OK');
      toast.success('Tâche supprimée avec succès !');
    } catch (error) {
      console.error('API Error deleteTask:', error);
      const message = error.response?.data?.error || 'Erreur lors de la suppression';
      toast.error(message);
      throw error;
    }
  }

  async getTaskById(id) {
    try {
      const response = await api.get(`/tasks/${id}`);
      return response.data;
    } catch (error) {
      const message = error.response?.data?.error || 'Tâche non trouvée';
      toast.error(message);
      throw error;
    }
  }
}

export const taskService = new TaskService();