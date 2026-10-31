'''
Create and modify menu data
'''
# Import
import pandas as pd

def create_menu(conn,
                menu_name,
                menu_notes,
                menu_status):
    conn.execute(
        "INSERT INTO menus (menu_name, menu_notes, menu_status) VALUES(?, ?, ?)",
        (menu_name, menu_notes, menu_status)
    )
    conn.commit()


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
