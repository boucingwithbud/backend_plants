# 🌱 backend_plants

API de classification de maladies végétales, construite avec **FastAPI** et des modèles de deep learning (**ResNet-152** + **Hugging Face Transformers**).

---

## 📋 Description

`backend_plants` est l'API REST qui expose des endpoints de prédiction de maladies de plantes à partir d'images. Elle prend en charge **7 cultures** grâce à des modèles entraînés spécifiquement pour chacune. Les modèles `.pth` sont stockés sur **AWS S3** et téléchargés automatiquement au démarrage.

---

## 🛠️ Stack technique

| Technologie | Rôle |
|---|---|
| FastAPI | Framework API REST |
| PyTorch + torchvision | Inférence des modèles ResNet-152 |
| Hugging Face Transformers | Inférence via pipeline (tomate, riz, maïs) |
| AWS S3 (boto3) | Stockage et téléchargement des modèles |
| Uvicorn | Serveur ASGI |
| Docker | Conteneurisation |
| python-dotenv | Gestion des variables d'environnement |

---

## 📁 Structure du projet

```
backend_plants/
├── models/                  # Modèles .pth (téléchargés depuis S3 au démarrage)
├── café_cacao/              # Encodeurs de classes pour le modèle café/cacao
├── cassava/                 # Encodeurs de classes pour le modèle manioc
├── cashew/                  # Encodeurs de classes pour le modèle cajou
├── Rubber tree/             # Encodeurs de classes pour le modèle hévéa
├── main.py                  # Point d'entrée FastAPI + configuration CORS
├── prediction.py            # Chargement des modèles et routes de prédiction
├── requirements.txt         # Dépendances Python
├── Dockerfile               # Image Docker de production
└── .env                     # Variables d'environnement (à créer, non versionné)
```

---

## 🤖 Modèles & Cultures supportées

| Endpoint | Culture | Architecture | Classes |
|---|---|---|---|
| `POST /predict_model1_café_cacao` | Café / Cacao | ResNet-152 | 8 |
| `POST /predict_model2_cassava` | Manioc (Cassava) | ResNet-152 | 5 |
| `POST /predict_model3_cashew` | Cajou (Cashew) | ResNet-152 | 5 |
| `POST /predict_model4_tomato` | Tomate | HuggingFace (`Doyourhomework/model_4_tomato`) | — |
| `POST /predict_model5_rice` | Riz | HuggingFace (`Doyourhomework/model_5_rice`) | — |
| `POST /predict_model6_maize` | Maïs | HuggingFace (`Doyourhomework/model_6_maize`) | — |
| `POST /predict_model7_rubber_tree` | Hévéa (Rubber Tree) | ResNet-152 | 4 |

---

## 🚀 Installation & Lancement

### Prérequis

- Python >= 3.10
- Un compte AWS avec accès au bucket S3 `backend-models-plants`

### En local

```bash
# Cloner le dépôt
git clone https://github.com/paulcoffi/backend_plants.git
cd backend_plants

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Renseigner AWS_ACCESS_KEY et AWS_SECRET_KEY dans .env

# Lancer l'API
uvicorn main:app --reload
```

L'API sera disponible sur [http://localhost:8000](http://localhost:8000).  
La documentation interactive Swagger est accessible sur [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🔑 Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
AWS_ACCESS_KEY=your_aws_access_key_id
AWS_SECRET_KEY=your_aws_secret_access_key
```

> ⚠️ Ne jamais commiter le fichier `.env`. Il est déjà listé dans `.gitignore`.

---

## 📡 Utilisation de l'API

Chaque endpoint accepte une image en `multipart/form-data` et retourne la prédiction avec les probabilités associées.

### Exemple avec `curl`

```bash
curl -X POST "http://localhost:8000/predict_model1_café_cacao" \
  -H "accept: application/json" \
  -F "img=@ma_plante.jpg"
```

### Exemple de réponse (modèles ResNet-152)

```json
{
  "prediction": "Coffee Leaf Rust",
  "probabilities": [[0.02, 0.91, 0.03, 0.01, 0.01, 0.01, 0.005, 0.005]]
}
```

### Exemple de réponse (modèles Hugging Face)

```json
{
  "prediction": "Tomato Bacterial Spot",
  "probability": 0.9823
}
```

---

## 🐳 Docker

```bash
# Construire l'image
docker build -t backend_plants .

# Lancer le conteneur (en passant les variables AWS)
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY=your_key \
  -e AWS_SECRET_KEY=your_secret \
  backend_plants
```

> Au démarrage, les modèles `.pth` sont automatiquement téléchargés depuis S3 si absents localement.

---

## ⚙️ Configuration CORS

L'API est configurée avec CORS permissif (toutes les origines autorisées) pour faciliter les appels depuis le frontend :

```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

En production, restreindre `allow_origins` à l'URL du frontend.

---

## 🌿 Classes de maladies par culture

Les modèles ont été entraînés sur les maladies suivantes, réparties par culture :

| Culture | Maladies détectées | Modèle | Architecture |
|---|---|---|---|
| **Cacao** | Pourriture noire, Moniliose, Mirides (capsides), Sain | `model1` | ResNet-152 |
| **Café** | Œil brun (*Cercospora coffeicola*), Mineuse des feuilles, Rouille (*Hemileia vastatrix*), Sain | `model1` | ResNet-152 |
| **Manioc** | Bactériose (*Xanthomonas axonopodis*), Cercosporiose (*Cercospora henningsii*), Acarien vert (*Mononychellus tanajoa*), Mosaïque (CMD), Sain | `model2` | ResNet-152 |
| **Anacarde** | Anthracnose (*Colletotrichum gloeosporioides*), Gommose (*Lasiodiplodia theobromae*), Mineuse des feuilles, Rouille rouge algaire, Sain | `model3` | ResNet-152 |
| **Tomate** | Mildiou / Brûlure foliaire, Enroulement foliaire (TYLCV), Septoriose, Verticilliose, Sain | `model4` | ViT (HuggingFace) |
| **Maïs** | Rouille commune, Brûlure foliaire, Tache grise des feuilles, Sain | `model6` | ViT (HuggingFace) |
| **Riz** | Pyriculariose (*Pyricularia oryzae*), Helminthosporiose (*Bipolaris oryzae*), Échaudure foliaire (*Microdochium oryzae*), Cercosporiose (*Cercospora janseana*), Bactériose foliaire (*Xanthomonas oryzae*), Sain | `model5` | ViT (HuggingFace) |
| **Hévéa** | Anthracnose, Dessèchement foliaire, Taches foliaires, Sain | `model7` | ResNet-152 |

> **Note :** Le café et le cacao sont regroupés dans un modèle unique (`model1`) car ils relèvent de la même filière agricole en Côte d'Ivoire.

---

## 📊 Performances des modèles

| Culture | Accuracy (train) | Accuracy (test) | F1 pondéré | Support (images) |
|---|---|---|---|---|
| Café-Cacao | 94% | 89.62% | 90% | 100 |
| Manioc | 98.34% | 90.57% | 91% | 7 510 |
| Anacarde | 98.53% | 92.38% | 95% | 1 310 |
| Tomate | 97.74% | 99.10% | 97% | 2 844 |
| Maïs | 96.30% | 96% | 96% | 838 |
| Riz | 98.86% | 96.53% | 97% | 1 480 |
| Hévéa | — | — | — | — |

> **Note Hévéa :** Le jeu de données hévéa présentait des images quasi-dupliquées (augmentations en amont), conduisant à une accuracy anormalement élevée (≈ 1). Le modèle sera réévalué sur des données terrain.

---

## 📂 Sources des données d'entraînement

Les datasets proviennent de **Mendeley Data** et de dépôts publics associés à des publications scientifiques. Ils sont distribués sous licences ouvertes (CC BY 4.0, CC BY-SA 4.0, CC0 1.0).

| Culture | DOI / Source | Licence |
|---|---|---|
| **Café-Cacao** | *(dataset interne — DOI en cours de publication)* | — |
| **Hévéa** | [10.17632/4kjz78m7x5.4](https://doi.org/10.17632/4kjz78m7x5.4) | CC BY 4.0 |
| **Maïs** (PlantDoc) | [10.17632/tywbtsjrjv.1](https://doi.org/10.17632/tywbtsjrjv.1) | CC BY 4.0 |
| **Tomate** | [10.17632/zfv4jj7855.1](https://doi.org/10.17632/zfv4jj7855.1) | CC BY 4.0 |
| **Manioc & Anacarde** | [10.1016/j.dib.2023.109306](https://doi.org/10.1016/j.dib.2023.109306) | CC BY-SA 4.0 |
| **Riz** | [10.17632/hx6f852hw4.2](https://doi.org/10.17632/hx6f852hw4.2) | CC BY 4.0 |

### Références scientifiques des modèles

- **ResNet** — He, K. et al. *Deep Residual Learning for Image Recognition*. CVPR, 2016. [doi:10.1109/CVPR.2016.90](https://doi.org/10.1109/CVPR.2016.90)
- **Vision Transformer (ViT)** — Dosovitskiy, A. et al. *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR, 2021. [arxiv:2010.11929](https://arxiv.org/abs/2010.11929)
- **Attention Mechanism** — Vaswani, A. et al. *Attention is All You Need*. NeurIPS, 2017. [arxiv:1706.03762](https://arxiv.org/abs/1706.03762)

---

## 🔗 Lien avec le frontend

Ce backend est consommé par le frontend **front_plantes**.

👉 [front_plantes](https://github.com/paulcoffi/front_plantes)
