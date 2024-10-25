from flask import Blueprint, request, jsonify
from db import get_db_connexion, close_db_connexion
import db.spectators
import sqlite3
spectators_bp = Blueprint("spectators", __name__)


@spectators_bp.route("/", methods=["GET"])
def get_all_spectators():
    """Fetch all spectators from the database.

    Returns
    -------
    status_code
        200 by default if no error occured
        500 if an error occured while fetching the spectators
    data
        spectators as a json if no error occurs (can be empty if no spectators)
        an error message if an error occured while fetching the spectators.
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    all_spectators = db.spectators.get_spectators(cursor)
    if all_spectators == None:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return "Error: while fetching spectators", 500
    conn.commit()
    close_db_connexion(cursor, conn)
    return jsonify({"spectators": [dict(spectator)["username"] for spectator in all_spectators]})


@spectators_bp.route("/<spectator_username>", methods=["GET"])
def get_spectator(spectator_username):
    """Fetch a single spectator from the database based on its username.

    Parameters
    ----------
    spectator_username
        username of the spectator (as defined in the database)

    Returns
    -------
    data
        spectator as a json if the spectator is in the database
        an error message "This spectator does not exists" if the spectator requested
            is not in the database
        an error message "Error: while fetching spectator" if an error occured
            while fetching the spectator.
    status_code
        200 if the spectator is correctly fetched
        404 if the query to the database was a success but the spectator
                is not in the database
        500 if an error occured while fetching the spectator
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    try:
        
        # Requête pour récupérer le spectateur par nom d'utilisateur


        
        
        # Récupérer le résultat
        spectator = db.spectators.get_spectator(spectator_username,cursor)
        

        if spectator is not None:
            # Si le spectateur existe, renvoyer les données
            return jsonify({'username': spectator['username']}), 200
        else:
            # Si le spectateur n'existe pas
            return jsonify({"erreur": "This spectator does not exists"}), 404

    except sqlite3.Error as error:
        # Gérer les erreurs de base de données
        print(f"error while fetching spectator: {error}")
        return jsonify({"erreur": "Error: while fetching spectator"}), 500

    finally:
        # Fermer la connexion à la base de données
        close_db_connexion(cursor, conn)




@spectators_bp.route("/<spectator_username>", methods=["PATCH"])
def patch_password(spectator_username):
    """Patch the password of an spectator.
    The password must be passed in the data of the POST request.

    Parameters
    ----------
    spectator_username
        username of the spectator (as defined in the database)

    Returns
    -------
    data
        spectator as a json if the spectator is in the database
        a message "Password not provided" if the password is not in
            the request
        an error message "Error: while updating password" if an error
            occured while updating the password.
    status_code
        200 if the password is correctly modified
        404 if no password is provided in the request
        500 if an error occured while updating the password
    """
    # Récupérer les données de la requête
    data = request.get_json()

    # Vérifier si le mot de passe est fourni
    if 'password' not in data:
        return jsonify({"error": "Password not provided"}), 404

    new_password = data['password']

    conn = get_db_connexion()
    cursor= conn.cursor()

    try:
        # Requête pour mettre à jour le mot de passe
        db.spectators.update_password(spectator_username,new_password,conn)
        


        # Si tout s'est bien passé, renvoyer un message de succès
        return jsonify({"message": "Password updated successfully"}), 200

    except sqlite3.Error as error:
        # Gérer les erreurs de base de données
        print(f"An error occurred while updating the password: {error}")
        return jsonify({"error": "Error: while updating password"}), 500

    finally:
        # Fermer la connexion à la base de données
        close_db_connexion(cursor, conn)




@spectators_bp.route("/", methods=["POST"])
def add_spectator():
    """Add an spectator to the database.
    The username and password must be passed in the data of the POST request.

    Returns
    -------
    data
        a message "Done" if the spectator is correctly added
        a message "Username or password not provided" if the password or
            username is not in the data of the POST request
        an error message "Error: while adding a new spectator" if an error occured
            while updating the password
    status_code
        200 if the spectator was added to the database
        404 if no username and password are provided in the request
        500 if an error occured while updating the password
    """
    data = request.get_json()
    
    new_username = data['username']
    new_password = data['password']

    conn = get_db_connexion()

    try:
        # Requête pour mettre à jour le mot de passe
        db.spectators.insert_spectator(new_username,new_password,conn)

        # Valider les changements
        conn.commit()

        # Si tout s'est bien passé, renvoyer un message de succès
        return jsonify({"message": "done"}), 200

    except sqlite3.Error as error:
        # Gérer les erreurs de base de données
        print(f"An error occurred while adding the user: {error}")
        return jsonify({"error": "Error: while adding the user"}), 500

    finally:
        # Fermer la connexion à la base de données
        conn.close()

