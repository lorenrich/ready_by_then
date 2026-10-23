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

DEFAULT_RECIPE_SECTIONS = [
    'Main ingredients',
    'Sauce',
    'Dressing',
    'Garnish'
]

DEFAULT_INGREDIENT_NAMES = [
    'Type to add new ingredient'
]

DEFAULT_UNITS = [
    'cup(s)',
    'Tbsp',
    'tsp'
]

PREP_OPTIONS = [
    'Day before',
    'Day of',
    'At Serving'
]

INGREDIENT_TYPE = [
    'Ingredient',
    'Recipe'
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
                recipe_status,
                recipe_id,   
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
        (recipe_name,
         recipe_type,
         recipe_yield,
         recipe_cooking_vessel,
         recipe_preheat_temp,
         recipe_preheat_unit,
         recipe_preheat_time,
         recipe_cook_time,
         recipe_source,
         recipe_notes,
         recipe_status,
         recipe_id
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

def resolve_recipe_timing(conn, recipe_id, section_id, section_name, ingredient_name):
    conn.execute("""
    SELECT i.ingredient_name, s.section_name,
       COALESCE(s.prep_days_before, i.prep_days_before) AS effective_prep
    FROM recipe_ingredients i
    LEFT JOIN recipe_sections s ON i.section_id = s.section_id
    WHERE i.recipe_id = ?
    """)
    conn.commit()

    