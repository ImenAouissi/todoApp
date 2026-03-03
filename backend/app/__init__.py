from flask import Flask, request, jsonify
from app.config import Config
from app.extensions import mongo, jwt
from flask_cors import CORS
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuration CORS simplifiée mais efficace
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         expose_headers=["Content-Type", "Authorization"],
         supports_credentials=True,
         max_age=600)

    # Désactiver la redirection automatique des slashes
    app.url_map.strict_slashes = False

    # Initialisation des extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # Enregistrement des blueprints
    from app.routes.users import users_bp
    from app.routes.tasks import tasks_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

    # Route de test
    @app.route('/api/health', methods=['GET', 'OPTIONS'])
    def health_check():
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
            return response, 200
        return {'status': 'OK', 'message': 'API is running'}, 200

    # Gestionnaire global pour les requêtes OPTIONS
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = jsonify({'message': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '600')
            return response, 200

    return app