import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">
          TodoApp
        </Link>
        <div className="navbar-menu">
          {user ? (
            <>
              <Link to="/dashboard" className="navbar-item">
                Tableau de bord
              </Link>
              <Link to="/profile" className="navbar-item">
                Profil
              </Link>
              <span className="navbar-item">
                Bonjour, {user.name}
              </span>
              <button onClick={handleLogout} className="btn-logout">
                Déconnexion
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-item">
                Connexion
              </Link>
              <Link to="/register" className="navbar-item">
                Inscription
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;