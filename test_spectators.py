import db.spectators
from db import get_db_connexion, close_db_connexion


def print_spectators():
    """Print the spectators in the database in the console."""
    conn = get_db_connexion()
    cursor = conn.cursor()

    spectators = db.spectators.get_spectators(cursor)
    print("Spectators in database:", [dict(spectator)
          for spectator in spectators])

    close_db_connexion(cursor, conn)


def insert_hubert(conn):
    """Inserts a spectator into the database.

    Parameters
    ----------
    cursor:
        The object used to query the database.

    Returns
    -------
    bool
        True if the spectator could be inserted, False otherwise.
    """

    # Personal data of spectator Hubert
    hubert = {"username": "hubert", "password": "117"}

    print("Inserting spectator Hubert...")
    if db.spectators.insert_spectator(hubert, conn):
        print("Hubert added successfully !")
        return True
    else:
        print("Impossible to add Hubert ...")
        return False


########## TEST FUNCTIONS ##########


def test_insert_spectator():
    print("## TEST: insert a spectator")
    # Open a connexion to the database.
    conn = get_db_connexion()

    # Get the cursor for the connection. This object is used to execute queries
    # in the database.
    cursor = conn.cursor()

    # Insert spectator Hubert
    insert_hubert(conn)
    

    # Close connexion
    close_db_connexion(cursor, conn)


def test_update_password_existing_spectator():
    print("\n## TEST: update a spectator that is in the database")


    try:
        # Update spectator hubert
        update_ok = db.spectators.update_password("hubert", "1233334")

        # Print results from update
        print("Update successful:", update_ok)
    except NotImplementedError as error:
        print("update_password() not implemented")


def test_update_password_non_existing_spectator():
    print("\n## TEST: update a spectator that does not exist in the database")
    conn = get_db_connexion()
    cursor = conn.cursor()

    # Update spectator bond
    try:
        update_ok = db.spectators.update_password("bond", "12", cursor)
        # Print results from update
        print("Update successful:", update_ok)
        print("Number of modified rows in the database:", cursor.rowcount)
    except NotImplementedError as error:
        print("update_password() not implemented")

    close_db_connexion(cursor, conn)


if __name__ == "__main__":

    print_spectators()
    test_insert_spectator()
    print_spectators()
