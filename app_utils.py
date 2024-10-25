import bcrypt
# import jwt
# import datetime
from functools import wraps
from flask import request, jsonify
import db
import db.spectators


CONFIG_FILE = "config/config"


def load_config():
    """Loads the application configuration from the configuration file
    into a dictionary.

    Returns
    -------
    A dictionary.
        The application configuration.
    """

    config = {}

    with open(CONFIG_FILE, mode='r', newline='') as Config:
        read = Config.read()
        liste = read.split('\n') ##sépare item
        for e in liste:
            e=e.split(',') #sépare clés et values
            config[e[0]]=e[1]
    return config


def hash_password(plain_password):
    """Hash a password

    Parameters
    ----------
    plain_password : str
        plain password to hash

    Returns
    -------
    hashed_password : str
        A hashed password
    """
    # genere un salt utiliser pour faire un hash random
    salt = bcrypt.gensalt()

    # Hash le mdp avec bcrypt
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')



def check_password(plain_password, hashed_password):
    """Check the plain password against its hashed value

    Parameters
    ----------
    plain_password : str
        the plain password to check
    hashed_password : str
        a password hash to check if it is the hash of the plain password

    Returns
    -------
    bool
        True if hashed_password is the hash of plain_password, False otherwise
    """
    # Hash the plain password and compare it to the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



import bcrypt

def check_spectator(username, plain_password):
    from db import get_db_connexion, close_db_connexion

    """Authenticate a spectator based on its username and a plain password.

    Parameters
    ----------
    username : str
        the spectator username
    plain_password : str
        the plain password to check

    Returns
    -------
    bool
        True if the password is associated to the spectator, False otherwise
    """

    conn = get_db_connexion()
    cursor = conn.cursor()
    
    data = db.spectators.get_spectator_data(username, cursor)
    
    if not data:
        close_db_connexion()
        return False
    
    # Extract the hashed password from the retrieved data
    hashed_password = data["password"]  # Assuming the hashed password is in the second column
    
    # Check the provided plain password against the hashed password
    if check_password(plain_password,hashed_password):
        close_db_connexion()
        return True

    close_db_connexion()
    return False



def generate_token(username):
    """Generate a token with a username and an expiracy date of 1h.

    Parameters
    ----------
    username
        the spectator username

    Returns
    -------
    token
        the generated token based on the username and an expiracy date of 1h.
    """
    # TODO - Generate a token using the secret key in the config file
    return ""


def check_token(token):
    """Check the validity of a token.

    Parameters
    ----------
    token
        the token to check

    Returns
    -------
    payload
        The payload associated with the token if the token is correctly decoded.
        An error if the token is expired or invalid
    """
    try:
        # TODO: Decode the token using the secret key in the configuration file
        payload = {}
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError


def token_required(f):
    """A decorator to specify which routes need a token validation."""

    @wraps(f)
    def decorated(*args, **kwargs):
        """Define the behaviour of a route when a token validation is required.
        """
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = check_token(token)
            if not "username" in payload or not "exp" in payload:
                return jsonify({"error": "Invalid token"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated

