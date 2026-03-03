import React from 'react';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const TaskCard = ({ task, onEdit, onDelete }) => {
  const getPriorityClass = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'priority-high';
      case 'medium':
        return 'priority-medium';
      case 'low':
        return 'priority-low';
      default:
        return 'priority-medium';
    }
  };

  const getStatusClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return 'status-pending';
      case 'in progress':
        return 'status-progress';
      case 'done':
        return 'status-done';
      default:
        return 'status-pending';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Pas de date';
    try {
      return format(new Date(dateString), 'dd MMM yyyy', { locale: fr });
    } catch {
      return 'Date invalide';
    }
  };

  // Vérifiez que task et task._id existent
  console.log('Task dans TaskCard:', task); // Pour déboguer

  const handleEdit = () => {
    console.log('Édition de la tâche avec ID:', task._id || task.id); // Débogage
    onEdit(task);
  };

  const handleDelete = () => {
    console.log('Suppression de la tâche avec ID:', task._id || task.id); // Débogage
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
      onDelete(task._id || task.id);
    }
  };

  return (
    <div className="task-card">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <span className={`priority-badge ${getPriorityClass(task.priority)}`}>
          {task.priority || 'Medium'}
        </span>
      </div>
      
      <p className="task-description">
        {task.description || 'Aucune description'}
      </p>
      
      <div className="task-footer">
        <span className="task-date">
          📅 {formatDate(task.dueDate)}
        </span>
        <span className={`status-badge ${getStatusClass(task.status)}`}>
          {task.status || 'Pending'}
        </span>
      </div>

      <div className="task-actions">
        <button 
          onClick={handleEdit} 
          className="btn-edit"
        >
          Modifier
        </button>
        <button 
          onClick={handleDelete} 
          className="btn-delete"
        >
          Supprimer
        </button>
      </div>
    </div>
  );
};

export default TaskCard;