from flask import Blueprint, request, jsonify
import db.events
from db import get_db_connexion, close_db_connexion
import sqlite3

data_bp = Blueprint("data", __name__)

@data_bp.route("/events")
def get_events():
    """Get all events in the database.

    Returns
    -------
    data
        all events in the database
        an error message "Error: while fetching events" if an error occurred
            while fetching the events.
    status_code
        200 if the events are correctly fetched
        500 if an error occurred while fetching the events
    """
    conn = get_db_connexion()

    try:
        events = db.events.get_events(conn)
        return jsonify({"events": [dict(event) for event in events]}), 200
    except sqlite3.Error as error:
        print(f"An error occurred while fetching the events: {error}")
        return jsonify({"error": "Error: while fetching events"}), 500
    finally:
        conn.close()


@data_bp.route("/locations")
def get_locations():
    """Get all locations in the database.

    Returns
    -------
    data
        all locations in the database
        an error message "Error: while fetching locations" if an error occurred
            while fetching the locations.
    status_code
        200 if the locations are correctly fetched
        500 if an error occurred while fetching the locations
    """
    conn = get_db_connexion()

    try:
        locations = db.events.get_locations(conn)  # Assuming you have a function for this
        return jsonify({"locations": [dict(location) for location in locations]}), 200
    except sqlite3.Error as error:
        print(f"An error occurred while fetching the locations: {error}")
        return jsonify({"error": "Error: while fetching locations"}), 500
    finally:
        conn.close()


@data_bp.route("/venues")
def get_venues():
    """Get all venues in the database.

    Returns
    -------
    data
        all venues in the database
        an error message "Error: while fetching venues" if an error occurred
            while fetching the venues.
    status_code
        200 if the venues are correctly fetched
        500 if an error occurred while fetching the venues
    """
    conn = get_db_connexion()

    try:
        venues = db.events.get_venues(conn)  # Assuming you have a function for this
        return jsonify({"venues": [dict(venue) for venue in venues]}), 200
    except sqlite3.Error as error:
        print(f"An error occurred while fetching the venues: {error}")
        return jsonify({"error": "Error: while fetching venues"}), 500
    finally:
        conn.close()


@data_bp.route("/disciplines")
def get_disciplines():
    """Get all disciplines in the database.

    Returns
    -------
    data
        all disciplines in the database
        an error message "Error: while fetching disciplines" if an error occurred
            while fetching the disciplines.
    status_code
        200 if the disciplines are correctly fetched
        500 if an error occurred while fetching the disciplines
    """
    conn = get_db_connexion()

    try:
        disciplines = db.events.get_disciplines(conn)  # Assuming you have a function for this
        return jsonify({"disciplines": [dict(discipline) for discipline in disciplines]}), 200
    except sqlite3.Error as error:
        print(f"An error occurred while fetching the disciplines: {error}")
        return jsonify({"error": "Error: while fetching disciplines"}), 500
    finally:
        conn.close()
