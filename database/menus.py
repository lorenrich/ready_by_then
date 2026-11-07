'''
Create and modify menu data
'''
# Import
import pandas as pd
import streamlit as st

# Constants
COURSES = [
    "Appetizer",
    "Main",
    "Side",
    "Dessert",
    "Drink",
    "Other"
]

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
        (menu_id,),
    ).fetchall()


def get_menu_events(conn, menu_id):
    menu_id = int(menu_id)
    events = conn.execute(
        """
        SELECT e.event_id, e.event_name
        FROM event_menus em
        JOIN events e ON e.event_id = em.event_id
        WHERE em.menu_id = ?
        ORDER BY e.event_name
        """,
        (menu_id,),
    ).fetchall()

    return events


def get_event_menus(conn, event_id):
    event_id = int(event_id)
    event_menus = conn.execute(
    """
    SELECT m.menu_id, m.menu_name, m.menu_status
    FROM event_menus em
    JOIN menus m ON m.menu_id = em.menu_id
    WHERE em.event_id = ?
    ORDER BY m.menu_name
    """,
    (event_id,),
    ).fetchall()

    return event_menus


def remove_menu_from_event(conn, event_id, menu_id):
    cursor = conn.execute (
        "DELETE FROM event_menus WHERE event_id = ? AND menu_id = ?",
        (int(event_id), int(menu_id)),
    )
    conn.commit()
    return cursor.rowcount


def add_menu_to_event(conn, event_id, menu_id):
    cursor = conn.execute(
        "INSERT OR IGNORE INTO event_menus (event_id, menu_id) VALUES (?, ?)",
        (int(event_id), int(menu_id)),
    )
    conn.commit()
    return cursor.rowcount


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
        (menu_name, menu_notes, menu_status, int(menu_id))
        )
    conn.commit()
    return cursor.rowcount
 

def copy_menu(conn, menu_id):
    """
    Duplicate a menu and its recipe and item lists. The copy is not attached to any event. Returns the new menu_id.
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

        conn.execute(
            """
            INSERT INTO menu_items (menu_id, item_id, course, amount, unit, scales_with_guests, prep_timing)
            SELECT ?, item_id, course, amount, unit, scales_with_guests, prep_timing FROM menu_items WHERE menu_id = ?
            """,
            (new_id, menu_id)
        )

        conn.commit()
        return new_id
    except Exception:
        conn.rollback()
        raise


def delete_menu(conn, menu_id):
    menu_id = int(menu_id)
    try:
        conn.execute(
            """
            DELETE FROM menu_recipes WHERE menu_id = ?
            """, (int(menu_id),)
                    )
        conn.execute(
            """
            DELETE FROM event_menus WHERE menu_id = ?
            """, (int(menu_id),)
                    )
        conn.execute(
            """
            DELETE FROM menu_items WHERE menu_id = ?
            """, (int(menu_id),)
                    )
        cursor = conn.execute(
            """
            DELETE FROM menus WHERE menu_id = ?
            """, (int(menu_id),)
                    )
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise


def save_menu(conn, menu_id, recipes):
    menu_id = int(menu_id)
    try:
        conn.execute("DELETE FROM menu_recipes WHERE menu_id = ?", (menu_id,))
        for item in recipes:
            conn.execute(
                "INSERT INTO menu_recipes (menu_id, recipe_id, course) VALUES (?, ?, ?)",
                (menu_id, int(item["recipe_id"]), item["course"]),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def format_item(recipe_name, recipe_status):
    if recipe_status == 'Complete':
        return recipe_name
    else:
        return f"{recipe_name} ({recipe_status})"


def render_menu(recipes, items=()):
    """
    recipes: list of (recipe_id, recipe_name, recipe_status, course) tuples
    items: list of (item_id, item_name, course) tuples
    """
    # Turn recipes and items into pairs
    entries = []
    for _, name, status, course in recipes:
        entries.append((course, format_item(recipe_name=name, recipe_status=status)))
    for _, name, course in items:
        entries.append((course, name))

    if not entries:
        st.caption("No items on this menu yet.")
        return

    # Guard for recipes and items without courses
    if not any(course for course, _ in entries):
        for _, text in entries:
            st.write(text)
        return

    # Group by course
    by_course = {}
    for course, text in entries:
        by_course.setdefault(course or "Unassigned", []).append(text)

    order = [c for c in COURSES if c in by_course] + [c for c in by_course if c not in COURSES]
    for course in order:
        label_col, items_col = st.columns([1, 4])
        label_col.markdown(f"**{course}**")
        with items_col:
            for text in by_course[course]:
                st.write(text)

