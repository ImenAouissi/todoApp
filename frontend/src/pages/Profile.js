import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const Profile = () => {
  const { user } = useAuth();

  const formatDate = (dateString) => {
    if (!dateString) return 'Non disponible';
    try {
      return format(new Date(dateString), 'dd MMMM yyyy à HH:mm', { locale: fr });
    } catch {
      return 'Date invalide';
    }
  };

  return (
    <div className="container" style={{ padding: '2rem 0' }}>
      <div className="auth-card" style={{ maxWidth: '600px', margin: '0 auto' }}>
        <h1 className="auth-title">Mon Profil</h1>
        
        <div style={{ marginBottom: '2rem' }}>
          <div className="form-group">
            <label>Nom</label>
            <input
              type="text"
              value={user?.name || ''}
              readOnly
              style={{ backgroundColor: '#f3f4f6' }}
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={user?.email || ''}
              readOnly
              style={{ backgroundColor: '#f3f4f6' }}
            />
          </div>

          <div className="form-group">
            <label>Membre depuis</label>
            <input
              type="text"
              value={formatDate(user?.createdAt)}
              readOnly
              style={{ backgroundColor: '#f3f4f6' }}
            />
          </div>
        </div>

        <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Statistiques</h3>
          <p>Cette section sera bientôt disponible...</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;