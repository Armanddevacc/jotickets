from flask import Blueprint, request, jsonify
from app_utils import check_spectator, check_token, generate_token

auth_bp = Blueprint("login", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login a spectator and provide a token for future requests to the API

    Returns
    -------
    data
        a token to authenticate future request to the API.
        an error message "No username or password provided" if the
            username or password is not provided
        an error message "Error: while authenticating spectator" if an error
            occured while authenticating the spectator.
    status_code
        200 if the token is correctly provided
        400 if the username or password is not provided
        500 if an error occured while authenticating the spectator
    """
    # TODO
    return jsonify({"message": "TODO"})
