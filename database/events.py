'''
Create, edit, and get events data
'''
# Import
import pandas as pd

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
        num_adults + num_kids AS "Guests"
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
                 num_adults, 
                 num_kids,
                 num_hearty_eaters,
                 need_kids_menu, 
                 dietary_needs,
                 event_complete,
                 event_notes):
    conn.execute(
        "INSERT INTO events (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_complete, event_notes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_complete, event_notes)
    )
    conn.commit()


def edit_event(conn, event_id, event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_complete, event_notes):
    """
    Modify content of a logged event record
    """
    conn.execute(
        """
        UPDATE events
        SET event_name = ?, event_date = ?, num_adults = ?, num_kids = ?, num_hearty_eaters = ?, need_kids_menu = ?, dietary_needs = ?, event_complete = ?, event_notes = ?
        WHERE event_id = ?;
        """,
        (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_complete, event_notes, event_id)
    )
    conn.commit()


def delete_event(conn, event_id):
    cur = conn.execute(
        """
        DELETE FROM events WHERE event_id = ?
        """, (event_id,)
                 )
    conn.commit()
    return cur.rowcount