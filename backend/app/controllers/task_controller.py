from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.task_service import TaskService

class TaskController:
    @staticmethod
    @jwt_required()
    def create_task():
        """Créer une nouvelle tâche"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            response, status = TaskService.create_task(current_user_id, data)
            return jsonify(response), status
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def get_all_tasks():
        """Récupérer toutes les tâches de l'utilisateur"""
        try:
            current_user_id = get_jwt_identity()
            
            # Récupérer les filtres depuis les query parameters
            status = request.args.get('status')
            priority = request.args.get('priority')
            
            response, status_code = TaskService.get_all_tasks(
                current_user_id, 
                status=status, 
                priority=priority
            )
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def get_task(task_id):
        """Récupérer une tâche spécifique"""
        try:
            current_user_id = get_jwt_identity()
            
            response, status_code = TaskService.get_task(task_id, current_user_id)
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def update_task(task_id):
        """Mettre à jour une tâche"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            response, status_code = TaskService.update_task(
                task_id, 
                current_user_id, 
                data
            )
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @jwt_required()
    def delete_task(task_id):
        """Supprimer une tâche"""
        try:
            current_user_id = get_jwt_identity()
            
            response, status_code = TaskService.delete_task(task_id, current_user_id)
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500