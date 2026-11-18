'''
Createand modify events data
'''
# Import
import pandas as pd
from database.database import clean


def get_events_for_display(conn):
    """
    Pull slimmed down version of table for summary display on events page
    """
    df = pd.read_sql_query(
    '''
    SELECT 
        event_id AS "Event ID",
        event_name AS "Event",
        event_date AS "Event Date",
        num_adults + num_kids AS "Guests",
        event_status AS "Status"
    FROM events
    ''', conn,
    )

    # Change date to new format
    df['Event Date'] = pd.to_datetime(df['Event Date'])
    df['Event Date'] = df['Event Date'].dt.strftime("%m/%d/%Y")

    return df


def get_selected_event(conn, event_id):
    df = pd.read_sql_query(
        "SELECT * FROM events WHERE event_id = ?", conn, params=(event_id,)
    )
    return df.iloc[0] if not df.empty else None


def create_event(conn, 
                 event_name, 
                 event_date, 
                 event_time,
                 event_serving_time,
                 num_adults, 
                 num_kids,
                 event_notes,
                 event_status):
    
    event_name = clean(event_name, collapse=True)
    event_notes = clean(event_notes)
    event_time = event_time.strftime("%H:%M") if event_time else None
    event_serving_time = \
    event_serving_time.strftime("%H:%M") if event_serving_time else None
    cursor = conn.execute(
        """INSERT INTO events (event_name, 
                                event_date, 
                                event_time,
                                event_serving_time,
                                num_adults, 
                                num_kids, 
                                event_notes, 
                                event_status) 
                                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)""",
        (event_name, 
         event_date, 
         event_time,
         event_serving_time,
         num_adults, 
         num_kids, 
         event_notes, 
         event_status)
    )
    conn.commit()
    return cursor.lastrowid


def edit_event(conn, 
               event_id, 
               event_name, 
               event_date, 
               event_time,
               event_serving_time,
               num_adults, 
               num_kids, 
               event_notes, 
               event_status):
    """
    Modify content of a logged event record
    """
    event_name = clean(event_name, collapse=True)
    event_notes = clean(event_notes)
    event_time = event_time.strftime("%H:%M") if event_time else None
    event_serving_time = \
    event_serving_time.strftime("%H:%M") if event_serving_time else None
    conn.execute(
        """
        UPDATE events
        SET event_name = ?, 
        event_date = ?, 
        event_time = ?,
        event_serving_time = ?,
        num_adults = ?, 
        num_kids = ?, 
        event_notes = ?, 
        event_status = ?
        WHERE event_id = ?;
        """,
        (event_name, 
         event_date, 
         event_time,
         event_serving_time,
         num_adults, 
         num_kids, 
         event_notes, 
         event_status,
         event_id)
    )
    conn.commit()


def copy_event(conn, event_id):
    """
    Duplicate an event and link the copy to the same menus
    """
    event_id = int(event_id)
    try:
        cur = conn.execute(
            """
            INSERT INTO events (event_name, 
                                event_date,
                                event_time, 
                                event_serving_time,
                                num_adults, 
                                num_kids, 
                                event_notes, 
                                event_status)
            SELECT 'Copy of ' || event_name, 
                                event_date, 
                                event_time,
                                event_serving_time,
                                num_adults, 
                                num_kids, 
                                event_notes, 
                                event_status 
                                
            FROM events
            WHERE event_id = ?
            """,
            (event_id,),
        )
        new_id = cur.lastrowid

        conn.execute(
            """
            INSERT INTO event_menus (event_id, menu_id)
            SELECT ?, menu_id FROM event_menus WHERE event_id = ?
            """,
            (new_id, event_id),
        )

        conn.commit()
        return new_id
    except Exception:
        conn.rollback()
        raise


def delete_event(conn, event_id):
    cur = conn.execute(
        """
        DELETE FROM events WHERE event_id = ?
        """, (int(event_id),)
                )
    conn.commit()
    return cur.rowcount