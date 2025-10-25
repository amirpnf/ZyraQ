# ZyraQ - Application de Quiz Interactive

Application web de quiz développée avec Vue.js 3 (frontend) et Flask (backend).

## 📋 Prérequis

### Frontend
- Node.js version **20.19+** ou **22.12+**
- npm (inclus avec Node.js)

### Backend
- Python 3.8+
- Flask
- Flask-CORS

## 🚀 Installation et Démarrage

### 1. Backend (API Flask)

```bash
cd ZyraQ-api
pip install -r requirements.txt
python app.py
```

Le serveur backend démarre sur `http://localhost:5000`

### 2. Frontend (Vue.js)

```bash
cd ZyraQ-ui
npm install
npm run dev
```

L'application frontend démarre sur `http://localhost:3000`

## 📁 Structure du Projet

### Frontend (ZyraQ-ui/)
```
src/
├── components/          # Composants réutilisables
│   └── QuestionDisplay.vue
├── views/              # Pages de l'application
│   ├── HomePage.vue
│   ├── NewQuizPage.vue
│   ├── QuestionsManager.vue
│   └── ScorePage.vue
├── services/           # Services pour les appels API
│   ├── QuizApiService.js
│   └── ParticipationStorageService.js
├── router/             # Configuration des routes
│   └── index.js
├── App.vue             # Composant racine
└── main.js             # Point d'entrée
```

### Backend (ZyraQ-api/)
```
├── app.py              # Application Flask principale
├── question.py         # Gestion des questions
├── answer.py           # Gestion des réponses
├── player.py           # Gestion des joueurs
├── auth_token.py       # Authentification
├── jwt_utils.py        # Utilitaires JWT
└── requirements.txt    # Dépendances Python
```

## 🎯 Fonctionnalités

1. **Page d'accueil** (`/`)
   - Affichage du tableau des scores
   - Bouton pour démarrer un nouveau quiz

2. **Nouvelle participation** (`/new-quiz`)
   - Saisie du nom du joueur
   - Validation et démarrage du quiz

3. **Questions** (`/questions`)
   - Affichage des questions une par une
   - Barre de progression
   - Sélection des réponses

4. **Résultats** (`/score`)
   - Affichage du score final
   - Message de félicitations
   - Options pour recommencer ou retourner à l'accueil

## 🛠️ Technologies Utilisées

### Frontend
- **Vue.js 3** - Framework JavaScript progressif
- **Vue Router** - Gestion des routes
- **Axios** - Client HTTP pour les appels API
- **Bootstrap 5** - Framework CSS
- **Vite** - Outil de build rapide

### Backend
- **Flask** - Framework web Python
- **Flask-CORS** - Gestion des CORS
- **SQLite** - Base de données

## 🎨 Design

L'application utilise Bootstrap 5 pour un design responsive et moderne :
- Interface utilisateur intuitive
- Animations et transitions fluides
- Compatibilité mobile et desktop
- Thème professionnel avec palette de couleurs cohérente

## 📝 Configuration

### Variables d'environnement (Frontend)

Fichier `.env.development` :
```
VITE_API_URL=http://localhost:5000
```

Pour la production, créez un fichier `.env.production` avec l'URL de votre API de production.

## 🔧 Scripts disponibles

### Frontend
- `npm run dev` - Démarre le serveur de développement
- `npm run build` - Compile l'application pour la production
- `npm run preview` - Prévisualise la version de production
- `npm run lint` - Vérifie la qualité du code
- `npm run format` - Formate le code avec Prettier

### Backend
- `python app.py` - Démarre le serveur Flask
- `python rebuild_db.py` - Réinitialise la base de données

## ⚠️ Notes Importantes

1. **Version Node.js** : Assurez-vous d'utiliser Node.js 20.19+ ou 22.12+
2. **CORS** : Le backend doit être configuré pour accepter les requêtes du frontend
3. **LocalStorage** : L'application utilise le localStorage du navigateur pour stocker temporairement les données de participation

## 🐛 Dépannage

### Erreur "crypto.hash is not a function"
- Mettez à jour Node.js vers la version 20.19+ ou 22.12+
- Téléchargez depuis https://nodejs.org/

### Le frontend ne peut pas se connecter au backend
- Vérifiez que le backend est bien démarré sur le port 5000
- Vérifiez la configuration CORS dans le backend
- Vérifiez la variable `VITE_API_URL` dans `.env.development`

### Problèmes d'affichage
- Videz le cache du navigateur
- Vérifiez la console du navigateur pour les erreurs JavaScript

## 📄 Licence

Projet académique - 2025

## 👥 Auteurs

Développé dans le cadre d'un projet éducatif.
