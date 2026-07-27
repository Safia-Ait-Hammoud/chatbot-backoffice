# Chatbot Back-Office

Back-office d'administration pour la gestion de la base de connaissances et des feedbacks utilisateur du chatbot.

## Description

Le back-office permet de :
- Gérer le contenu de la base de connaissances par produit (FAQ, documentation)
- Suivre et analyser les retours utilisateurs (feedbacks) sur les réponses du chatbot
- Déclencher et suivre la réindexation des contenus dans la base vectorielle

## Stack technique

- **Backend** : FastAPI (Python)
- **Frontend** : React 
- **Base de données** : MongoDB 
- **Base vectorielle** : Qdrant 
- **Stockage fichiers** : Amazon S3 

## Prérequis

- Docker et Docker Compose
- Python 3.11+

## Installation

1. Cloner le dépôt :
```bash
   git 
   cd chatbot-backoffice
```

2. Copier le fichier d'environnement et configurer les variables :
```bash
   cp .env.example .env
```

3. Démarrer les services (MongoDB, Qdrant) :
```bash
   docker compose up -d
```

4. Créer un environnement virtuel et installer les dépendances :
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   pip install -r requirements.txt
```

5. Lancer l'application :
```bash
   uvicorn app.main:app --reload
```

6. L'API est accessible sur `http://localhost:8000` et la documentation interactive sur `http://localhost:8000/docs`.

## Variables d'environnement

Voir `.env.example` pour la liste complète des variables requises (identifiants MongoDB, URL Qdrant, etc.).

## Vérification de l'installation

- MongoDB : `docker exec -it backoffice-mongodb mongosh -u <user> -p <password> --authenticationDatabase admin`
- Qdrant : ouvrir `http://localhost:6333/dashboard`
- API FastAPI : ouvrir `http://localhost:8000/docs`


## Auteurs

- AIT HAMMOUD Safia
- ERRAGUIBI Abdelilah

## Statut du projet

Projet de Fin d'Année (PFA) — en cours de développement.