'''
Database connection and schema
'''
# Import
import sqlite3
import os

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
        event_complete BOOLEAN DEFAULT 0,
        event_notes TEXT
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menus (
        event_id INTEGER,
        recipe_id INTEGER,
        host_prepares BOOLEAN DEFAULT 0,
        who_brings TEXT,
        FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
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
        notes TEXT
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
        ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        ingredient_name TEXT NOT NULL,
        amount INTEGER,
        unit TEXT,
        prep_timing TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_components (
        parent_recipe_id INTEGER NOT NULL,
        component_recipe_id INTEGER NOT NULL,
        FOREIGN KEY (parent_recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (component_recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
        )
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS custom_lists (
        list_id INTEGER PRIMARY KEY,
        list_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        need_to_buy BOOLEAN DEFAULT 0,
        advance_prep_okay BOOLEAN DEFAULT 0,
        ideal_start_time INTEGER,  -- e.g. 1
        ideal_start_units TEXT,  -- e.g. 'day' for 1 day before event
        apply_to_all BOOLEAN DEFAULT 0,
        );
    """)
        
    conn.commit()


'''
Set table data restrictions - thoughts, not fully built into rest of code yet

ALTER_RECIPES_TABLE = """
    ALTER TABLE recipes
    ADD CONSTRAINT dish_type
    CHECK (dish_type IN ('Entree', 'Side dish', 'Salad', 'Soup', 'Dessert'));
"""

ALTER_INGREDIENTS_TABLE = """
    ALTER TABLE ingredients
    ADD CONSTRAINT prep_timing_value
    CHECK (prep_timing IN ('day before', 'day of', 'at cook time'));
"""

ALTER_CUSTOM_LIST_TABLE = """
    ALTER TABLE custom_lists
    ADD CONSTRAINT ideal_start_units
    CHECK (ideal_start_units IN ('minutes', 'hours', 'days', 'weeks', 'months'));
"""
'''