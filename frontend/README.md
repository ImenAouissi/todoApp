# Explication des dossiers - Frontend

## Structure du projet

```

frontend/
├── public/
├── src/
├── .env
├── package.json
└── README.md

```

---

## Détails des dossiers et fichiers

| Dossier / Fichier | Rôle |
|-------------------|------|
| `public/` | Contient les fichiers statiques accessibles publiquement |
| `public/index.html` | Fichier HTML principal où l'application React est injectée |
| `public/favicon.ico` | Icône affichée dans l'onglet du navigateur |
| `src/` | Contient tout le code source de l'application React |
| `src/components/` | Composants réutilisables (Navbar, cartes, formulaires, etc.) |
| `src/pages/` | Pages principales de l'application (Login, Dashboard, etc.) |
| `src/services/` | Gestion des appels API vers le backend |
| `src/context/` | Gestion de l’état global avec React Context (authentification) |
| `src/App.js` | Composant principal qui gère le routing |
| `src/index.js` | Point d’entrée React (render de l’application) |
| `src/index.css` | Fichier de styles globaux |
| `.env` | Variables d’environnement (ex: URL du backend) |
| `package.json` | Liste des dépendances et scripts npm |
| `README.md` | Documentation du projet |

---

## Explication détaillée des dossiers importants

### `components/`
Contient les composants UI réutilisables :

- `Navbar.js` → Barre de navigation
- `PrivateRoute.js` → Protège les routes nécessitant une authentification
- `TaskCard.js` → Affichage d’une tâche
- `TaskForm.js` → Formulaire d’ajout/modification d’une tâche
- `Alert.js` → Messages d’erreur ou de succès

---

### `pages/`
Chaque fichier représente une page complète :

- `Login.js` → Page de connexion
- `Register.js` → Page d'inscription
- `Dashboard.js` → Page principale après connexion
- `Profile.js` → Gestion du profil utilisateur

---

### `services/`
Gère la communication avec le backend :

- `api.js` → Configuration Axios (baseURL, headers, token JWT)
- `auth.service.js` → Fonctions login, register, logout

---

### `context/`
- `AuthContext.js` → Gère l'état global d’authentification (user, token, logout)

---

# Installation et démarrage

## 1. Installer les dépendances

```bash
cd frontend
npm install
````

## 2. Lancer l'application

```bash
npm start
```

## 3. Accéder à l'application

* Ouvrez [http://localhost:3000](http://localhost:3000)
* Inscrivez-vous ou connectez-vous
* Commencez à gérer vos tâches !

```
