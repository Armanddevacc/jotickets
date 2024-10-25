def insert_event(id,status,phase,type,result_url,gender,start_date,end_date,day,displine_code,location_code,conn):
    cursor = conn.cursor()
    query = """
    INSERT INTO Event (Event_Code, Start_Date, End_Date, Competition_Phase, 
    Type, Gender, Status, Results_URL, Location_Code, Discipline_Code)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, ( id, str(day+" "+start_date),str(day+" "+end_date), phase, type, gender, status, result_url, location_code, displine_code))
    conn.commit()


def get_events(conn):
    cursor = conn.cursor()
    query = """
    SELECT * FROM Event
    """
    cursor.execute(query)
    return cursor.fetchall()

def get_event(id,conn):
    cursor = conn.cursor()
    query = """
    SELECT * FROM Event WHERE Event_Code = ?
    """
    cursor.execute(query,(id,))
    return cursor.fetchone()


def update_event_location(id, location_code,conn):
    cursor = conn.cursor()
    query = """
    UPDATE Event
    SET Location_Code = ?
    WHERE Event_Code = ?
    """
    cursor.execute(query, (location_code, id))
    conn.commit()



def update_event_schedule(id, fields, values, conn):
    cursor = conn.cursor()
    query = f"UPDATE Event SET {', '.join([f'{field} = ?' for field in fields])} WHERE Event_Code = ?"
    print(query)
    values = list(values)
    values.append(id)
    cursor.execute(query, values)
    conn.commit()





def update_event_date(event_id, date_start, date_end ,conn):
    cursor = conn.cursor()
    query = """
    UPDATE Event
    SET Start_Date = ?
    AND End_Date = ?
    WHERE Event_Code = ?
    """
    cursor.execute(query, (date_start, date_end, event_id))
    conn.commit()


def update_event_result_url(event_id, result_url,conn):
    cursor = conn.cursor()
    query = """
    UPDATE Event
    SET Results_URL = ?
    WHERE Event_Code = ?
    """
    cursor.execute(query, (result_url, event_id))
    conn.commit()


def update_event_status(id, event_status,conn):
    cursor = conn.cursor()
    query = """
    UPDATE Event
    SET Results_URL = ?
    WHERE Event_Code = ?
    """
    cursor.execute(query, (event_status, id))
    conn.commit()
