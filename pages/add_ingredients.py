"""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
        ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        ingredient_name TEXT NOT NULL,
        amount INTEGER,
        unit TEXT,
        prep_timing TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
        );
    """
"""
        CREATE TABLE IF NOT EXISTS recipe_components (
        parent_recipe_id INTEGER NOT NULL,
        component_recipe_id INTEGER NOT NULL,
        amount REAL,
        unit TEXT,
        PRIMARY KEY (parent_recipe_id, component_recipe_id)
        FOREIGN KEY (parent_recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        FOREIGN KEY (component_recipe_id) REFERENCES recipes(recipe_id) ON DELETE RESTRICT
        )
    """
# Import
import sys 
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Connect to database
conn = get_connection()

recipe_id = st.session_state.get("selected_recipe_id")

# Set up pages
setup_page_defaults()

# Title
st.title("Add Ingredients")
st.write(" ")

# Form
with st.form("add_ingredients"):
    st.write("Let's get started!")
    
    with st.expander("Instructions"):
        st.write('Ready by Then needs your ingredients and their amounts.  Any dropdown can have new options added.')
        st.write('Recipes sometimes include other recipes.  When this happens, add the ingredient as a "Recipe Component".  For example, '\
                 'Chicken Soup contains "Homemade Broth" as a recipe component.  Ready by Then will log "Homemade Broth" as a recipe for '\
                'you to finish editing later.  Do not all an ingredient to BOTH the ingredients list and the components list or it will '\
                'be counted twice in your shopping list.')
        st.write("Prep Timing allows you to decide when it can be prepared.  For example, veggies might be able to be prepped a day in '\
                 'advance but an avocado is best left to prepare at meal time.")
        st.write("You can come back and edit a recipe's ingredients at any time, even if it's marked complete.  We'll remind you when you have incomplete recipes.")

    st.write(recipe_id)

    # Structure as a table with each ingredient and its parts on one line
    # Delete button on each line to remove ingredient
    # User clicks to add more ingredients
    # st.selectbox("Ready to mark this recipe as complete?")
    # Submit button - sends update to recipes table and ingredients to ingredients table
    # Take user to recipe_details page to see full content

    # Need edit_ingredients page
    