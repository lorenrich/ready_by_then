'''
Database connection and schema
'''
# Import
import sqlite3
import os
import pandas as pd

# Identify directory path
DB_PATH = "ready_by_then.db"

def get_connection():
    db_exists = os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    if not db_exists:
        initialize_schema(conn)
    return conn

def initialize_schema(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        event_date TEXT NOT NULL,
        num_adults INTEGER NOT NULL,
        num_kids INTEGER NOT NULL,
        num_hearty_eaters INTEGER NOT NULL,
        need_kids_menu BOOLEAN NOT NULL,
        dietary_needs TEXT,
        event_occurred BOOLEAN DEFAULT 0,
        event_notes TEXT,
        event_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menus (
        menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
        menu_name TEXT NOT NULL,
        menu_notes TEXT,
        menu_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menu_recipes (
        menu_id INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        course TEXT,
        PRIMARY KEY (menu_id, recipe_id)
        FOREIGN KEY (menu_id) REFERENCES menus(menu_id) ON DELETE CASCADE,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE RESTRICT
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS event_menus (
        event_id INTEGER NOT NULL,
        menu_id INTEGER NOT NULL,
        PRIMARY KEY (event_id, menu_id)
        FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
        FOREIGN KEY (menu_id) REFERENCES menus(menu_id) ON DELETE CASCADE
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        recipe_type TEXT,
        recipe_yield INTEGER,
        recipe_cooking_vessel TEXT,
        recipe_preheat_temp INTEGER,
        recipe_preheat_unit TEXT,
        recipe_preheat_time INTEGER,
        recipe_cook_time INTEGER,
        recipe_source TEXT,
        recipe_notes TEXT,
        recipe_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
        ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        section_id INTEGER,
        ingredient_name TEXT NOT NULL,
        amount REAL,
        unit TEXT,
        prep_timing INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        FOREIGN KEY (section_id) REFERENCES recipe_sections(section_id) ON DELETE SET NULL
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_components (
        parent_recipe_id INTEGER NOT NULL,
        component_recipe_id INTEGER NOT NULL,
        section_id INTEGER,
        amount REAL,
        unit TEXT,
        prep_timing INTEGER,
        PRIMARY KEY (parent_recipe_id, component_recipe_id),
        CHECK (parent_recipe_id != component_recipe_id),
        FOREIGN KEY (parent_recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        FOREIGN KEY (component_recipe_id) REFERENCES recipes(recipe_id) ON DELETE RESTRICT,
        FOREIGN KEY (section_id) REFERENCES recipe_sections(section_id) ON DELETE SET NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_sections (
        section_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        section_name TEXT NOT NULL,
        prep_timing INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        UNIQUE (recipe_id, section_name)
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS custom_lists (
        list_id INTEGER PRIMARY KEY,
        list_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        need_to_buy BOOLEAN DEFAULT 0,
        prep_timing INTEGER,
        apply_to_all BOOLEAN DEFAULT 0,
        list_notes TEXT,
        list_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
    """)
        
    conn.commit()


DEFAULT_STATUSES = [
    "Complete",
    "Incomplete"
]


ALLOWED_COLUMNS = {
    "recipes": {"recipe_type", "recipe_preheat_unit"},
    "recipe_ingredients": {"ingredient_name", "unit"},
    "recipe_sections": {"section_name"}
}


def get_unique_records(conn, table_name, col_name):
    if col_name not in ALLOWED_COLUMNS.get(table_name, set()):
        raise ValueError(f"Not allowed: {table_name}.{col_name}")

    rows = conn.execute(
        f"""
        SELECT DISTINCT {col_name}
        FROM {table_name}
        WHERE {col_name} IS NOT NULL AND {col_name} != ''
        ORDER BY {col_name} COLLATE NOCASE
        """
    ).fetchall()
    return [row[0] for row in rows]


def update_and_default_selectbox(conn, table_name, col_name, default_options, selected_record_df=None):
    """
    Remember to add any new fields to ALLOWED_COLUMNS in db.py or this will throw a ValueError.
    """
    # Get unique values from existing database table
    entries = get_unique_records(conn=conn, table_name=table_name, col_name=col_name)

    # Identify user selection
    options = list(default_options)
    if selected_record_df is not None:
        current = selected_record_df[col_name]
        if pd.notna(current) and current:
            options.append(current)

    # Drop entries to lowercase
    seen = {e.strip().lower() for e in entries}

    # Ensure default options are in the list if they aren't found in table records
    for o in options:
        if o.strip().lower() not in seen:
            entries.append(o.strip())
            seen.add(o.strip().lower())

    return sorted(entries, key=str.lower)
