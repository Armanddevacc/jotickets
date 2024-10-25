def insert_venue(venue_code, venue, city,conn):

    cursor = conn.cursor()
    query = '''
    INSERT INTO Venue (Venue_Code, Venue_name, City_Name)
    VALUES (?,?,?)
    '''
    cursor.execute(query, (venue_code, venue, city))
    conn.commit()


def get_venues(cursor):
    query = "SELECT Venue_Name FROM Venues"

    cursor.execute(query)
    return cursor.fetchall()

