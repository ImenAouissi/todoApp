from app.models.task import Task
from bson import ObjectId
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(user_id, data):
        """Service de création de tâche"""
        # Validation
        if not data.get('title'):
            return {'error': 'Le titre est requis'}, 400
        
        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority', 'medium')
        status = data.get('status', 'pending')
        due_date = data.get('dueDate')
        
        # Valider les valeurs énumérées
        valid_priorities = ['low', 'medium', 'high']
        valid_statuses = ['pending', 'in progress', 'done']
        
        if priority not in valid_priorities:
            return {'error': 'Priorité invalide'}, 400
        
        if status not in valid_statuses:
            return {'error': 'Statut invalide'}, 400
        
        # Créer la tâche
        task = Task.create_task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date
        )
        
        # Formater la réponse
        return TaskService.format_task(task), 201

    @staticmethod
    def get_all_tasks(user_id, status=None, priority=None):
        """Récupérer toutes les tâches avec filtres optionnels"""
        if status or priority:
            tasks = Task.filter_tasks(user_id, status, priority)
        else:
            tasks = Task.get_user_tasks(user_id)
        
        formatted_tasks = [TaskService.format_task(task) for task in tasks]
        return formatted_tasks, 200

    @staticmethod
    def get_task(task_id, user_id):
        """Récupérer une tâche spécifique"""
        task = Task.get_task_by_id(task_id, user_id)
        
        if not task:
            return {'error': 'Tâche non trouvée'}, 404
        
        return TaskService.format_task(task), 200

    @staticmethod
    def update_task(task_id, user_id, data):
        """Mettre à jour une tâche"""
        # Vérifier que la tâche existe
        existing_task = Task.get_task_by_id(task_id, user_id)
        if not existing_task:
            return {'error': 'Tâche non trouvée'}, 404
        
        # Préparer les données de mise à jour
        update_data = {}
        
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'priority' in data:
            valid_priorities = ['low', 'medium', 'high']
            if data['priority'] not in valid_priorities:
                return {'error': 'Priorité invalide'}, 400
            update_data['priority'] = data['priority']
        if 'status' in data:
            valid_statuses = ['pending', 'in progress', 'done']
            if data['status'] not in valid_statuses:
                return {'error': 'Statut invalide'}, 400
            update_data['status'] = data['status']
        if 'dueDate' in data:
            update_data['dueDate'] = data['dueDate']
        
        if not update_data:
            return {'error': 'Aucune donnée à mettre à jour'}, 400
        
        # Mettre à jour
        updated_task = Task.update_task(task_id, user_id, update_data)
        
        if not updated_task:
            return {'error': 'Erreur lors de la mise à jour'}, 500
        
        return TaskService.format_task(updated_task), 200

    @staticmethod
    def delete_task(task_id, user_id):
        """Supprimer une tâche"""
        deleted = Task.delete_task(task_id, user_id)
        
        if not deleted:
            return {'error': 'Tâche non trouvée'}, 404
        
        return {'message': 'Tâche supprimée avec succès'}, 200

    @staticmethod
    def format_task(task):
        """Formater une tâche pour la réponse JSON - CORRIGÉ"""
        # Fonction helper pour formater les dates en toute sécurité
        def format_date(date_value):
            if not date_value:
                return None
            if isinstance(date_value, datetime):
                return date_value.isoformat()
            if isinstance(date_value, str):
                return date_value
            return str(date_value)
        
        return {
            'id': str(task['_id']),
            'title': task['title'],
            'description': task.get('description', ''),
            'priority': task.get('priority', 'medium'),
            'status': task.get('status', 'pending'),
            'dueDate': format_date(task.get('dueDate')),
            'createdAt': format_date(task.get('createdAt')),
            'updatedAt': format_date(task.get('updatedAt'))
        }