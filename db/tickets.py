def insert_ticket(ticket_Code, maxGuests, event_Code, spectator_username, conn):
    cursor = conn.cursor()
    query = '''
    INSERT INTO Ticket (Ticket_Code, Event_Code, Number_of_People, Username)
    VALUES (?,?,?,?)
    '''
    cursor.execute(query, (ticket_Code, event_Code, maxGuests, spectator_username))
    conn.commit()


def get_tickets(spectator_username,conn):
    cursor = conn.cursor()
    query = '''
    SELECT Ticket_Code FROM ticket Where Username = ? 
    '''
    cursor.execute(query, (spectator_username,))
    return cursor.fetchall()

def get_ticket(id,conn):
    cursor = conn.cursor()
    query = '''
    SELECT * FROM ticket Where Ticket_Code = ? 
    '''
    cursor.execute(query, (id,))
    return cursor.fetchone()

def update_ticket(spectator_username,ticket_id,conn):
    cursor = conn.cursor()
    query = """
    UPDATE Ticket
    SET Username = ?
    WHERE Ticket_Code = ?
    """
    
    cursor.execute(query, (spectator_username, ticket_id))
    conn.commit()




