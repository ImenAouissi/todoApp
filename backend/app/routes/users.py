from flask import Blueprint
from app.controllers.user_controller import UserController

users_bp = Blueprint('users', __name__)

# Ajoutez des slashes
users_bp.route('/register', methods=['POST'])(UserController.register)
users_bp.route('/login', methods=['POST'])(UserController.login)
users_bp.route('/profile', methods=['GET'])(UserController.get_profile)
users_bp.route('/refresh', methods=['POST'])(UserController.refresh)