'''
Create and modify list data
'''
# Import
import pandas as pd


def create_list(conn,
                list_name,
                apply_to_all,
                list_notes,
                list_status):
    conn.execute(
        "INSERT INTO custom_lists (list_name, apply_to_all, list_notes, list_status) VALUES(?, ?, ?, ?)",
        (list_name, apply_to_all, list_notes, list_status)
    )
    conn.commit()


def get_lists_for_display(conn):
    """
    Pull slimmed down version of table for summary display on lists page
    """
    df = pd.read_sql_query(
    '''
    SELECT 
        list_id AS "List ID",
        list_name AS "List",
        apply_to_all AS "Standard List",
        list_status AS "List"
    FROM custom_lists
    ''', conn,
    )

    return df
