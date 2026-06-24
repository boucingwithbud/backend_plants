# back_plants
# back_plants
# 🌿 front_plantes

Interface web de classification de maladies végétales, construite avec **React + Vite** et déployée via Docker/Nginx.

🔗 Démo en ligne : [front-plantes.vercel.app](https://front-plantes.vercel.app)

---

## 📋 Description

`front_plantes` est le frontend de l'application de détection de maladies de plantes. Il permet à l'utilisateur de soumettre une image de feuille et d'obtenir en retour une prédiction de maladie via l'API backend (`backend_plants`).

---

## 🛠️ Stack technique

| Technologie | Version | Rôle |
|---|---|---|
| React | ^19.2.0 | Framework UI |
| Vite | ^7.3.1 | Bundler / Dev server |
| Nginx | alpine | Serveur de production |
| Docker | — | Conteneurisation |
| ESLint | ^9.39.1 | Linting |

---

## 📁 Structure du projet

```
front_plantes/
├── public/             # Fichiers statiques publics
├── src/                # Code source React
├── index.html          # Point d'entrée HTML
├── vite.config.js      # Configuration Vite
├── eslint.config.js    # Configuration ESLint
├── nginx.conf          # Configuration Nginx (SPA routing)
├── Dockerfile          # Build multi-stage (Node → Nginx)
├── server.js           # Serveur Node (optionnel)
└── package.json        # Dépendances et scripts
```

---

## 🚀 Installation & Lancement

### Prérequis

- Node.js >= 20
- npm

### En local (mode développement)

```bash
# Cloner le dépôt
git clone https://github.com/paulcoffi/front_plantes.git
cd front_plantes

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

L'application sera disponible sur [http://localhost:5173](http://localhost:5173).

### Build de production

```bash
npm run build
npm run preview
```

---

## 🐳 Docker

Le projet utilise un **build multi-stage** :

1. **Stage 1 — Build** : Node 20 Alpine compile l'application React (`npm run build` → dossier `dist/`)
2. **Stage 2 — Serve** : Nginx Alpine sert les fichiers statiques et gère le routing SPA

```bash
# Construire l'image
docker build -t front_plantes .

# Lancer le conteneur
docker run -p 80:80 front_plantes
```

L'application sera disponible sur [http://localhost](http://localhost).

> Le fichier `nginx.conf` est configuré pour le routing SPA (React Router) — toutes les routes renvoient vers `index.html`.

---

## 📜 Scripts disponibles

| Commande | Description |
|---|---|
| `npm run dev` | Démarre le serveur de développement avec HMR |
| `npm run build` | Compile l'application pour la production |
| `npm run preview` | Prévisualise le build de production |
| `npm run lint` | Lance ESLint sur le code source |

---

## 🔗 Lien avec le backend

Ce frontend communique avec l'API **backend_plants** pour effectuer les prédictions. Assurez-vous que le backend est démarré et accessible.

👉 [backend_plants](https://github.com/paulcoffi/backend_plants)
