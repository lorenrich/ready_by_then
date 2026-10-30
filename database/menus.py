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
 
