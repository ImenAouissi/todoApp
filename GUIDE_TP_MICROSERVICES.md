# Guide pas à pas : du monolithe todoApp aux microservices

Ce guide suit les 5 exercices du sujet, dans l'ordre, avec les commandes et le code à écrire.
Il est basé sur le contenu réel de ton dépôt (`backend/`, `frontend/`).
Le code Docker n'a pas été exécuté ici (pas de Docker dans mon environnement) : fais le test final chez toi.

**Durée visée : ~50 min. Ordre de travail : 1 → 2 → 3 → 4 → 5.**

---

## 0. Préparation (2 min)

```bash
cd todoApp                 # racine du dépôt (là où se trouvent backend/ et frontend/)
git status                 # doit être propre
git remote -v              # vérifie que "origin" pointe bien vers GitHub (le sujet demande GitHub)
git branch                 # tu dois être sur main
```

Si `origin` pointe vers GitLab (ton README par défaut le mentionne), ajoute/modifie le remote GitHub :

```bash
git remote set-url origin https://github.com/<ton-user>/<ton-repo>.git
```

Crée tout de suite `RENDU.md` à la racine : tu y colleras les sorties au fur et à mesure.

---

## EXERCICE 1 : Analyse de l'architecture (sans rien modifier)

### 1.1 Ce que tu dois constater dans le code

| Question | Réponse tirée du code |
|---|---|
| Monolithe ou microservices ? | **Monolithe** : un seul backend Flask, une seule application (`create_app()` dans `backend/app/__init__.py`) qui enregistre les deux blueprints `users_bp` et `tasks_bp`. |
| Parties déployables | **2** : `backend/` (Flask, port 5000) et `frontend/` (React). |
| Organisation interne du backend | Architecture en couches : `routes/` → `controllers/` → `services/` → `models/`, + `utils/`, `config.py`, `extensions.py`, `tests/`. |
| Base de données | **MongoDB** (`flask-pymongo`, `MONGO_URI` par défaut `mongodb://localhost:27017/todolist` dans `backend/app/config.py`). Une seule base `todolist` pour users et tasks. |

Éléments précis à citer (au moins 3) :
- `backend/app/__init__.py` : un seul `create_app()` enregistre `users_bp` et `tasks_bp`.
- `backend/app/config.py` : une seule `MONGO_URI` / une seule base `todolist`.
- `backend/run.py` : un seul point d'entrée, un seul processus, port 5000.
- `backend/app/models/` (`user.py`, `task.py`) : les deux modèles partagent la même instance `mongo` de `extensions.py`.

### 1.2 Docker ou « run dev » ?

```bash
git ls-files | grep -i -E "docker|compose"
```

La sortie est **vide** → il n'existe aucun `Dockerfile`, `.dockerignore` ni `docker-compose.yml` dans le dépôt : le projet ne s'exécute pas avec Docker tel quel, seulement en mode dev.

Lancement actuel :
- Backend : `python -m venv venv`, `pip install -r requirements.txt`, `python run.py`
- Frontend : `npm install`, `npm start` (port 3000)
- MongoDB doit tourner en local sur `localhost:27017`.

Éléments qui gêneraient les conteneurs (en donner au moins 2) :
1. `config.py` : `MONGO_URI` par défaut = `localhost` → dans un conteneur, `localhost` est le conteneur lui-même, pas MongoDB.
2. `app/__init__.py` : CORS et en-têtes avec `http://localhost:3000` écrits en dur.
3. `config.py` : secret JWT par défaut en dur (`ma_super_cle_secrete_123456789`).
4. `run.py` : `debug=True`, port 5000 en dur, serveur de dev Flask (pas de gunicorn).
5. `frontend/.env` : `REACT_APP_API_URL=http://localhost:5000/api` en dur et **suivi par Git**.

### 1.3 Modèle de réponse pour RENDU.md (10 lignes max)

````markdown
# RENDU

## Exercice 1

1. Architecture : monolithe. 2 parties déployables : backend Flask (5000) et frontend React (3000).
2. Backend en couches : routes/ -> controllers/ -> services/ -> models/ (+ utils/, config.py, extensions.py, tests/).
3. Base : MongoDB (flask-pymongo), une seule base `todolist` (backend/app/config.py).
4. Preuves : un seul create_app() qui enregistre users_bp et tasks_bp (app/__init__.py) ; une seule
   MONGO_URI (config.py) ; un seul point d'entrée run.py ; models partagent la même instance mongo (extensions.py).
5. Docker : non, aucun fichier Docker ; le projet se lance en mode dev (python run.py, npm start, Mongo local).
6. Freins aux conteneurs : MONGO_URI par défaut sur localhost ; CORS localhost:3000 en dur ; secret JWT en dur ;
   run.py en debug avec port en dur ; frontend/.env suivi par Git.

Sortie de `git ls-files | grep -i -E "docker|compose"` : (vide). Cela prouve qu'aucun fichier Docker
ou Compose n'est versionné dans le dépôt.
````

### 1.4 Commit

```bash
git add RENDU.md
git commit -m "docs: add architecture analysis (exercise 1)"
```

---

## EXERCICE 2 : Git et hygiène du dépôt

### 2.1 Tag annoté sur main, puis push

```bash
git checkout main
git tag -a v1-monolithe -m "Version monolithe avant passage aux microservices"
git push origin v1-monolithe
```

### 2.2 Branche `microservice`

```bash
git checkout -b microservice
```

Tout le reste se fait ici.

### 2.3 Fichiers sensibles suivis

```bash
git ls-files | grep -i env
```

Tu vas très probablement voir `frontend/.env` (il est dans le zip, et `frontend/.gitignore` n'ignore que `.env.local`, etc., **pas** `.env`). Retire-le de l'index (le fichier reste sur ton disque) :

```bash
git rm --cached frontend/.env
```

Explication en une ligne (à mettre dans RENDU.md) :
> `.env` contient une configuration propre à chaque machine, voire des secrets : il ne doit pas être versionné ; on versionne seulement `.env.example` avec des valeurs fictives.

### 2.4 `.gitignore` à la racine + dans chaque partie

Racine `.gitignore` :

```gitignore
# Dépendances
node_modules/
venv/
.venv/
__pycache__/
*.pyc

# Secrets / config locale
.env
.env.*
!.env.example

# Logs et build
*.log
build/
dist/

# Système / éditeur
.DS_Store
.idea/
.vscode/
```

Le `!.env.example` est important : il garde `.env.example` versionnable.

Pour `backend/` (qui va disparaître à l'exercice 3, mais fais-le pour respecter la consigne) et `frontend/`, ajoute les lignes manquantes :

```bash
# frontend/.gitignore : ajouter à la fin
cat >> frontend/.gitignore <<'EOF'

# ajouts
node_modules/
.env
*.log
venv/
__pycache__/
build/
EOF

# backend/.gitignore : ajouter à la fin
cat >> backend/.gitignore <<'EOF'

# ajouts
node_modules/
*.log
build/
EOF
```

Plus tard, chaque service aura son propre `.gitignore` (voir 3.6). Commit :

```bash
git add .gitignore frontend/.gitignore backend/.gitignore
git commit -m "chore: add gitignore files and untrack frontend/.env"
```

### 2.5 Repérer les secrets en dur (juste les noter)

```bash
grep -rn -E "secret|SECRET|localhost|mongodb://" backend/app backend/run.py frontend/src frontend/.env
```

À noter pour l'exercice 3 :
- `backend/app/config.py` : `JWT_SECRET_KEY` par défaut `'ma_super_cle_secrete_123456789'`
- `backend/app/config.py` : `MONGO_URI` par défaut avec `localhost`
- `backend/app/__init__.py` : origines CORS `http://localhost:3000` / `127.0.0.1:3000`
- `backend/run.py` : port 5000 et `debug=True`

### 2.6 Sorties à coller dans RENDU.md (ajoute-les en fin d'exercice 5 pour avoir les vrais résultats)

```bash
git tag -n
git branch
git log --oneline
```

---

## EXERCICE 3 : Traduction en microservices

### 3.0 Structure cible

```
todoApp/
├── services/
│   ├── auth-service/      (port 5001, base users)
│   ├── task-service/      (port 5002, base tasks)
│   └── gateway/           (port 5000)
├── frontend/
├── docker-compose.yml
├─�� .env.example
├── .gitignore
├── README.md
└── RENDU.md
```

### 3.1 Découpage du code (commit `refactor:`)

```bash
mkdir -p services/auth-service/app/{routes,controllers,services,models}
mkdir -p services/task-service/app/{routes,controllers,services,models}
mkdir -p services/gateway/app

# --- auth-service : tout ce qui concerne les utilisateurs
git mv backend/app/routes/users.py                    services/auth-service/app/routes/users.py
git mv backend/app/controllers/user_controller.py     services/auth-service/app/controllers/user_controller.py
git mv backend/app/services/auth_service.py           services/auth-service/app/services/auth_service.py
git mv backend/app/models/user.py                     services/auth-service/app/models/user.py

# --- task-service : tout ce qui concerne les tâches
git mv backend/app/routes/tasks.py                    services/task-service/app/routes/tasks.py
git mv backend/app/controllers/task_controller.py     services/task-service/app/controllers/task_controller.py
git mv backend/app/services/task_service.py           services/task-service/app/services/task_service.py
git mv backend/app/models/task.py                     services/task-service/app/models/task.py

# --- fichiers communs : copiés dans les deux services (un service n'importe JAMAIS l'autre)
for s in auth-service task-service; do
  cp backend/app/extensions.py services/$s/app/extensions.py
  touch services/$s/app/__init__.py \
        services/$s/app/routes/__init__.py \
        services/$s/app/controllers/__init__.py \
        services/$s/app/services/__init__.py \
        services/$s/app/models/__init__.py
done
```

Ensuite, supprime l'ancien backend (le reste : `config.py`, `__init__.py`, `run.py`, `utils/`, `tests/`, `README.md`, `requirements.txt` est réécrit ou vide) :

```bash
git rm -r backend
rm -rf backend            # supprime d'éventuels fichiers non suivis (venv, __pycache__)
```

> `utils/` et `tests/` sont vides dans ton dépôt, donc rien à migrer.

Ajuste `extensions.py` dans **chaque** service : retire CORS (seule la gateway gère le CORS) et, pour `task-service`, retire tout ce qui concerne les utilisateurs (il n'y en a pas) :

```python
# services/auth-service/app/extensions.py  et  services/task-service/app/extensions.py
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()
```

Vérifie que les imports restent corrects (`from app.extensions import mongo`, `from app.models.user import User`, etc.) : ils le sont, car chaque service a sa propre arborescence `app/`.

Ne fais pas encore le commit : fais d'abord 3.2 à 3.5 pour que chaque service démarre, puis commit par étapes (voir 3.9).

### 3.2 `auth-service` (port 5001, base `users`)

**`services/auth-service/app/__init__.py`**

```python
import os
from flask import Flask
from app.extensions import mongo, jwt


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]          # base users
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # pas de valeur par défaut
    app.url_map.strict_slashes = False

    mongo.init_app(app)
    jwt.init_app(app)

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    @app.route("/health", methods=["GET"])
    def health():
        # volontairement sans accès à la base
        return {"status": "ok"}, 200

    return app
```

`os.environ["..."]` (et non `os.getenv(..., "défaut")`) fait planter le service au démarrage si la variable manque : c'est voulu, ça évite tout secret par défaut.

**`services/auth-service/run.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # lit .env en mode "sans Docker" ; sans effet dans Docker

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        debug=os.getenv("DEBUG", "False") == "True",
    )
```

**`services/auth-service/requirements.txt`**

```
Flask==2.3.3
Werkzeug==2.3.7
Flask-PyMongo==2.3.0
pymongo==4.5.0
Flask-JWT-Extended==4.5.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

(On retire `bcrypt`, `email-validator` et `flask-cors`, qui ne servent à rien ici.)

**`services/auth-service/.env.example`**

```env
PORT=5001
MONGO_URI=mongodb://localhost:27017/users
JWT_SECRET_KEY=change-me-with-a-long-random-string
DEBUG=False
```

### 3.3 `task-service` (port 5002, base `tasks`)

Mêmes fichiers, adaptés :

**`services/task-service/app/__init__.py`**

```python
import os
from flask import Flask
from app.extensions import mongo, jwt


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]          # base tasks
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # même secret que auth-service
    app.url_map.strict_slashes = False

    mongo.init_app(app)
    jwt.init_app(app)

    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app
```

**`services/task-service/run.py`** : identique à celui d'auth-service (copie-le).

**`services/task-service/requirements.txt`**

```
Flask==2.3.3
Werkzeug==2.3.7
Flask-PyMongo==2.3.0
pymongo==4.5.0
Flask-JWT-Extended==4.5.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

**`services/task-service/.env.example`**

```env
PORT=5002
MONGO_URI=mongodb://localhost:27017/tasks
JWT_SECRET_KEY=change-me-with-a-long-random-string
DEBUG=False
```

Point du sujet : *task-service ne cherche jamais un utilisateur dans la base `users`*. C'est déjà le cas : `TaskController` utilise seulement `get_jwt_identity()` (l'id contenu dans le jeton, vérifié avec le même `JWT_SECRET_KEY`) et `Task` filtre par `userId`. Vérifie avec :

```bash
grep -rn "user" services/task-service/app | grep -v -i "user_id\|userId\|current_user_id"
```

Il ne doit rester aucun import de `User` ni aucune requête sur la collection `users`.

### 3.4 `gateway` (port 5000)

**`services/gateway/app/__init__.py`**

```python
import os
import requests
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

METHODS = ["GET", "POST", "PUT", "DELETE"]
FORWARDED_REQUEST_HEADERS = ("authorization", "content-type")


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    origins = [o.strip() for o in os.environ["CORS_ORIGINS"].split(",") if o.strip()]
    CORS(
        app,
        origins=origins,
        methods=METHODS + ["OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Authorization"],
        supports_credentials=True,
    )

    timeout = float(os.environ.get("UPSTREAM_TIMEOUT", "10"))
    upstreams = {
        "/api/users": os.environ["AUTH_SERVICE_URL"],
        "/api/tasks": os.environ["TASK_SERVICE_URL"],
    }

    def make_proxy(prefix, base_url):
        def proxy(path=""):
            target = f"{base_url}{prefix}" + (f"/{path}" if path else "")
            headers = {
                k: v for k, v in request.headers
                if k.lower() in FORWARDED_REQUEST_HEADERS
            }
            try:
                resp = requests.request(
                    request.method,
                    target,
                    params=request.args,
                    data=request.get_data(),
                    headers=headers,
                    timeout=timeout,
                )
            except requests.exceptions.RequestException:
                return jsonify({
                    "error": "Service temporairement indisponible, réessayez plus tard"
                }), 503

            out = Response(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/json"),
            )
            if "Authorization" in resp.headers:
                out.headers["Authorization"] = resp.headers["Authorization"]
            return out

        proxy.__name__ = "proxy_" + prefix.strip("/").replace("/", "_")
        app.add_url_rule(prefix, view_func=proxy, defaults={"path": ""}, methods=METHODS)
        app.add_url_rule(f"{prefix}/<path:path>", view_func=proxy, methods=METHODS)

    for prefix, base_url in upstreams.items():
        make_proxy(prefix, base_url)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app
```

Le préflight CORS (`OPTIONS`) est traité automatiquement par `flask-cors` : les services n'ont donc pas besoin de CORS.

**`services/gateway/run.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        debug=os.getenv("DEBUG", "False") == "True",
    )
```

**`services/gateway/requirements.txt`**

```
Flask==2.3.3
Werkzeug==2.3.7
Flask-CORS==4.0.1
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

**`services/gateway/.env.example`**

```env
PORT=5000
AUTH_SERVICE_URL=http://localhost:5001
TASK_SERVICE_URL=http://localhost:5002
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
UPSTREAM_TIMEOUT=10
DEBUG=False
```

(Dans Docker, `AUTH_SERVICE_URL` vaudra `http://auth-service:5001` : le nom du service Compose est l'adresse.)

**Frontend** : ton `frontend/.env` pointe déjà vers `http://localhost:5000/api`, c'est-à-dire vers la gateway. Il n'y a donc rien à changer dans le code. Crée juste un exemple versionné :

```bash
cp frontend/.env frontend/.env.example      # contient REACT_APP_API_URL=http://localhost:5000/api
```

### 3.5 Fichiers Docker de chaque service

**`services/<service>/Dockerfile`** (identique pour les 3, seul `PORT` change à l'exécution) :

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# PORT vient de l'environnement (docker-compose / .env)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} run:app"]
```

**`services/<service>/.dockerignore`**

```
venv/
.venv/
__pycache__/
*.pyc
.env
*.log
.git
.gitignore
Dockerfile
.dockerignore
```

Le `.env` est exclu de l'image : les secrets arrivent par `docker-compose`, jamais dans l'image.

**`services/<service>/.gitignore`** (pour les 3 services) :

```gitignore
node_modules/
.env
*.log
venv/
__pycache__/
build/
```

Génère tout d'un coup :

```bash
for s in auth-service task-service gateway; do
  cat > services/$s/Dockerfile <<'EOF'
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} run:app"]
EOF
  printf 'venv/\n.venv/\n__pycache__/\n*.pyc\n.env\n*.log\n.git\n.gitignore\nDockerfile\n.dockerignore\n' > services/$s/.dockerignore
  printf 'node_modules/\n.env\n*.log\nvenv/\n__pycache__/\nbuild/\n' > services/$s/.gitignore
done
```

### 3.6 `.env.example` racine (valeurs fictives)

```env
# --- MongoDB (un seul serveur, deux bases : users et tasks)
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=change-me-password

# --- Secret JWT partagé par auth-service et task-service
JWT_SECRET_KEY=change-me-with-a-long-random-string

# --- Ports (internes aux conteneurs ; seul GATEWAY_PORT est publié)
GATEWAY_PORT=5000
AUTH_PORT=5001
TASK_PORT=5002

# --- CORS : origine(s) du frontend, autorisée(s) par la gateway uniquement
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

> Si ton mot de passe Mongo contient des caractères spéciaux (`@`, `:`, `/`…), il doit être encodé en URL dans la `MONGO_URI`. Avec un mot de passe alphanumérique, aucun souci.

Puis crée ton vrai `.env` (ignoré par Git) :

```bash
cp .env.example .env
# édite .env : mets un vrai mot de passe et un vrai secret
python3 -c "import secrets; print(secrets.token_hex(32))"   # pour générer JWT_SECRET_KEY
```

### 3.7 `docker-compose.yml`

```yaml
services:
  mongo:
    image: mongo:7
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test:
        - CMD
        - mongosh
        - --quiet
        - -u
        - ${MONGO_ROOT_USER}
        - -p
        - ${MONGO_ROOT_PASSWORD}
        - --authenticationDatabase
        - admin
        - --eval
        - "db.adminCommand('ping').ok"
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    # pas de "ports:" : MongoDB n'est pas exposé à l'hôte

  auth-service:
    build: ./services/auth-service
    restart: unless-stopped
    environment:
      PORT: ${AUTH_PORT}
      MONGO_URI: mongodb://${MONGO_ROOT_USER}:${MONGO_ROOT_PASSWORD}@mongo:27017/users?authSource=admin
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      mongo:
        condition: service_healthy
    healthcheck:
      test:
        - CMD-SHELL
        - python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:'+os.environ['PORT']+'/health')"
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  task-service:
    build: ./services/task-service
    restart: unless-stopped
    environment:
      PORT: ${TASK_PORT}
      MONGO_URI: mongodb://${MONGO_ROOT_USER}:${MONGO_ROOT_PASSWORD}@mongo:27017/tasks?authSource=admin
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      mongo:
        condition: service_healthy
    healthcheck:
      test:
        - CMD-SHELL
        - python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:'+os.environ['PORT']+'/health')"
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  gateway:
    build: ./services/gateway
    restart: unless-stopped
    environment:
      PORT: ${GATEWAY_PORT}
      AUTH_SERVICE_URL: http://auth-service:${AUTH_PORT}
      TASK_SERVICE_URL: http://task-service:${TASK_PORT}
      CORS_ORIGINS: ${CORS_ORIGINS}
    depends_on:
      auth-service:
        condition: service_healthy
      task-service:
        condition: service_healthy
    ports:
      - "${GATEWAY_PORT}:${GATEWAY_PORT}"   # SEUL port publié
    healthcheck:
      test:
        - CMD-SHELL
        - python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:'+os.environ['PORT']+'/health')"
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

volumes:
  mongo_data:
```

Points du barème à vérifier :
- healthcheck + volume pour la base : oui (`mongo_data`)
- identifiants lus depuis `.env` : oui (`${MONGO_ROOT_USER}`…)
- `depends_on` + `condition: service_healthy` : oui
- noms de services comme adresses (`mongo`, `auth-service`, `task-service`) : oui
- seul le port 5000 est publié : oui (aucun `ports:` ailleurs)

Test :

```bash
docker compose config        # vérifie la syntaxe et l'interpolation
docker compose up --build -d
docker compose ps            # tous "healthy"
```

### 3.8 Test de bout en bout par la gateway

```bash
curl -i -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"secret123"}'
```

Attendu : `HTTP/1.1 201 CREATED` avec `access_token` et `refresh_token`.
Puis un test de tâche avec le token reçu :

```bash
TOKEN="<access_token>"
curl -i -X POST http://localhost:5000/api/tasks \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Ma première tâche"}'
curl -i http://localhost:5000/api/tasks -H "Authorization: Bearer $TOKEN"
```

Test du 503 : `docker compose stop task-service`, puis `curl -i http://localhost:5000/api/tasks -H "Authorization: Bearer $TOKEN"` doit renvoyer `503`. Relance avec `docker compose start task-service`.

Test de non-exposition : `curl http://localhost:5001/health` doit échouer (connexion refusée).

Frontend (hors Docker) : `cd frontend && npm install && npm start` → http://localhost:3000.

### 3.9 Commits (au moins 3 pour cet exercice)

```bash
git add -A services backend           # le déplacement/suppression de backend
git commit -m "refactor: split backend into auth-service and task-service"

git add services/auth-service/app/__init__.py services/auth-service/run.py \
        services/task-service/app/__init__.py services/task-service/run.py \
        services/*/requirements.txt services/*/.env.example services/*/.gitignore
git commit -m "chore: add per-service env config and remove hardcoded secrets"

git add services/gateway
git commit -m "feat: add gateway service with reverse proxy and CORS"

git add services/*/Dockerfile services/*/.dockerignore docker-compose.yml .env.example frontend/.env.example
git commit -m "feat: add Dockerfiles and docker-compose with mongo healthcheck"
```

Si Git refuse un `git add` parce qu'un fichier est déjà ajouté, ce n'est pas grave : ajuste simplement le découpage des commits. Le but est d'avoir des messages propres et variés (`refactor:`, `feat:`, `chore:`, `docs:`, `fix:`).

### 3.10 Sorties à coller dans RENDU.md

```bash
ls services/*
docker compose ps
curl -i -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test2@example.com","password":"secret123"}'
```

(Utilise un autre email que précédemment si l'utilisateur existe déjà, sinon tu obtiens `409`.)

---

## EXERCICE 4 : Microservices sans Docker

### 4.1 Texte pour RENDU.md (6 à 8 lignes)

````markdown
## Exercice 4

Oui, c'est possible : un microservice se définit par son découpage (un service = une responsabilité, son
propre code, sa propre base, son propre déploiement et une communication par API), pas par Docker.
Mais c'est peu pratique : Docker ajoute l'isolation, la reproductibilité et l'orchestration (réseau, healthchecks).
Avantages de Docker pour ce projet : (1) un seul `docker compose up` lance Mongo + 3 services avec le même
environnement partout ; (2) réseau interne isolé : seule la gateway est exposée, Mongo et les services restent privés.
Difficultés sans Docker : (1) installer et configurer MongoDB soi-même, et gérer un venv et un terminal par service
avec des versions de Python/dépendances qui peuvent différer ; (2) gérer à la main les ports, les .env et l'ordre
de démarrage (pas de depends_on/healthcheck), donc plus d'erreurs de configuration.
````

### 4.2 Preuve : lancer les trois services sans Docker

Prérequis : MongoDB local sur `localhost:27017` (si tu n'en as pas, dis-le dans RENDU.md, les services démarrent quand même car `/health` ne touche pas la base : PyMongo se connecte paresseusement).

Prépare les `.env` (un par service) :

```bash
for s in auth-service task-service gateway; do cp services/$s/.env.example services/$s/.env; done
# Mets le MÊME JWT_SECRET_KEY dans auth-service/.env et task-service/.env
```

**Terminal 1 : auth-service**

```bash
cd services/auth-service
python3 -m venv venv
source venv/bin/activate            # Windows : venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Terminal 2 : task-service**

```bash
cd services/task-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

**Terminal 3 : gateway**

```bash
cd services/gateway
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

**Terminal 4 : vérifications**

```bash
curl -i http://localhost:5000/health
curl -i http://localhost:5001/health
curl -i http://localhost:5002/health
```

Chaque réponse doit contenir `{"status":"ok"}`. Pense à arrêter la pile Docker avant (`docker compose down`) pour libérer le port 5000.

### 4.3 Section « Lancer sans Docker » dans le README

Tu rédigeras le README complet à l'exercice 5. Si tu veux committer maintenant, crée-le avec au moins cette section (tu la garderas telle quelle) :

````markdown
## Lancer sans Docker

Prérequis : Python 3.11+, Node.js 18+, MongoDB en local (`localhost:27017`).

1. Configuration (un `.env` par service, à partir des exemples) :
   ```bash
   cp services/auth-service/.env.example services/auth-service/.env
   cp services/task-service/.env.example services/task-service/.env
   cp services/gateway/.env.example     services/gateway/.env
   cp frontend/.env.example             frontend/.env
   ```
   Le `JWT_SECRET_KEY` doit être identique dans `auth-service` et `task-service`.

2. Un terminal par service :
   ```bash
   # auth-service (5001)
   cd services/auth-service && python3 -m venv venv && source venv/bin/activate \
     && pip install -r requirements.txt && python run.py

   # task-service (5002)
   cd services/task-service && python3 -m venv venv && source venv/bin/activate \
     && pip install -r requirements.txt && python run.py

   # gateway (5000)
   cd services/gateway && python3 -m venv venv && source venv/bin/activate \
     && pip install -r requirements.txt && python run.py
   ```

3. Frontend :
   ```bash
   cd frontend && npm install && npm start
   ```

4. Vérification : `curl http://localhost:5000/health`, `:5001/health`, `:5002/health`.
````

```bash
git add README.md RENDU.md
git commit -m "docs: add 'run without Docker' section"
```

---

## EXERCICE 5 : Livraison

### 5.1 README.md complet (remplace le modèle GitLab)

````markdown
# todoApp : gestionnaire de tâches (architecture microservices)

Application web de gestion de tâches : inscription / connexion (JWT), création, modification, filtrage et
suppression de tâches avec priorité, statut et date d'échéance.

## Architecture

| Service | Rôle | Port | Base MongoDB |
|---|---|---|---|
| `gateway` | Point d'entrée unique, reverse proxy, CORS | 5000 (publié) | aucune |
| `auth-service` | Utilisateurs, inscription, connexion, JWT | 5001 (interne) | `users` |
| `task-service` | Tâches (CRUD, filtres) | 5002 (interne) | `tasks` |
| `frontend` | Interface React | 3000 | aucune |
| `mongo` | Base de données | 27017 (interne) | `users`, `tasks` |

La gateway route `/api/users/*` vers `auth-service` et `/api/tasks/*` vers `task-service`.
`task-service` ne consulte jamais la base `users` : il vérifie le jeton JWT avec le même secret.

## Configuration

Les variables sont décrites dans les fichiers d'exemple (valeurs fictives) :
`.env.example` (racine, pour Docker), `services/*/.env.example` (sans Docker) et `frontend/.env.example`.
Les vrais fichiers `.env` ne sont jamais versionnés.

## Lancer avec Docker

```bash
cp .env.example .env        # puis modifier le mot de passe Mongo et JWT_SECRET_KEY
docker compose up --build
curl http://localhost:5000/health
```

Frontend : `cd frontend && npm install && npm start` (http://localhost:3000).

## Lancer sans Docker
(section de l'exercice 4)

## Tests rapides

```bash
curl -i -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"secret123"}'
```
````

(Remplace la ligne « (section de l'exercice 4) » par le contenu de la section de 4.3.)

### 5.2 Contrôles avant envoi

```bash
git status                                    # propre
git ls-files | grep -E "(^|/)\.env$"          # ne doit rien renvoyer
docker compose down -v
docker compose up --build -d && docker compose ps
git log --oneline                             # >= 6 commits au format feat:/fix:/docs:/chore:/refactor:
```

Si tu as moins de 6 commits, découpe tes changements (par exemple : un `fix:` pour un bug rencontré, un `docs:` pour le README, un `chore:` pour `.dockerignore`). Ne triche pas avec des commits vides : fais des vrais petits commits.

### 5.3 Compléter RENDU.md puis envoyer

Ajoute à `RENDU.md` : `git tag -n`, `git branch`, `git log --oneline` (exercice 2), la sortie de la commande de contrôle des `.env` (vide, à dire explicitement), et l'URL de la branche :
`https://github.com/<ton-user>/<ton-repo>/tree/microservice`.

```bash
git add RENDU.md
git commit -m "docs: complete RENDU.md"
git push -u origin microservice
```

Ne fusionne pas dans `main`. Sur GitHub, vérifie que la branche `microservice` existe et contient `services/`, `docker-compose.yml`, `README.md` et `RENDU.md`, et que le tag `v1-monolithe` apparaît dans *Tags*.

---

## Checklist finale

- [ ] Tag annoté `v1-monolithe` poussé, branche `microservice` créée
- [ ] Aucun `.env` suivi par Git (`frontend/.env` retiré de l'index)
- [ ] `.gitignore` racine + un par service/partie
- [ ] Plus de secret JWT par défaut ; tout vient des variables d'environnement
- [ ] Chaque service : `run.py`, `app/`, `requirements.txt`, `Dockerfile`, `.dockerignore`, `.env.example`, `GET /health`
- [ ] Chaque service n'importe jamais le code d'un autre ; deux bases (`users`, `tasks`)
- [ ] Gateway : routage, en-tête `Authorization`, 503 si service absent, CORS uniquement ici
- [ ] `docker-compose.yml` : healthchecks, volume, `service_healthy`, seul le port 5000 publié
- [ ] Section « Lancer sans Docker » + README complet
- [ ] Au moins 6 commits conventionnels, `git status` propre
- [ ] `git push -u origin microservice`, RENDU.md complet

## Pièges fréquents

- **`KeyError: 'MONGO_URI'` au démarrage** : le `.env` du service est absent ou mal nommé (sans Docker), ou la variable manque dans `docker-compose.yml`.
- **401 sur les tâches** : le `JWT_SECRET_KEY` n'est pas identique entre `auth-service` et `task-service`.
- **Erreur CORS dans le navigateur** : `CORS_ORIGINS` de la gateway ne contient pas exactement l'origine du frontend (`http://localhost:3000`).
- **`Authentication failed` côté Mongo** : le volume `mongo_data` a été créé avec d'anciens identifiants ; fais `docker compose down -v` puis relance.
- **Port 5000 déjà utilisé** : sur macOS, AirPlay occupe parfois le 5000 ; désactive-le ou arrête l'autre processus.
- **`.env.example` ignoré par Git** : vérifie la ligne `!.env.example` dans le `.gitignore` racine.
