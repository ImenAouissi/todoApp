from app.extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime

class User:
    collection = mongo.db.users

    @staticmethod
    def create_user(name, email, password):
        """Créer un nouvel utilisateur"""
        # Vérifier si l'email existe déjà
        if User.collection.find_one({'email': email}):
            return None
        
        # Hasher le mot de passe
        hashed_password = generate_password_hash(password)
        
        # Créer l'utilisateur
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'createdAt': datetime.utcnow()
        }
        
        result = User.collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        
        # Ne pas retourner le mot de passe
        del user_data['password']
        return user_data

    @staticmethod
    def find_by_email(email):
        """Trouver un utilisateur par son email"""
        return User.collection.find_one({'email': email})

    @staticmethod
    def find_by_id(user_id):
        """Trouver un utilisateur par son ID"""
        try:
            return User.collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None

    @staticmethod
    def verify_password(user, password):
        """Vérifier le mot de passe"""
        return check_password_hash(user['password'], password)