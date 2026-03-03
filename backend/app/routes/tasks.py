from flask import Blueprint
from app.controllers.task_controller import TaskController

tasks_bp = Blueprint('tasks', __name__)

# Ajoutez un slash à la fin pour éviter les redirections
tasks_bp.route('/', methods=['POST'])(TaskController.create_task)
tasks_bp.route('/', methods=['GET'])(TaskController.get_all_tasks)
tasks_bp.route('/<task_id>', methods=['GET'])(TaskController.get_task)
tasks_bp.route('/<task_id>', methods=['PUT'])(TaskController.update_task)
tasks_bp.route('/<task_id>', methods=['DELETE'])(TaskController.delete_task)