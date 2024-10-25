# Projet : API REST pour la Gestion des Tickets des Jeux Olympiques

Ce projet consiste en la création d'une API REST avec Flask pour gérer les tickets des événements des Jeux Olympiques, selon les exigences spécifiques du Comité International Olympique (CIO). Ce projet a été réalisé dans le cadre d'un TP de 8 sessions de 1h30, en binôme.

## Objectifs et Fonctionnalités

- **Authentification des utilisateurs** : Chaque spectateur est authentifié avec un nom d'utilisateur et un mot de passe.
- **Gestion des tickets** : Les spectateurs peuvent acheter plusieurs tickets, chacun donnant accès à un événement dans une zone spécifique d’un lieu, avec un nombre illimité d'accompagnants.
- **Gestion des événements** : Les événements sont planifiés avec des dates, heures, disciplines et lieux spécifiques. Le CIO peut surveiller le statut de chaque événement pour notifier les spectateurs en cas d'annulation.
- **Consultation des résultats** : Les résultats des compétitions sont accessibles via des URLs spécifiques pour chaque événement.

## Structure du Projet

- **Back-end** : Développé en Python avec Flask pour créer des routes HTTP et gérer les requêtes.
- **Base de données** : Utilisation de SQLite3 pour stocker les informations sur les spectateurs, les tickets, les événements et les lieux.
- **Sécurité** : Hashage des mots de passe avec la bibliothèque `bcrypt` et gestion de l'authentification via des tokens avec `PyJWT`.

## Installation

1. **Cloner le dépôt** :
```bash
git clone https://github.com/Armanddevvacc/jotickets.git
```
2. **Naviguer dans le répertoire du projet** :
```bash
cd jotickets
```
3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```
4. **Lancer l'application** :
```bash
python app.py
```

## Utilisation

Routes principales de l'API
- **Spectateurs**
GET /spectators : Récupère la liste de tous les spectateurs.
POST /spectators : Ajoute un nouveau spectateur dans la base de données.
PATCH /spectators/{username}/password : Met à jour le mot de passe d'un spectateur.
- **Tickets**
POST /tickets : Ajoute un nouveau ticket.
GET /tickets/{spectator_id} : Récupère tous les tickets d'un spectateur.
- **Événements**
POST /events : Ajoute un nouvel événement.
GET /events : Récupère la liste de tous les événements.
PATCH /events/{event_id} : Met à jour les informations d'un événement.
- **Sécurité de l'API**
Hashage des mots de passe : Les mots de passe sont hashés avant d'être stockés en base de données.
Authentification par token : Un token est généré à la connexion d'un utilisateur via /login et doit être inclus dans les requêtes pour accéder aux routes protégées.

## Fonctionnalités Avancées

### 1.Initialisation de la base de données :
Fonction create_database() dans ./db/init.py pour créer la structure des tables.
Fonction populate_database() pour charger les données depuis un fichier CSV.
### 3.Traitement des données :
Transformation des données pour ajouter la ville par défaut (Paris) quand elle n’est pas mentionnée dans la colonne de localisation.
### 4.Configuration et Sécurité :
Stockage des mots de passe sous forme de hash grâce à bcrypt.
Utilisation de tokens JWT pour sécuriser les accès aux routes sensibles.
Exemple de requête avec token

```http
GET localhost:5000/spectators HTTP/1.1
Authorization: Bearer <token> 
```
