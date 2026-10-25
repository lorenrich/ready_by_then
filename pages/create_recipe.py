# Import
import sys 
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.recipes import create_recipe, DEFAULT_PREHEAT_UNITS, DEFAULT_RECIPE_TYPES
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Connect to database
conn = get_connection()

# Set up pages
setup_page_defaults()

# Title
st.title("Create New Recipe")
st.write(" ")

# Form
with st.form("create_recipe"):
    st.write("Let's get started!")
    
    with st.expander("Instructions"):
        st.write('Ready by Then needs your recipe details like cook time and ingredients but not your recipe steps like "Add ingredients to bowl".')
        st.write("You can come back and edit a recipe at any time, even if it's marked complete.  We'll remind you when you have incomplete recipes.")
        st.write("Once you create a recipe, you can tag it to a menu from the Menu page.")

    recipe_name = st.text_input("Recipe Name")
    recipe_type = st.selectbox("Recipe Type", DEFAULT_RECIPE_TYPES, index=None, accept_new_options=True)
    recipe_yield = st.number_input("Servings Yield", step=1)
    recipe_cooking_vessel = st.text_input("Where recipe is cooked (e.g. oven, air fryer)")
    recipe_preheat_temp = st.number_input("Preheat Temperature", step=1)
    recipe_preheat_unit = st.selectbox("Preheat Unit", DEFAULT_PREHEAT_UNITS, index=None, accept_new_options=True)
    recipe_preheat_time = st.number_input("How long should be allowed for preheat (in minutes)?", step=1)
    recipe_cook_time = st.number_input("What is the approximate cook time (in minutes)?", step=1)
    recipe_source = st.text_input("Who or where is this recipe from?")
    recipe_notes = st.text_area("Any extra notes you want to add?")

    # Take user to add_ingredients or submit as-is
    col1, col2 = st.columns([1, 7], gap="small")

    with col1:
        add_now = st.form_submit_button("Add ingredients", type="primary")
    with col2:
        add_later = st.form_submit_button("I'll add ingredients later")

    if add_now or add_later:
        if not recipe_name.strip():
            st.error("Please give the recipe a name.")
            st.stop()

        new_recipe_id = create_recipe(
            conn,
            recipe_name=recipe_name.strip(),
            recipe_type=recipe_type,
            recipe_yield=recipe_yield,
            recipe_cooking_vessel=recipe_cooking_vessel,
            recipe_preheat_temp=recipe_preheat_temp,
            recipe_preheat_unit=recipe_preheat_unit,
            recipe_preheat_time=recipe_preheat_time,
            recipe_cook_time=recipe_cook_time,
            recipe_source=recipe_source,
            recipe_notes=recipe_notes,
            recipe_status="Incomplete",
        )

        if add_now:
            st.session_state["selected_recipe_id"] = new_recipe_id
            st.switch_page(pages["add_ingredients"])
        else:
            st.switch_page(pages["recipes"])
       