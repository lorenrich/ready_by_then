# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database import get_connection
from recipes import create_recipe

# Create the connection to the database
conn = get_connection()

# Configure browser tab
st.set_page_config(page_title="Ready by Then", layout="wide")

# Title
st.title("Create New Recipe")
st.write(" ")

# Form
with st.form("create_recipe"):
    st.write("Let's get started!  Add your recipes below.  We'll get to ingredients and tagging recipes to events later.")
    recipe_name = st.text_input("Recipe Name")
    recipe_type = st.selectbox("Recipe Type", [
        "Appetizer",
        "Entree",
        "Salad",
        "Soup",
        "Side",
        "Dessert"
    ], index=None, accept_new_options=True)
    recipe_yield = st.number_input("Servings Yield", step=1)
    recipe_cooking_vessel = st.text_input("Where recipe is cooked (e.g. oven, air fryer)")
    recipe_preheat_temp = st.number_input("Preheat Temperature", step=1)
    recipe_preheat_unit = st.selectbox("Preheat Unit", ["Celsius", "Fahrenheit"],
                                     index=None,
                                     accept_new_options=True)
    recipe_preheat_time = st.number_input("How long should be allowed for preheat (in minutes)?", step=1)
    recipe_cook_time = st.number_input("What is the approximate cook time (in minutes)?", step=1)
    recipe_source = st.text_input("Who or where is this recipe from?")
    notes = st.text_area("Any extra notes you want to add?")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
       create_recipe(conn,
                    name=recipe_name, 
                    recipe_type=recipe_type,
                    recipe_yield=recipe_yield,
                    recipe_cooking_vessel=recipe_cooking_vessel,
                    recipe_preheat_temp=recipe_preheat_temp,
                    recipe_preheat_unit=recipe_preheat_unit,
                    recipe_preheat_time=recipe_preheat_time,
                    recipe_cook_time=recipe_cook_time,
                    recipe_source=recipe_source,
                    notes=notes)
       st.switch_page("pages/recipes.py")
       