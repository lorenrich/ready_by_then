'''
Create and modify recipe data
'''
# Import
import pandas as pd

DEFAULT_RECIPE_TYPES = [
    'Entree',
    'Side',
    'Dessert'
]

DEFAULT_PREHEAT_UNITS = [
    'Celsius',
    'Fahrenheit'
]


def get_recipes_for_display(conn):
    """
    Pull slimmed down version of table for summary display on recipes page
    """
    df = pd.read_sql_query(
    '''
    SELECT 
        recipe_id AS "Recipe ID",
        recipe_name AS "Recipe",
        recipe_type AS "Type",
        recipe_status AS "Status"
    FROM recipes
    ''', conn,
    )

    return df


def create_recipe(conn,
                  recipe_name,
                  recipe_type, 
                  recipe_yield,
                  recipe_cooking_vessel,
                  recipe_preheat_temp,
                  recipe_preheat_unit,
                  recipe_preheat_time,
                  recipe_cook_time,
                  recipe_source,
                  recipe_notes,
                  recipe_status):
    conn.execute(
        "INSERT INTO recipes (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source, recipe_notes, recipe_status) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source, recipe_notes, recipe_status)
    )
    conn.commit()


def get_selected_recipe(conn, recipe_id):
    df = pd.read_sql_query(
        "SELECT * FROM recipes WHERE recipe_id = ?", conn, params=(recipe_id,)
    )
    return df.iloc[0] if not df.empty else None


def edit_recipe(conn, 
                recipe_id, 
                recipe_name,
                recipe_type, 
                recipe_yield,
                recipe_cooking_vessel,
                recipe_preheat_temp,
                recipe_preheat_unit,
                recipe_preheat_time,
                recipe_cook_time,
                recipe_source,
                recipe_notes,
                recipe_status
                ):
    """
    Modify content of a logged recipe record
    """
    conn.execute(
        """
        UPDATE recipes
        SET recipe_name = ?, recipe_type = ?, recipe_yield = ?, recipe_cooking_vessel = ?, recipe_preheat_temp = ?, recipe_preheat_unit = ?, recipe_preheat_time = ?, recipe_cook_time = ?, recipe_source = ?, recipe_notes = ?, recipe_status = ?
        WHERE recipe_id = ?;
        """,
        (recipe_id,
         recipe_name,
         recipe_type,
         recipe_yield,
         recipe_cooking_vessel,
         recipe_preheat_temp,
         recipe_preheat_unit,
         recipe_preheat_time,
         recipe_cook_time,
         recipe_source,
         recipe_notes,
         recipe_status 
         )
    )
    conn.commit()


def copy_recipe(conn,
                recipe_name,
                recipe_type,
                recipe_yield,
                recipe_cooking_vessel,
                recipe_preheat_temp,
                recipe_preheat_unit,
                recipe_preheat_time,
                recipe_cook_time,
                recipe_source,
                recipe_notes,
                recipe_status
                ):
    """
    Duplicate a logged recipe record and assign a new recipe_id
    """
    conn.execute(
        """
        INSERT INTO recipes
        VALUES recipe_id = ?, recipe_type = ?, recipe_yield = ?, recipe_cooking_vessel = ?, recipe_preheat_temp = ?, recipe_preheat_unit = ?, recipe_preheat_time = ?, recipe_cook_time = ?, recipe_source = ?, recipe_notes = ?, recipe_status = ?;
        """,
        ()
    )
    conn.commit(recipe_name,
                recipe_type,
                recipe_yield,
                recipe_cooking_vessel,
                recipe_preheat_temp,
                recipe_preheat_unit,
                recipe_preheat_time,
                recipe_cook_time,
                recipe_source,
                recipe_notes,
                recipe_status
                )


def delete_recipe(conn, recipe_id):
    cur = conn.execute(
        """
        DELETE FROM recipes WHERE recipe_id = ?
        """, (int(recipe_id),)
                 )
    conn.commit()
    return cur.rowcount

    