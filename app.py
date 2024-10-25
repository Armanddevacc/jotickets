from flask import Flask

from db import init_database

from routes.spectators import spectators_bp
from routes.events import events_bp
from routes.tickets import tickets_bp


def create_app():
    """Create a Flask application and add blueprints with all routes.

    Returns
    -------
    app
        the application created
    """
    # Create the default app
    app = Flask(__name__)

    # Add a first blueprints with all routes for the API
    # Take a look at the file ./routes/spectators.py to have more
    # details about the routes you have access to.
    app.register_blueprint(spectators_bp, url_prefix="/spectators")
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(tickets_bp, url_prefix="/tickets")


    return app


# Entry point of the application
if __name__ == "__main__":
    app = create_app()
    init_database()
    app.run(port=5001, debug=False)
