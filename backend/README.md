# Explication des dossiers clés

| Dossier       | Rôle |
|--------------|------|
| `models/`     | Définit les schémas MongoDB (ex: avec PyMongo ou MongoEngine) |
| `routes/`     | Déclare les endpoints et appelle les contrôleurs |
| `controllers/`| Contient la logique métier (CRUD, filtres, etc.) |
| `services/`   | Gère l'authentification, JWT, hash des mots de passe |
| `utils/`      | Fonctions transverses (validation, formatage) |
| `tests/`      | Tests avec pytest ou unittest |

---

# Création et activation d'un environnement virtuel

## 1. Créer l'environnement virtuel

```bash
python -m venv venv
# ou
python3 -m venv venv
````

## 2. Activer l'environnement virtuel

### Sur Mac / Linux

```bash
source venv/bin/activate
```

### Sur Windows

```bash
venv\Scripts\activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

```

---
