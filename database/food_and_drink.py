'''
Create and edit food and drink items
'''

# Import
import pandas as pd

DEFAULT_ITEM_TYPES = [
    'Food',
    'Drink'
]


def get_items_for_display(conn):
    """
    Pull slimmed down version of table for summary display on food and drink page
    """
    df = pd.read_sql_query(
    '''
    SELECT 
        item_id AS "Item ID",
        item_name AS "Item",
        item_type AS "Type"
    FROM food_and_drinks
    ''', conn,
    )

    return df


def get_items_for_menu_selection(conn):
    """
    Pull items from database to allow user to tag to menu
    """
    df = pd.read_sql_query(
        '''
        SELECT
            item_id AS "Item ID",
            item_name AS "Item",
            item_type AS "Type"
        FROM food_and_drinks
        ''', conn,
    )

    df["Add to Menu"] = False

    return df


def create_item(conn,
                item_name,
                item_type):
    cursor = conn.execute(
        "INSERT INTO food_and_drinks (item_name, item_type) VALUES ( ?, ?)",
        (item_name, item_type)
    )
    conn.commit()
    return cursor.lastrowid


def get_selected_item(conn, item_id):
    df = pd.read_sql_query(
        "SELECT * FROM food_and_drinks WHERE item_id = ?", conn, params=(item_id,)
    )
    return df.iloc[0] if not df.empty else None


def edit_item(conn,
              item_name,
              item_type, 
              item_id,   
            ):
    """
    Modify content of a logged item record
    """
    conn.execute(
        """
        UPDATE food_and_drinks
        SET item_name = ?, item_type = ?
        WHERE item_id = ?;
        """,
        (item_name,
         item_type,
         item_id
         )
    )
    conn.commit()


def delete_item(conn, item_id):
    cursor = conn.execute(
        """
        DELETE FROM food_and_drinks WHERE item_id = ?
        """, (int(item_id),)
                 )
    conn.commit()
    return cursor.rowcount


def get_item_usage(conn, item_id):
    item_id = int(item_id)
    menus = conn.execute(
        """
        SELECT f.menu_id, f.menu_name
        FROM menu_items m
        JOIN food_and_drinks f ON f.item_id = m.item_id
        WHERE m.menu_id = ?
        ORDER BY f.menu_name
        """,
        (item_id,),
    ).fetchall()

    events = conn.execute(
        """
        SELECT f.event_id, f.event_name
        FROM event_items e
        JOIN food_and_drinks f ON f.item_id = e.item_id
        WHERE e.event_id = ?
        ORDER BY f.event_name
        """,
        (item_id,),
    ).fetchall()

    return menus, events


def get_or_create_item(conn, name):
    name = name.strip()
    row = conn.execute(
        "SELECT item_id FROM food_and_drinks WHERE item_name = ? COLLATE NOCASE",
        (name,),
    ).fetchone()
    if row:
        return row[0]
    cur = conn.execute("INSERT INTO food_and_drinks (item_name) VALUES (?)", (name,))
    return cur.lastrowid


def save_menu_items(conn, menu_id, items):
    menu_id = int(menu_id)
    try:
        conn.execute("DELETE FROM menu_items WHERE menu_id = ?", (menu_id,))

        for item in items:
            item_id = get_or_create_item(conn, item["name"])
            conn.execute(
                """
                INSERT INTO menu_items (menu_id, item_id, course, amount, unit, scales_with_guests, prep_timing)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (menu_id, item_id, item["course"], item["amount"], item["unit"],
                 item["scales"], item["prep"]),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

def get_selected_menu_items(conn,
                            menu_id):
    menu_id = int(menu_id)
    return conn.execute(
        """
        SELECT i.item_id, i.item_name, mi.course
        FROM menu_items mi
        JOIN food_and_drinks i on i.item_id = mi.item_id
        WHERE mi.menu_id = ?
        ORDER BY mi.course, i.item_name
        """,
        (menu_id,),
    ).fetchall()

    