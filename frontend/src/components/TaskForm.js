import React, { useState, useEffect } from 'react';

const TaskForm = ({ task, onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    status: 'pending',
    dueDate: ''
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        priority: task.priority || 'medium',
        status: task.status || 'pending',
        dueDate: task.dueDate ? task.dueDate.split('T')[0] : ''
      });
    }
  }, [task]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{task ? 'Modifier la tâche' : 'Nouvelle tâche'}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Titre *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="Titre de la tâche"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Description (optionnelle)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="priority">Priorité</label>
            <select
              id="priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
            >
              <option value="low">Basse</option>
              <option value="medium">Moyenne</option>
              <option value="high">Haute</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="status">Statut</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="pending">En attente</option>
              <option value="in progress">En cours</option>
              <option value="done">Terminé</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="dueDate">Date limite</label>
            <input
              type="date"
              id="dueDate"
              name="dueDate"
              value={formData.dueDate}
              onChange={handleChange}
            />
          </div>

          <div className="modal-actions">
            <button type="submit" className="btn-primary">
              {task ? 'Mettre à jour' : 'Créer'}
            </button>
            <button type="button" onClick={onClose} className="btn-secondary">
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskForm;