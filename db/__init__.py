import sys
import os
from app_utils import load_config

import sqlite3
import csv


def get_db_connexion():
    # Loads the app config into the dictionary app_config.
    app_config = load_config()
    print(1)
    if not app_config:
        print("Error: while loading the app configuration")
        return None

    # From the configuration, gets the path to the database file.
    db_file = app_config["db"]
    # Open a connection to the database.
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    return conn


def close_db_connexion(cursor, conn):
    """Close a database connexion and the cursor.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    """
    cursor.close()
    conn.close()


def transform_csv(old_csv_file_name, new_csv_file_name):
    """Write a new CSV file based on the input CSV file by adding
    new columns to obtain a CSV file that is easier to read.

    Parameters
    ----------
    csv_file_name
        Name of the CSV file to transform
    new_csv_file_name
        Name of the new CSV file
    """
    with open(old_csv_file_name, mode='r', newline='') as old_csv, open(new_csv_file_name, mode='w', newline='', encoding='utf-8') as new_csv:
        #read from csv
        reader = csv.DictReader(old_csv)

        # Create a new list of header excluding 'event_medal'
        new_fieldnames = [field for field in reader.fieldnames if field != 'event_medal']
        new_fieldnames.append('city')

        # write (from csv)
        writer = csv.DictWriter(new_csv, fieldnames=new_fieldnames)

        # Write the header (new fieldnames)
        writer.writeheader()

        # Write the rows, excluding the 'event_medal' field
        for row in reader:
            row.pop('event_medal', None)  # Remove 'event_medal' from the row
            location_description = row['location_description']
            city = 'Paris'
            try:
                description = location_description.split(",")
                row['location_description']=description[0]

                city=description[1]
                
            except:
                print("no city mentionned")
            row["city"]=city
            writer.writerow(row)

    


def create_database(cursor, conn):
    """Creates the Paris 2024 database

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.

    Returns
    -------
    bool
        True if the database could be created, False otherwise.
    """

    # We open a transaction.
    # A transaction is a sequence of read/write statements that
    # have a permanent result in the database only if they all succeed.
    #
    # More concretely, in this function we create many tables in the database.
    # The transaction is therefore a sequence of CREATE TABLE statements such as :
    #
    # BEGIN
    # CREATE TABLE XXX
    # CREATE TABLE YYY
    # CREATE TABLE ZZZ
    # ....
    #
    # If no error occurs, all the tables are permanently created in the database.
    # If an error occurs while creating a table (for instance YYY), no table will be created, even those for which
    # the statement CREATE TABLE has already been executed (in this example, XXX).
    #
    # When we start a transaction with the statement BEGIN, we must end it with either COMMIT
    # or ROLLBACK.
    #
    # * COMMIT is called when no error occurs. After calling COMMIT, the result of all the statements in
    # the transaction is permanetly written to the database. In our example, COMMIT results in actually creating all the tables
    # (XXX, YYY, ZZZ, ....)
    #
    # * ROLLBACK is called when any error occurs in the transaction. Calling ROLLBACK means that
    # the database is not modified (in our example, no table is created).
    #
    #
    cursor.execute("BEGIN")

    # Create the tables.
    tables = {
        "Spectator": """
            CREATE TABLE Spectator(
            username VARCHAR(255) PRIMARY KEY,
            password BINARY(256)
            );
            """,
        "Ticket": """
        CREATE TABLE Ticket (
            Ticket_Code INT PRIMARY KEY,
            Username VARCHAR(255),
            Number_of_People INT,
            Event_Code INT, 
            FOREIGN KEY (Username) REFERENCES Spectator(Username) ON DELETE CASCADE,
            FOREIGN KEY (Event_Code) REFERENCES Event(Event_Code) ON DELETE CASCADE

            );
            """,
        "Venue": """
        CREATE TABLE Venue (
            Venue_Code VARCHAR(255),
            Venue_Name VARCHAR(255) NOT NULL,
            City_Name VARCHAR(255) NOT NULL
        );
        """,

        "Location": """
        CREATE TABLE Location (
            Location_Code VARCHAR(255),
            Venue_Code VARCHAR(255),
            Location_Description VARCHAR(255),
            FOREIGN KEY (Venue_Code) REFERENCES Venue(Venue_Code) ON DELETE CASCADE
        );
        """,
        "Discipline":"""
        CREATE TABLE Discipline (
            Discipline_Code VARCHAR(255),
            Discipline_Name VARCHAR(255) NOT NULL
        );""",

       "Event": """
        CREATE TABLE Event (
            Event_Code INT PRIMARY KEY,
            Start_Date VARCHAR(255) NOT NULL,
            End_Date VARCHAR(255) NOT NULL,
            Competition_Phase VARCHAR(255),
            Type VARCHAR(255),
            Gender VARCHAR(255),
            Status VARCHAR(255),
            Results_URL VARCHAR(255),
            Location_Code VARCHAR(255),
            Discipline_Code VARCHAR(255),
            FOREIGN KEY (Location_Code) REFERENCES Location(Location_Code) ON DELETE CASCADE,
            FOREIGN KEY (Discipline_Code) REFERENCES Discipline(Discipline_Code) ON DELETE CASCADE
        );
        """

    }
    try:
        # To create the tables, we call the function cursor.execute() and we pass it the
        # CREATE TABLE statement as a parameter.
        # The function cursor.execute() can raise an exception sqlite3.Error.
        # That's why we write the code for creating the tables in a try...except block.
        for tablename in tables:
            print(f"Creating table {tablename}...", end=" ")
            cursor.execute(tables[tablename])
            print("OK")

    ###################################################################

    # Exception raised when something goes wrong while creating the tables.
    except sqlite3.Error as error:
        print("An error occurred while creating the tables: {}".format(error))
        # IMPORTANT : we rollback the transaction! No table is created in the database.
        conn.rollback()
        # Return False to indicate that something went wrong.
        return False

    # If we arrive here, that means that no error occurred.
    # IMPORTANT : we must COMMIT the transaction, so that all tables are actually created in the database.
    conn.commit()
    print("Database created successfully")
    # Returns True to indicate that everything went well!
    return True


def populate_database(cursor, conn, csv_file_name):
    """Populate the database with data in a CSV file.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    csv_file_name
        Name of the CSV file where the data are.

    Returns
    -------
    bool
        True if the database is correctly populated, False otherwise.
    """
    with open(csv_file_name,'r') as csv_file:

        reader = csv.DictReader(csv_file)


        i=0
        for row in reader:
            # Insertion dans la table Spectator

            ## rien

            
            # Insertion dans la table Ticket

            ## rien
            
            # Insertion dans la table Venue

            # Insertion dans la table Venue avec placeholders
            query = """
                INSERT INTO Venue (Venue_Code, Venue_Name, City_Name)
                VALUES (?, ?, ?)
                """
            cursor.execute(query, (row['venue_code'], row['venue'], row['city']))

            # Insertion dans la table Location avec placeholders
            query = """
                INSERT INTO Location (Location_Code, Venue_Code, Location_Description)
                VALUES (?, ?, ?)
                """
            cursor.execute(query, (row['location_code'], row['venue_code'], row['location_description']))

            # Insertion dans la table Discipline avec placeholders
            query = """
                INSERT INTO Discipline (Discipline_Code, Discipline_Name)
                VALUES (?, ?)
                """
            cursor.execute(query, (row['discipline_code'], row['discipline']))

            # Insertion dans la table Event avec placeholders
            query = """
                INSERT INTO Event (Event_Code, Start_Date, End_Date, Competition_Phase, 
                Type, Gender, Status, Results_URL, Location_Code, Discipline_Code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(query, (i,
                row['start_date'], row['end_date'], row['phase'], row['event_type'],
                row['gender'], row['status'], row['url'], row['location_code'], row['discipline_code']
            ))
            i+=1


        # Commit des transactions dans la base de données
        conn.commit()
        print("Données insérées avec succès!")

    



    return False

def init_database():
    """Initialise the database by creating the database
    and populating it.
    """
    try:
        conn = get_db_connexion()
        
        # The cursor is used to execute queries to the database.
        cursor = conn.cursor()
        
        # Drop the existing tables if they exist
        # cursor.execute(f"DROP TABLE IF EXISTS Spectator;")
        # cursor.execute(f"DROP TABLE IF EXISTS Ticket;")
        # cursor.execute(f"DROP TABLE IF EXISTS Venue;")   
        # cursor.execute(f"DROP TABLE IF EXISTS Location;")   
        # cursor.execute(f"DROP TABLE IF EXISTS Discipline;")   
        # cursor.execute(f"DROP TABLE IF EXISTS Event;")   

        conn.commit()

        # Create the database with the updated table structure
        create_database(cursor, conn)

        # Populate the database with CSV data
        populate_database(cursor, conn, 'data/schedules2.csv')

        # Closes the connection to the database
        close_db_connexion(cursor, conn)
    except Exception as e:
        print("Error: Database cannot be initialised:", e)
