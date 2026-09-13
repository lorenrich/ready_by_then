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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        event_date TEXT NOT NULL,
        num_adults INTEGER NOT NULL,
        num_kids INTEGER NOT NULL,
        will_kids_eat_adult_meal BOOLEAN NOT NULL,
        dietary_needs TEXT,
        event_complete BOOLEAN DEFAULT 0,
        notes TEXT
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menus (
        event_id INTEGER,
        menu_item_id INTEGER,
        host_prepares BOOLEAN DEFAULT 0,
        whos_bringing TEXT,
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (menu_item_id) REFERENCES recipes(id)
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dish_type TEXT,
        yield INTEGER,
        preheat_temp INTEGER,
        preheat_unit TEXT,
        preheat_time_estimate INTEGER,
        cook_time_estimate INTEGER,
        notes TEXT
        );
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        ingredient_name TEXT NOT NULL,
        amount INTEGER,
        unit TEXT,
        prep_timing TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe_components (
        parent_recipe_id INTEGER NOT NULL,
        component_recipe_id INTEGER NOT NULL,
        FOREIGN KEY (parent_recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (component_recipe_id) REFERENCES recipes(id)
        )
    """)
        
    conn.execute("""
        CREATE TABLE IF NOT EXISTS custom_lists (
        id INTEGER PRIMARY KEY,
        list_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        need_to_buy BOOLEAN DEFAULT 0,
        advance_prep_okay BOOLEAN DEFAULT 0,
        ideal_start_time INTEGER,  -- e.g. 1
        ideal_start_units TEXT  -- e.g. 'day' for 1 day before event
        );
    """)
        
    conn.commit()


'''
Set table data restrictions - thoughts, not fully built into rest of code yet

ALTER_RECIPES_TABLE = """
    ALTER TABLE recipes
    ADD CONSTRAINT dish_type
    CHECK (dish_type IN ('entree', 'side dish', 'salad', 'soup', 'dessert'));
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