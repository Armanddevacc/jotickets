import app_utils
import sqlite3

def insert_spectator(username,password, conn):
    """Inserts a spectator into to the database.

    Parameters
    ----------
    spectator: a dictionnary
        Spectator personal data: spectator["username"] and spectator["password"].
    cursor:
        The object used to query the database.

    Returns
    -------
    bool
        True if no error occurs, False otherwise.
    """
    try:
        # The spectator is described by two attributes: username and password.
        # The values of these attributes are available in the dictionary spectator, one of the parameters of this function.
        # So, we need to write our insert query in such a way that the values are obtained from the dictionary spectator.
        # Our insert query contains two question marks (?) that indicate that the values will be specified later.
        #
        #  IMPORTANT:
        #
        # * The query assumes that you called Spectator the table with the spectator personal data. If you gave it another name, CHANGE the query accordingly.
        #
        # * The query assumes that in your table Spectator the columns are defined in this order:
        # username, password.
        # IF THE ORDER in which you created the columns IS DIFFERENT, CHANGE this variable accordingly.

        query_insert_spectator = "INSERT INTO Spectator (username, password) VALUES (?, ?)"
        cursor = conn.cursor()
        cursor.execute(query_insert_spectator, (username, password))
        conn.commit()
        cursor.close()
    except sqlite3.IntegrityError as error:
        print(
            f"An integrity error occurred while insert the spectator: {error}")
        return False
    except sqlite3.Error as error:
        print(
            f"A database error occurred while inserting the spectator: {error}")
        return False

    return True


def get_spectator(username, cursor):
    """Get a spectator from the database based on its username and a list of
    the tickets bought by the spectator.

    Parameters
    ----------
    username: string
        Spectator username.
    cursor:
        The object used to query the database.

    Returns
    -------
    dict
        The spectator username, password and tickets if no error occurs, None otherwise.
    """
    try:
        query_get_spectator = "SELECT username FROM Spectator WHERE username = ?"
        cursor.execute(query_get_spectator, (username,))

        spectator = cursor.fetchone()

        query_get_tickets = "SELECT Ticket_Code FROM Ticket WHERE Username = ?"
        cursor.execute(query_get_tickets, (username,))

        tickets = cursor.fetchall()

    except sqlite3.IntegrityError as error:
        print(
            f"An integrity error occurred while fetching the spectator: {error}")
        return None
    except sqlite3.Error as error:
        print(
            f"A database error occurred while fetching the spectator: {error}")
        return None

    return {
        "username": spectator["username"],
        "tickets": tickets
    }


def get_spectator_data(username, cursor):
    try:
        query_get_spectator = "SELECT * FROM Spectator WHERE username = ?"
        cursor.execute(query_get_spectator, (username,))

        spectator = cursor.fetchone()



    except sqlite3.IntegrityError as error:
        print(
            f"An integrity error occurred while fetching the spectator: {error}")
        return None
    except sqlite3.Error as error:
        print(
            f"A database error occurred while fetching the spectator: {error}")
        return None

    return dict(spectator)


def get_spectators(cursor):
    """Get all spectators from the database.

    Parameters
    ----------
    cursor:
        The object used to query the database.

    Returns
    -------
    list
        The list of all the spectator if no error occurs, None otherwise.
    """
    try:
        query_get_spectators = "SELECT username FROM Spectator"
        cursor.execute(query_get_spectators, [])

    except sqlite3.IntegrityError as error:
        print(
            f"An integrity error occurred while fetching the spectators: {error}")
        return None
    except sqlite3.Error as error:
        print(
            f"A database error occurred while fetching the spectators: {error}")
        return None

    return cursor.fetchall()


def update_password(username, password,conn):
    """Update the password of a spectator.

    Parameters
    ----------
    username: string
        Spectator username.
    password: bytes
        New password
    cursor:
        The object used to query the database.

    Returns
    -------
    bool
        True if no error occurs, False otherwise.
    """
    try:
        cursor = conn.cursor()
        query = """
        UPDATE Spectator
        SET password = ?
        WHERE username = ?; """
        cursor.execute(query, (app_utils.hash_password(password), username))
        conn.commit()
        if cursor.rowcount()== 0:
            return False
        return True
    except:
        return False


