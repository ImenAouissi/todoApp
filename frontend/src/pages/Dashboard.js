import React, { useState, useEffect } from 'react';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';
import { taskService } from '../services/task.service';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      console.log('Chargement des tâches...');
      const data = await taskService.getAllTasks();
      console.log('Tâches chargées:', data);
      setTasks(data);
    } catch (error) {
      console.error('Erreur chargement tâches:', error);
      toast.error('Erreur lors du chargement des tâches');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      console.log('Création tâche avec données:', taskData);
      const newTask = await taskService.createTask(taskData);
      console.log('Tâche créée:', newTask);
      setTasks([...tasks, newTask]);
      setShowModal(false);
      toast.success('Tâche créée avec succès !');
    } catch (error) {
      console.error('Erreur création:', error);
      toast.error('Erreur lors de la création');
    }
  };

  const handleUpdateTask = async (taskData) => {
    try {
      console.log('Mise à jour tâche - selectedTask:', selectedTask);
      console.log('Données de mise à jour:', taskData);
      
      // Vérifier que selectedTask existe et a un ID
      if (!selectedTask || !selectedTask._id) {
        console.error('ID de tâche manquant:', selectedTask);
        toast.error('Erreur: ID de tâche manquant');
        return;
      }

      const taskId = selectedTask._id;
      console.log('Mise à jour tâche ID:', taskId);
      
      const updatedTask = await taskService.updateTask(taskId, taskData);
      console.log('Tâche mise à jour:', updatedTask);
      
      setTasks(tasks.map(t => t._id === taskId ? updatedTask : t));
      setShowModal(false);
      setSelectedTask(null);
      toast.success('Tâche mise à jour avec succès !');
    } catch (error) {
      console.error('Erreur mise à jour:', error);
      toast.error('Erreur lors de la mise à jour');
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      console.log('Suppression tâche ID:', taskId);
      
      if (!taskId) {
        console.error('ID de tâche manquant');
        toast.error('Erreur: ID de tâche manquant');
        return;
      }

      await taskService.deleteTask(taskId);
      console.log('Tâche supprimée avec succès');
      
      setTasks(tasks.filter(t => t._id !== taskId));
      toast.success('Tâche supprimée avec succès !');
    } catch (error) {
      console.error('Erreur suppression:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const handleEditTask = (task) => {
    console.log('Édition tâche - tâche reçue:', task);
    console.log('ID de la tâche à éditer:', task._id);
    setSelectedTask(task);
    setShowModal(true);
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status?.toLowerCase() === filter;
  });

  if (loading) {
    return <div className="loading">Chargement des tâches...</div>;
  }

  return (
    <div className="container dashboard">
      <div className="dashboard-header">
        <h1>Mes tâches</h1>
        <div>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ marginRight: '1rem', padding: '0.5rem' }}
          >
            <option value="all">Toutes</option>
            <option value="pending">En attente</option>
            <option value="in progress">En cours</option>
            <option value="done">Terminées</option>
          </select>
          <button onClick={() => {
            setSelectedTask(null);
            setShowModal(true);
          }} className="btn-add">
            + Nouvelle tâche
          </button>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="empty-state">
          <p>Aucune tâche trouvée</p>
          <button onClick={() => {
            setSelectedTask(null);
            setShowModal(true);
          }} className="btn-primary" style={{ width: 'auto' }}>
            Créer votre première tâche
          </button>
        </div>
      ) : (
        <div className="tasks-grid">
          {filteredTasks.map(task => (
            <TaskCard
              key={task._id || task.id}
              task={task}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
            />
          ))}
        </div>
      )}

      {showModal && (
        <TaskForm
          task={selectedTask}
          onSubmit={selectedTask ? handleUpdateTask : handleCreateTask}
          onClose={() => {
            setShowModal(false);
            setSelectedTask(null);
          }}
        />
      )}
    </div>
  );
};

export default Dashboard;