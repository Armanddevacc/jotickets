from flask import Blueprint, jsonify, request
from db import get_db_connexion, close_db_connexion
import sqlite3
import db.spectators
import db.tickets

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/<int:ticket_id>")
def get_ticket(ticket_id):
    """Get a ticket in the database.

    Parameters
    ----------
    ticket_id
        id of the ticket to get

    Returns
    -------
    data
        all data about the ticket if correctly fetched
        a message "Ticket does not exist" if the ticket is not found in
            the database.
        an error message "Error: while fetching the ticket" if an error
            occured while fetching the ticket.
    status_code
        200 if the ticket is correctly fetched
        404 if the ticket does not exist in the database
        500 if an error occured while fetching the ticket
    """
    conn = get_db_connexion()
    cursor = conn.cursor()
    try:
        ticket = db.tickets.get_ticket(ticket_id,conn)
        

        if cursor.rowcount == 0:
            return jsonify({"message": "Ticket does not exist"}), 404
        return jsonify({"event": dict(ticket)}), 200
    except: 
        return jsonify({"message": "Error: while fetching the ticket"}), 500
    finally:
        close_db_connexion(cursor, conn)


@tickets_bp.route("/<int:ticket_id>/purchase", methods=["PATCH"])
def purchase_ticket(ticket_id):
    """Assign a ticket to a spectator.
    The fields to update the owner must be passed in the data of the POST request among
    the following (pass all of them):
        - username
        - password

    Parameters
    ----------
    ticket_id
        id of the ticket to get

    Returns
    -------
    data
        a message "Done" if the spectator is assigned correctly to the ticket.
        a message "No spectator username provided for assignment" if no the field
            username is not found in the request data
        a message "Ticket does not exist" if the ticket is not found in
            the database.
        a message "Spectator does not exist" if the spectator is not found in the
            database
        an error message "Error: while fetching the ticket" if an error
            occured while fetching the ticket.
    status_code
        200 if the tickets are correctly fetched
        400 if no the field username is not found in the request data
        404 if the ticket does not exist in the database
        404 if the spectator does not exist in the database
        500 if an error occured while fetching the ticket
    """

    conn = get_db_connexion()
    cursor = conn.cursor()
    data = request.get_json()
    if not data:
        return jsonify({"message": "No spectator username provided for assignment"}), 400
    try:
        db.tickets.get_ticket(ticket_id,conn)
        if cursor.rowcount == 0:
            return jsonify({"message": "Ticket does not exist"}), 404
    except: 
        return jsonify({"message": "error while fetching the ticket"}), 500

    try:
        db.spectators.get_spectator(data['Username'], cursor)
        db.tickets.update_ticket(data['Username'],ticket_id,conn)
        if cursor.rowcount == 0:
            return jsonify({"message": "Spectator does not exist"}), 404
        return jsonify({"message": "Done"}), 200
    except: 
        return jsonify({"message": "error while fetching the ticket"}), 500
    finally:
        close_db_connexion(cursor, conn)
