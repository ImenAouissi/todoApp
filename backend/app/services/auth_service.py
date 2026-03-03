from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta, datetime
from app.models.user import User

class AuthService:
    @staticmethod
    def register_user(name, email, password):
        """Service d'inscription"""
        # Validation des données
        if not name or not email or not password:
            return {'error': 'Tous les champs sont requis'}, 400
        
        if len(password) < 6:
            return {'error': 'Le mot de passe doit contenir au moins 6 caractères'}, 400
        
        if '@' not in email or '.' not in email:
            return {'error': 'Email invalide'}, 400
        
        # Créer l'utilisateur
        user = User.create_user(name, email, password)
        
        if not user:
            return {'error': 'Cet email est déjà utilisé'}, 409
        
        # Créer les tokens
        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=str(user['_id'])
        )
        
        return {
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'createdAt': user['createdAt'].isoformat() if isinstance(user['createdAt'], datetime) else user['createdAt']
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201

    @staticmethod
    def login_user(email, password):
        """Service de connexion"""
        if not email or not password:
            return {'error': 'Email et mot de passe requis'}, 400
        
        # Chercher l'utilisateur
        user = User.find_by_email(email)
        
        if not user or not User.verify_password(user, password):
            return {'error': 'Email ou mot de passe incorrect'}, 401
        
        # Créer les tokens
        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=str(user['_id'])
        )
        
        # Ne pas retourner le mot de passe
        user_data = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'createdAt': user['createdAt'].isoformat() if isinstance(user['createdAt'], datetime) else user['createdAt']
        }
        
        return {
            'message': 'Connexion réussie',
            'user': user_data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200

    @staticmethod
    def refresh_token(identity):
        """Rafraîchir le token"""
        new_access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(hours=1)
        )
        
        return {
            'access_token': new_access_token
        }, 200