def insert_disciplines(discipline_code, discipline,conn):
    cursor = conn.cursor()
    query = '''
    INSERT INTO Discipline (Discipline_Code, Discipline_Name)
    VALUES (?,?,?)
    '''
    cursor.execute(query, (discipline_code, discipline))
    conn.commit()


def get_discipline(ticket_id, conn):
        cursor = conn.cursor() 
        query = "SELECT Discipline_Name FROM Discipline d JOIN Event e ON e.Discipline_Code=d.Discipline_Code JOIN Tickets t ON t.event_Code = e.Event_Code WHERE t.ticket_id = ?"
        cursor.execute(query, [ticket_id])

def get_disciplines(cursor):
    query_get_disciplines = "SELECT Discipline_Name FROM Discipline"
    cursor.execute(query_get_disciplines, [])
    return cursor.fetchall()

