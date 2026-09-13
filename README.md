# Plant Disease Classification API

API de classification de maladies végétales développée avec FastAPI et des modèles de Deep Learning (ResNet-152 et Vision Transformers).

L'application analyse une image de feuille et prédit une maladie parmi plusieurs classes selon la culture concernée. Les modèles sont stockés sur AWS S3 et téléchargés à la demande par le backend.

Auteur : Paul Coffi

## Sommaire

- [Présentation](#présentation)
- [Cultures prises en charge](#cultures-prises-en-charge)
- [Modèles utilisés](#modèles-utilisés)
- [Endpoints de l'API](#endpoints-de-lapi)
- [Exemple d'utilisation](#exemple-dutilisation)
- [Gestion des modèles (AWS S3)](#gestion-des-modèles-aws-s3)
- [Architecture du projet](#architecture-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement de l'API](#lancement-de-lapi)
- [Docker](#docker)
- [CORS](#cors)
- [Classes de maladies par culture](#classes-de-maladies-par-culture)
- [Performances des modèles](#performances-des-modèles)
- [Sources des données d'entraînement](#sources-des-données-dentraînement)
- [Références scientifiques](#références-scientifiques)
- [Projet frontend associé](#projet-frontend-associé)
- [Pistes d'amélioration](#pistes-damélioration)
- [Licence](#licence)

## Présentation

Le projet a pour objectif de mettre à disposition une API capable d'identifier des maladies végétales à partir d'images de feuilles, afin d'être intégrée à une application web ou mobile.

Fonctionnement général :

```
Image de la plante
        |
        v
    API FastAPI
        |
        v
Sélection du modèle
        |
        v
Modèle de Deep Learning
        |
        v
    Inférence
        |
        v
Maladie prédite + probabilité
```

## Cultures prises en charge

| Culture   | Endpoint associé |
|-----------|-------------------|
| Café      | `/predict_model1_café_cacao` |
| Cacao     | `/predict_model1_café_cacao` |
| Manioc    | `/predict_model2_cassava` |
| Anacarde  | `/predict_model3_cashew` |
| Tomate    | `/predict_model4_tomato` |
| Riz       | `/predict_model5_rice` |
| Maïs      | `/predict_model6_maize` |
| Hévéa     | `/predict_model7_rubber_tree` |

Chaque culture est associée à un modèle de classification et à un ensemble de classes correspondant aux maladies pouvant être détectées, ou à un état sain.

## Modèles utilisés

### ResNet-152

Plusieurs modèles reposent sur l'architecture ResNet-152, un réseau de neurones convolutif profond bien adapté à la classification d'images.

### Vision Transformers (ViT)

D'autres modèles utilisent une architecture Vision Transformer, intégrée via la bibliothèque Hugging Face Transformers.

Le backend fait ainsi cohabiter deux familles d'architectures de Deep Learning au sein d'une même API. Elles ne retournent pas exactement le même format de réponse (voir la section Exemple d'utilisation).

## Endpoints de l'API

| Endpoint | Culture | Architecture | Classes |
|---|---|---|---|
| `POST /predict_model1_café_cacao` | Café / Cacao | ResNet-152 | 8 |
| `POST /predict_model2_cassava` | Manioc | ResNet-152 | 5 |
| `POST /predict_model3_cashew` | Anacarde | ResNet-152 | 5 |
| `POST /predict_model4_tomato` | Tomate | Vision Transformer | 5 |
| `POST /predict_model5_rice` | Riz | Vision Transformer | 6 |
| `POST /predict_model6_maize` | Maïs | Vision Transformer | 4 |
| `POST /predict_model7_rubber_tree` | Hévéa | ResNet-152 | 4 |

Chaque endpoint reçoit une image en `multipart/form-data` (champ `img`) et effectue l'inférence avec le modèle correspondant.

La documentation interactive Swagger permet de tester chaque endpoint directement depuis le navigateur (voir la section Lancement de l'API).

## Exemple d'utilisation

Requête avec curl :

```
curl -X POST "http://localhost:8000/predict_model1_café_cacao" \
  -H "accept: application/json" \
  -F "img=@ma_plante.jpg"
```

Réponse pour les modèles ResNet-152 :

```
{
  "prediction": "Coffee Leaf Rust",
  "probabilities": [
    [0.02, 0.91, 0.03, 0.01, 0.01, 0.01, 0.005, 0.005]
  ]
}
```

Réponse pour les modèles Hugging Face (ViT) :

```
{
  "prediction": "Tomato Bacterial Spot",
  "probability": 0.9823
}
```

## Gestion des modèles (AWS S3)

Les modèles de Deep Learning ne sont pas versionnés dans le repository afin d'éviter d'alourdir Git avec des artefacts volumineux. Ils sont conservés dans un bucket AWS S3 et téléchargés par le backend au moment où ils sont nécessaires.

```
                AWS S3
                  |
                  | téléchargement
                  v
          Modèles de Deep Learning
                  |
                  v
            FastAPI Backend
                  |
                  v
               Inférence
                  |
                  v
              Prédiction
```

## Architecture du projet

```
backend_plants/
|
|-- models/                # Modèles de Deep Learning (.pth, téléchargés depuis S3)
|
|-- café_cacao/             # Encodeurs de classes - modèle café/cacao
|-- cassava/                # Encodeurs de classes - modèle manioc
|-- cashew/                 # Encodeurs de classes - modèle anacarde
|-- Rubber tree/            # Encodeurs de classes - modèle hévéa
|
|-- main.py                 # Point d'entrée de l'application FastAPI
|-- prediction.py           # Chargement des modèles et logique de prédiction
|
|-- requirements.txt        # Dépendances Python
|-- Dockerfile              # Configuration de l'image Docker
|-- .env                    # Variables d'environnement (à créer, non versionné)
|-- README.md
```

## Technologies utilisées

- Python 3.10 ou supérieur
- FastAPI, pour l'API REST
- PyTorch et torchvision, pour l'inférence des modèles ResNet-152
- Hugging Face Transformers, pour l'inférence des modèles Vision Transformer
- AWS S3 et boto3, pour le stockage et le téléchargement des modèles
- Uvicorn, comme serveur ASGI
- Docker, pour la conteneurisation
- python-dotenv, pour la gestion des variables d'environnement

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Un compte AWS avec accès au bucket S3 contenant les modèles
- Docker, si l'application doit être exécutée en conteneur

### Cloner le repository

```
git clone https://github.com/boucingwithbud/backend_plants.git
cd backend_plants
```

### Créer un environnement virtuel

```
python -m venv venv
```

Sous Linux ou macOS :

```
source venv/bin/activate
```

Sous Windows :

```
venv\Scripts\activate
```

### Installer les dépendances

```
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine du projet :

```
AWS_ACCESS_KEY=your_aws_access_key_id
AWS_SECRET_KEY=your_aws_secret_key
```

Ces variables permettent au backend d'accéder au bucket AWS S3 contenant les modèles.

Le fichier `.env` ne doit jamais être versionné dans Git. Il est déjà listé dans `.gitignore`.

## Lancement de l'API

```
uvicorn main:app --reload
```

L'API est alors disponible à l'adresse :

http://localhost:8000

La documentation interactive Swagger, générée automatiquement par FastAPI, est accessible à :

http://localhost:8000/docs

Elle permet de tester chaque endpoint directement depuis l'interface, sans écrire de code.

## Docker

Construire l'image :

```
docker build -t backend_plants .
```

Lancer le conteneur :

```
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY=your_key \
  -e AWS_SECRET_KEY=your_secret \
  backend_plants
```

Au démarrage, les modèles nécessaires sont téléchargés depuis AWS S3 s'ils ne sont pas déjà présents localement.

## CORS

Le backend utilise CORS afin de permettre les appels depuis une application cliente, web ou mobile.

En développement, la configuration peut être permissive :

```
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

En production, il est recommandé de restreindre les origines autorisées aux seuls domaines réellement utilisés par l'application cliente, par exemple :

```
allow_origins=["https://votre-frontend.example.com"]
```

## Classes de maladies par culture

| Culture | Maladies détectées | Modèle | Architecture |
|---|---|---|---|
| Café | Œil brun (Cercospora coffeicola), Mineuse des feuilles, Rouille (Hemileia vastatrix), Sain | model1 | ResNet-152 |
| Cacao | Pourriture noire, Moniliose, Mirides (capsides), Sain | model1 | ResNet-152 |
| Manioc | Bactériose (Xanthomonas axonopodis), Cercosporiose (Cercospora henningsii), Acarien vert (Mononychellus tanajoa), Mosaïque (CMD), Sain | model2 | ResNet-152 |
| Anacarde | Anthracnose (Colletotrichum gloeosporioides), Gommose (Lasiodiplodia theobromae), Mineuse des feuilles, Rouille rouge algaire, Sain | model3 | ResNet-152 |
| Tomate | Mildiou / Brûlure foliaire, Enroulement foliaire (TYLCV), Septoriose, Verticilliose, Sain | model4 | Vision Transformer |
| Riz | Pyriculariose (Pyricularia oryzae), Helminthosporiose (Bipolaris oryzae), Échaudure foliaire (Microdochium oryzae), Cercosporiose (Cercospora janseana), Bactériose foliaire (Xanthomonas oryzae), Sain | model5 | Vision Transformer |
| Maïs | Rouille commune, Brûlure foliaire, Tache grise des feuilles, Sain | model6 | Vision Transformer |
| Hévéa | Anthracnose, Dessèchement foliaire, Taches foliaires, Sain | model7 | ResNet-152 |

Le café et le cacao sont regroupés dans un modèle unique (model1), ces deux cultures relevant souvent de la même filière agricole.

## Performances des modèles

| Culture | Accuracy (train) | Accuracy (test) | F1 pondéré | Support (images) |
|---|---|---|---|---|
| Café-Cacao | 94% | 89.62% | 90% | 100 |
| Manioc | 98.34% | 90.57% | 91% | 7 510 |
| Anacarde | 98.53% | 92.38% | 95% | 1 310 |
| Tomate | 97.74% | 99.10% | 97% | 2 844 |
| Riz | 98.86% | 96.53% | 97% | 1 480 |
| Maïs | 96.30% | 96% | 96% | 838 |
| Hévéa | — | — | — | — |

Note sur l'Hévéa : le jeu de données présentait des images quasi-dupliquées, issues d'augmentations réalisées en amont, ce qui a conduit à une accuracy anormalement élevée sur le jeu de test. Le modèle sera réévalué sur des données terrain avant toute utilisation en production.

## Sources des données d'entraînement

Les jeux de données proviennent de Mendeley Data et de dépôts publics associés à des publications scientifiques, distribués sous licences ouvertes.

| Culture | DOI / Source | Licence |
|---|---|---|
| Café-Cacao | dataset interne, DOI en cours de publication | — |
| Hévéa | 10.17632/4kjz78m7x5.4 | CC BY 4.0 |
| Maïs (PlantDoc) | 10.17632/tywbtsjrjv.1 | CC BY 4.0 |
| Tomate | 10.17632/zfv4jj7855.1 | CC BY 4.0 |
| Manioc et Anacarde | 10.1016/j.dib.2023.109306 | CC BY-SA 4.0 |
| Riz | 10.17632/hx6f852hw4.2 | CC BY 4.0 |

## Références scientifiques

- ResNet : He, K. et al., Deep Residual Learning for Image Recognition, CVPR, 2016 (doi:10.1109/CVPR.2016.90)
- Vision Transformer (ViT) : Dosovitskiy, A. et al., An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale, ICLR, 2021 (arXiv:2010.11929)
- Attention Mechanism : Vaswani, A. et al., Attention is All You Need, NeurIPS, 2017 (arXiv:1706.03762)



Auteur : Paul Coffi
