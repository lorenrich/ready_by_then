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

DEFAULT_PREP_OPTIONS = {
    'Day before': 2,
    'Day of': 1,
    'At Serving': 0
}

PREP_LABELS = {v: k for k, v in DEFAULT_PREP_OPTIONS.items()}

DEFAULT_INGREDIENT_TYPE = [
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


def get_recipes_for_menu_selection(conn):
    """
    Pull recipes from database to allow user to tag to menu
    """
    df = pd.read_sql_query(
        '''
        SELECT
            recipe_id AS "Recipe ID",
            recipe_name AS "Recipe",
            recipe_type AS "Type"
        FROM recipes
        ''', conn,
    )

    df["Add to Menu"] = False

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
    cursor = conn.execute(
        "INSERT INTO recipes (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source, recipe_notes, recipe_status) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source, recipe_notes, recipe_status)
    )
    conn.commit()
    return cursor.lastrowid


def get_selected_recipe(conn, recipe_id):
    df = pd.read_sql_query(
        "SELECT * FROM recipes WHERE recipe_id = ?", conn, params=(recipe_id,)
    )
    return df.iloc[0] if not df.empty else None


def get_selected_recipe_ingredients(conn, recipe_id):
    recipe_id = int(recipe_id)
    return conn.execute(
        """
        SELECT i.ingredient_name,
                s.section_name,
                'Ingredient',
                i.amount,
                i.unit,
                i.prep_timing,
                NULL
        FROM recipe_ingredients i
        LEFT JOIN recipe_sections s on i.section_id = s.section_id
        WHERE i.recipe_id = ?

        UNION ALL

        SELECT r.recipe_name,
                s.section_name,
                'Recipe',
                c.amount,
                c.unit,
                c.prep_timing,
                c.component_recipe_id
        FROM recipe_components c
        JOIN recipes r ON r.recipe_id = c.component_recipe_id
        LEFT JOIN recipe_sections s ON c.section_ID = s.section_ID
        WHERE c.parent_recipe_id = ?
        ORDER BY 2, 3
        """,
        (recipe_id, recipe_id),
    ).fetchall()



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
                source_recipe_id, 
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
    """
    Duplicate a recipe with its sections, ingredients, and components and return the new recipe_id.
    """
    source_recipe_id = int(source_recipe_id)
    try:
        # Copy the recipe row
        cur = conn.execute(
            """
            INSERT INTO recipes (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel,
                                recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time,
                                recipe_cook_time, recipe_source, recipe_notes, recipe_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (recipe_name, recipe_type, recipe_yield, recipe_cooking_vessel,
            recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time,
            recipe_cook_time, recipe_source, recipe_notes, recipe_status),
        )
        new_id = cur.lastrowid

        # Copy the sections
        conn.execute(
            """
            INSERT INTO recipe_sections (recipe_id, section_name, prep_timing)
            SELECT ?, section_name, prep_timing
            FROM recipe_sections
            WHERE recipe_id = ?
            """,
            (new_id, source_recipe_id),
        )

        # Copy the ingredients
        conn.execute(
            """
            INSERT INTO recipe_ingredients (recipe_id, section_id, ingredient_name, amount, unit, prep_timing)
            SELECT ?, ns.section_id, i.ingredient_name, i.amount, i.unit, i.prep_timing
            FROM recipe_ingredients i
            LEFT JOIN recipe_sections os ON os.section_id = i.section_id
            LEFT JOIN recipe_sections ns ON ns.recipe_id = ? AND ns.section_name = os.section_name
            WHERE i.recipe_id = ?
            """,
            (new_id, new_id, source_recipe_id),
        )

        # Copy the components
        conn.execute(
            """
            INSERT INTO recipe_components (parent_recipe_id, component_recipe_id, section_id, amount, unit, prep_timing)
            SELECT ?, c.component_recipe_id, ns.section_id, c.amount, c.unit, c.prep_timing
            FROM recipe_components c
            LEFT JOIN recipe_sections os ON os.section_id = c.section_id
            LEFT JOIN recipe_sections ns ON ns.recipe_id = ? AND ns.section_name = os.section_name
            WHERE c.parent_recipe_id = ?
            """,
            (new_id, new_id, source_recipe_id),
        )

        conn.commit()
        return new_id
    except Exception:
        conn.rollback()
        raise


def delete_recipe(conn, recipe_id):
    cursor = conn.execute(
        """
        DELETE FROM recipes WHERE recipe_id = ?
        """, (int(recipe_id),)
                 )
    conn.commit()
    return cursor.rowcount

def get_recipe_usage(conn, recipe_id):
    recipe_id = int(recipe_id)
    parents = conn.execute(
        """
        SELECT r.recipe_id, r.recipe_name
        FROM recipe_components c
        JOIN recipes r ON r.recipe_id = c.parent_recipe_id
        WHERE c.component_recipe_id = ?
        ORDER BY r.recipe_name
        """,
        (recipe_id,),
    ).fetchall()

    events = conn.execute(
        """
        SELECT e.event_id, e.name
        FROM menus m
        JOIN events e ON e.event_id = m.event_id
        WHERE m.recipe_id = ?
        ORDER BY e.name
        """,
        (recipe_id,),
    ).fetchall()

    return parents, events


def resolve_recipe_timing(conn, recipe_id):
    """
    List every ingredient and sub-recipe in a recipe with the prep timing that applies.
    Returns tuples: (name, section_name, item_type, effective_prep)
    """
    recipe_id = int(recipe_id)
    return conn.execute(
        """
        SELECT i.ingredient_name,
               s.section_name,
               'Ingredient',
               COALESCE(s.prep_timing, i.prep_timing)
        FROM recipe_ingredients i
        LEFT JOIN recipe_sections s ON i.section_id = s.section_id
        WHERE i.recipe_id = ?

        UNION ALL

        SELECT r.recipe_name,
               s.section_name,
               'Recipe',
               COALESCE(s.prep_timing, c.prep_timing)
        FROM recipe_components c
        JOIN recipes r ON r.recipe_id = c.component_recipe_id
        LEFT JOIN recipe_sections s ON c.section_id = s.section_id
        WHERE c.parent_recipe_id = ?
        """,
        (recipe_id, recipe_id),
    ).fetchall()


def get_or_create_section(conn, recipe_id, name):
    cursor = conn.execute(
        """
        SELECT section_id FROM recipe_sections WHERE recipe_id = ? AND section_name = ? COLLATE NOCASE
        """, (recipe_id, name)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor = conn.execute(
            """
            INSERT INTO recipe_sections (recipe_id, section_name) VALUES (?, ?)
            """,
            (recipe_id, name)
        )
        return cursor.lastrowid


def get_or_create_stub(conn, name):
    row = conn.execute(
        """
        SELECT recipe_id FROM recipes WHERE recipe_name = ? COLLATE NOCASE
        """, (name.strip(),)
    ).fetchone()
    if row:
        return row[0]

    cur = conn.execute(
        """
        INSERT INTO recipes (recipe_name, recipe_status) VALUES(?, 'Incomplete')
        """, (name.strip(),)
    )
    return cur.lastrowid


def save_ingredients(conn, recipe_id, items):
    recipe_id = int(recipe_id)
    try:
        # Delete any existing data
        conn.execute("""DELETE from recipe_components WHERE parent_recipe_id = ?""", (int(recipe_id),))
        conn.execute("""DELETE FROM recipe_ingredients WHERE recipe_id = ?""", (int(recipe_id),))
        conn.execute("""DELETE FROM recipe_sections WHERE recipe_id = ?""", (int(recipe_id),))

        for item in items:
            section_id = get_or_create_section(conn, recipe_id, item["section"]) if item["section"] else None
            if item["type"] == "Recipe":
                component_id = get_or_create_stub(conn, item["name"])
                if component_id == recipe_id:
                    raise ValueError("A recipe can't be an ingredient of itself.")

                # Insert into recipe_components
                conn.execute(
                    """
                    INSERT INTO recipe_components (parent_recipe_id, component_recipe_id, section_id, amount, unit, prep_timing) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (recipe_id, component_id, section_id, item["amount"], item["unit"], item["prep"])
                    
                )
            else:
                # Insert into recipe_ingredients
                conn.execute(
                    """
                    INSERT INTO recipe_ingredients (recipe_id, section_id, ingredient_name, amount, unit, prep_timing) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (recipe_id, section_id, item["name"], item["amount"], item["unit"], item["prep"]),
                    )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
