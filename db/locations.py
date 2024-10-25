

def insert_location(code, description, venue_code, conn):
    #adds a location in the database.

    
    # Open a connexion to the database.
    cursor = conn.cursor()
    

    query = """
    INSERT INTO Location (Location_Code, Venue_Code, Location_Description) 
    VALUES (?, ?, ?)
    """
    cursor.execute(query,(code, venue_code, description))

    conn.commit()

    print(f"Location {code} description inserted")
    


def update_location_description(code, description,conn):
    # Met à jour la description d'un emplacement dans la base de données.
    
    # Ouvre une connexion à la base de données.
    cursor = conn.cursor()
    

    # Requête de mise à jour de la description de l'emplacement
    query = """
    UPDATE Location
    SET Location_Description = ?
    WHERE Location_Code = ?
    """
    cursor.execute(query, (description, code))


    conn.commit()

    print(f"Location {code} description updated")
    

def get_locations(conn):
    # Récupère toutes les localisations de la base de données.
    
    # Ouvre une connexion à la base de données.

    # Obtenir le curseur pour la connexion.
    cursor = conn.cursor()
    
    # Requête de sélection de toutes les localisations
    query = """
    SELECT Location_Code, Venue_Code, Location_Description
    FROM Location
    """
    cursor.execute(query)

    # Récupère tous les résultats de la requête
    locations = cursor.fetchall()

    # Affiche les résultats
    for location in locations:
        print(f"Code: {location[0]}, Venue Code: {location[1]}, Description: {location[2]}")

    # Fermeture de la connexion à la base de données
    
    return locations