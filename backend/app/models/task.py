from app.extensions import mongo
from bson import ObjectId
from datetime import datetime

class Task:
    collection = mongo.db.tasks

    @staticmethod
    def create_task(user_id, title, description=None, priority='medium', status='pending', due_date=None):
        """Créer une nouvelle tâche"""
        # Convertir due_date en datetime si c'est une chaîne
        due_date_obj = None
        if due_date:
            try:
                # Si c'est une chaîne au format YYYY-MM-DD
                if isinstance(due_date, str) and 'T' not in due_date:
                    due_date_obj = datetime.fromisoformat(due_date + 'T00:00:00')
                elif isinstance(due_date, str):
                    due_date_obj = datetime.fromisoformat(due_date)
                else:
                    due_date_obj = due_date
            except:
                due_date_obj = due_date
        
        task_data = {
            'userId': ObjectId(user_id),
            'title': title,
            'description': description,
            'priority': priority,
            'status': status,
            'dueDate': due_date_obj,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        result = Task.collection.insert_one(task_data)
        task_data['_id'] = result.inserted_id
        return task_data

    @staticmethod
    def get_user_tasks(user_id):
        """Récupérer toutes les tâches d'un utilisateur"""
        tasks = Task.collection.find({'userId': ObjectId(user_id)}).sort('createdAt', -1)
        return list(tasks)

    @staticmethod
    def get_task_by_id(task_id, user_id):
        """Récupérer une tâche par son ID"""
        try:
            return Task.collection.find_one({
                '_id': ObjectId(task_id),
                'userId': ObjectId(user_id)
            })
        except:
            return None

    @staticmethod
    def update_task(task_id, user_id, update_data):
        """Mettre à jour une tâche"""
        try:
            # Convertir dueDate si présent
            if 'dueDate' in update_data and update_data['dueDate']:
                try:
                    if isinstance(update_data['dueDate'], str) and 'T' not in update_data['dueDate']:
                        update_data['dueDate'] = datetime.fromisoformat(update_data['dueDate'] + 'T00:00:00')
                    elif isinstance(update_data['dueDate'], str):
                        update_data['dueDate'] = datetime.fromisoformat(update_data['dueDate'])
                except:
                    pass  # Garder la valeur originale si la conversion échoue
            
            update_data['updatedAt'] = datetime.utcnow()
            
            result = Task.collection.update_one(
                {'_id': ObjectId(task_id), 'userId': ObjectId(user_id)},
                {'$set': update_data}
            )
            if result.modified_count > 0:
                return Task.get_task_by_id(task_id, user_id)
            return None
        except Exception as e:
            print(f"Erreur update_task: {e}")
            return None

    @staticmethod
    def delete_task(task_id, user_id):
        """Supprimer une tâche"""
        try:
            result = Task.collection.delete_one({
                '_id': ObjectId(task_id),
                'userId': ObjectId(user_id)
            })
            return result.deleted_count > 0
        except:
            return False

    @staticmethod
    def filter_tasks(user_id, status=None, priority=None):
        """Filtrer les tâches par statut et priorité"""
        query = {'userId': ObjectId(user_id)}
        
        if status:
            query['status'] = status
        if priority:
            query['priority'] = priority
            
        tasks = Task.collection.find(query).sort('createdAt', -1)
        return list(tasks)