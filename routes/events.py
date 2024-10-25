from flask import Blueprint, request, jsonify
from db import get_db_connexion, close_db_connexion
import sqlite3
events_bp = Blueprint("events", __name__)
import json
import db.events


@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    """Get an event in the database.

    Parameters
    ----------
    event_id
        id of the event to get

    Returns
    -------
    data
        all data about the event if correctly fetched
        a message "Event does not exist" if the event is not found in
            the database.
        an error message "Error: while fetching the event" if an error
            occurred while fetching the event.
    status_code
        200 if the event is correctly fetched
        404 if the event does not exist in the database
        500 if an error occurred while fetching the event
    """
    conn = get_db_connexion()
    cursor = conn.cursor()
    try:
        # Requête pour obtenir l'événement
        event = db.events.get_event(int(event_id),conn)
        if event:
            # Si l'événement existe, le retourner sous forme de JSON
            return jsonify({"event": dict(event)}), 200
        else:
            # Si l'événement n'existe pas
            return jsonify({"message": "Event does not exist"}), 404
    except sqlite3.Error as error:
        # Gérer les erreurs de base de données
        print(f"Error fetching event: {error}")
        return jsonify({"error": "Error: while fetching the event"}), 500
    finally:
        close_db_connexion(cursor, conn)



@events_bp.route("/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """Update an event in the database based on its id.
    The fields to update must be passed in the data of the PATCH request among
    the following (pass any of them):
        - spectator_username
        - type
        - status
        - gender
        - result_url
        - discipline_code
        - location_code
        - start_date
        - end_date

    Parameters
    ----------
    event_id
        id of the event to update

    Returns
    -------
    data
        a message "Done" if the event is updated correctly.
        a message "No field provided for update" if no field is found in the
            data passed in the request.
        a message "Event does not exist" if the event is not found in
            the database.
        an error message "Error: while updating the event" if an error
            occurred while updating the event.
    status_code
        200 if the event is updated correctly
        400 if no field is found in the data passed in the request
        404 if the event does not exist in the database
        500 if an error occurred while updating the event
    """
    data = request.get_json()


    if not data:
        return jsonify({"message": "No field provided for update"}), 400


    fields = data.keys()
    values = data.values()
    conn = get_db_connexion()
    cursor = conn.cursor()

    # Construction dynamique de la requête en fonction des champs fournis
    try:
        db.events.update_event_location(event_id,str(data['location_code']),conn)
    except:
        return jsonify({"message": "No location provided for update"}), 400    

    try:
        db.events.update_event_schedule(event_id,fields,values,conn)
        if cursor.rowcount == 0:
            return jsonify({"message": "Event does not exist"}), 404

        return jsonify({"message": "Done"}), 200
    except sqlite3.Error as error:
        print(f"Error updating event: {error}")
        return jsonify({"error": "Error: while updating the event"}), 500
    finally:
        close_db_connexion(cursor, conn)



@events_bp.route("/count/", methods=["GET"])
@events_bp.route("/count/<int:event_id>", methods=["GET"])
def get_spectator_count(event_id):
    """Get the number of spectators attending an event.

    Parameters
    ----------
    event_id
        Id of the event for which the number of spectators is collected.
        If None, count all event.

    Returns
    -------
    data
        the number of spectators attending the event (or all events) if correctly fetched.
        a message "Event does not exist" if the event is not found in
            the database.
        an error message "Error: while fetching the events" if an error
            occurred while fetching the event (or all events).
    status_code
        200 if the events are correctly fetched
        404 if the event does not exist in the database
        500 if an error occurred while fetching the event (or all events)
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    try:
        if event_id is None:
            # Requête pour compter tous les spectateurs sur tous les événements
            query = "SELECT SUM(spectator_count) FROM Event"
            cursor.execute(query)
        else:
            # Requête pour compter les spectateurs d'un événement spécifique
            query = "SELECT spectator_count FROM Event WHERE id = ?"
            cursor.execute(query, (event_id,))

        result = cursor.fetchone()

        if result:
            return jsonify({"spectator_count": result[0]}), 200
        else:
            return jsonify({"message": "Event does not exist"}), 404
    except sqlite3.Error as error:
        print(f"Error fetching spectator count: {error}")
        return jsonify({"error": "Error: while fetching the events"}), 500
    finally:
        close_db_connexion(cursor, conn)

