'''
Createand modify events data
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
                 num_adults, 
                 num_kids,
                 num_hearty_eaters,
                 need_kids_menu, 
                 dietary_needs,
                 event_occurred,
                 event_notes,
                 event_status):
    cursor = conn.execute(
        "INSERT INTO events (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_occurred, event_notes, event_status) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_occurred, event_notes, event_status)
    )
    conn.commit()
    return cursor.lastrowid


def edit_event(conn, event_id, event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_occurred, event_notes, event_status):
    """
    Modify content of a logged event record
    """
    conn.execute(
        """
        UPDATE events
        SET event_name = ?, event_date = ?, num_adults = ?, num_kids = ?, num_hearty_eaters = ?, need_kids_menu = ?, dietary_needs = ?, event_occurred = ?, event_notes = ?, event_status = ?
        WHERE event_id = ?;
        """,
        (event_name, event_date, num_adults, num_kids, num_hearty_eaters, need_kids_menu, dietary_needs, event_occurred, event_notes, event_status, event_id)
    )
    conn.commit()


def copy_event(conn, event_id):
    """
    Duplicate an event and link the copy to the same menus. Returns the new event_id.
    """
    event_id = int(event_id)
    try:
        cur = conn.execute(
            """
            INSERT INTO events (event_name, event_date, num_adults, num_kids, num_hearty_eaters,
                                need_kids_menu, dietary_needs, event_occurred, event_notes, event_status)
            SELECT 'Copy of ' || event_name, event_date, num_adults, num_kids, num_hearty_eaters,
                   need_kids_menu, dietary_needs, 0, event_notes, event_status
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