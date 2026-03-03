from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.models.user import User

class UserController:
    @staticmethod
    def register():
        """Endpoint d'inscription"""
        try:
            data = request.get_json()
            
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            
            response, status = AuthService.register_user(name, email, password)
            return jsonify(response), status
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def login():
        """Endpoint de connexion"""
        try:
            data = request.get_json()
            
            email = data.get('email')
            password = data.get('password')
            
            response, status = AuthService.login_user(email, password)
            return jsonify(response), status
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def get_profile():
        """Récupérer le profil de l'utilisateur connecté"""
        try:
            current_user_id = get_jwt_identity()
            user = User.find_by_id(current_user_id)
            
            if not user:
                return jsonify({'error': 'Utilisateur non trouvé'}), 404
            
            return jsonify({
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'createdAt': user['createdAt']
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def refresh():
        """Rafraîchir le token"""
        try:
            current_user_id = get_jwt_identity()
            response, status = AuthService.refresh_token(current_user_id)
            return jsonify(response), status
        except Exception as e:
            return jsonify({'error': str(e)}), 500