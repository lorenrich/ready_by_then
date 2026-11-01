'''
Create and modify menu data
'''
# Import
import pandas as pd

def create_menu(conn,
                menu_name,
                menu_notes,
                menu_status):
    cursor = conn.execute(
        "INSERT INTO menus (menu_name, menu_notes, menu_status) VALUES(?, ?, ?)",
        (menu_name, menu_notes, menu_status)
        )
    conn.commit()
    return cursor.lastrowid


def get_menus_for_display(conn):
    """
    Pull slimmed down version of table for summary display on menus page
    """
    df = pd.read_sql_query(
    '''
    SELECT 
        menu_id AS "Menu ID",
        menu_name AS "Menu",
        menu_status AS "Status"
    FROM menus
    ''', conn,
    )

    return df


def get_selected_menu(conn, menu_id):
    df = pd.read_sql_query(
        "SELECT * FROM menus WHERE menu_id = ?", conn, params=(menu_id,)
    )
    return df.iloc[0] if not df.empty else None


def get_selected_menu_recipes(conn, menu_id):
    menu_id = int(menu_id)
    return conn.execute(
        """
        SELECT r.recipe_id, r.recipe_name, r.recipe_status, mr.course
        FROM menu_recipes mr
        JOIN recipes r ON r.recipe_id = mr.recipe_id
        WHERE mr.menu_id = ?
        ORDER BY mr.course, r.recipe_name
        """,
        (menu_id, menu_id),
    ).fetchall()


def edit_menu(conn,
              menu_name,
              menu_notes,
              menu_status,
              menu_id,  
            ):
    """
    Modify content of a logged menu record
    """
    cursor = conn.execute(
        """
        UPDATE menus
        SET menu_name = ?, menu_notes = ?, menu_status = ?
        WHERE menu_id = ?;
        """,
        (int(menu_name),
         menu_notes,
         menu_status,
         menu_id
         )
        )
    conn.commit()
    return cursor.rowcount


def copy_menu(conn, menu_id):
    """
    Duplicate a menu and its recipe list. The copy is not attached to any event. Returns the new menu_id.
    """
    menu_id = int(menu_id)
    try:
        cur = conn.execute(
            """
            INSERT INTO menus (menu_name, menu_notes, menu_status)
            SELECT 'Copy of ' || menu_name, menu_notes, menu_status
            FROM menus
            WHERE menu_id = ?
            """,
            (menu_id,),
        )
        new_id = cur.lastrowid

        conn.execute(
            """
            INSERT INTO menu_recipes (menu_id, recipe_id, course)
            SELECT ?, recipe_id, course FROM menu_recipes WHERE menu_id = ?
            """,
            (new_id, menu_id),
        )

        conn.commit()
        return new_id
    except Exception:
        conn.rollback()
        raise


def delete_menu(conn, menu_id):
    cursor = conn.execute(
        """
        DELETE FROM menu_recipes WHERE menu_id = ?
        """, (int(menu_id),)
                 )
    conn.commit()
    return cursor.rowcount


def save_menu(conn, menu_id, recipes):
    menu_id = int(menu_id)
    try:
        # Delete any existing data
        conn.execute("""DELETE from menus WHERE menu_id = ?""", (int(menu_id),))

        for recipe in recipes:
            # Insert into menu_recipes
            conn.execute(
                """
                INSERT INTO menu_recipes (menu_id, recipe_id, course) VALUES (?, ?, ?)
                """,
                (menu_id, recipe_id, course),
                )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_menu_events(conn, menu_id):
    menu_id = int(menu_id)
    events = conn.execute(
        """
        SELECT e.event)id, e.event_name
        FROM event_menus em
        JOIN events e ON e.event_id = em.event_id
        WHERE em.menu_id = ?
        ORDER BY e.event_name
        """,
        (menu_id,),
    ).fetchall()

    return events
