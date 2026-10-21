# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection, update_and_default_selectbox, DEFAULT_STATUSES
from database.recipes import get_selected_recipe, edit_recipe, DEFAULT_PREHEAT_UNITS, DEFAULT_RECIPE_TYPES
from styles.page_config import setup_page_defaults, pages

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Identify selected recipe and filter dataframe
recipe_id = st.session_state.get("selected_recipe_id")

# Create dataframe
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None

# Guard against empty dataframe else filter it to the selected recipe
if selected_recipe_df.empty:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

# Title
st.title("Edit Recipe")
st.space("small")

# Create the unique lists for selectboxes including defaults and user-created entries
recipe_types = update_and_default_selectbox(conn=conn,
                                            table_name='recipes',
                                            col_name='recipe_type',
                                            selected_record_df=selected_recipe_df,
                                            default_options=DEFAULT_RECIPE_TYPES)

preheat_units = update_and_default_selectbox(conn=conn,
                                             table_name='recipes',
                                             col_name='recipe_preheat_unit',
                                             selected_record_df=selected_recipe_df,
                                             default_options=DEFAULT_PREHEAT_UNITS)

# Identify default user selections
default_recipe_type = selected_recipe_df['recipe_type']
default_preheat_unit = selected_recipe_df['recipe_preheat_unit']

# Form
with st.form("edit_recipe"):
    recipe_id = st.text_input("Recipe ID", 
                                   value=selected_recipe_df["recipe_id"], disabled=True)
    recipe_name = st.text_input("Recipe name", 
                               value=selected_recipe_df["recipe_name"])
    recipe_type = st.selectbox(
        "Recipe type",
        options=recipe_types,
        index=recipe_types.index(default_recipe_type) if default_recipe_type in recipe_types else None,
        accept_new_options=True,
        placeholder="Choose or type a new type",
    )
    recipe_yield = st.number_input("Servings yield",
                                   step=1,
                                   value=selected_recipe_df['recipe_yield'])
    recipe_cooking_vessel = st.text_input("Where recipe is cooked (e.g. oven, air fryer)", value=selected_recipe_df['recipe_cooking_vessel'])
    recipe_preheat_temp = st.number_input("Preheat Temperature", step=1, value=selected_recipe_df['recipe_preheat_temp'])
    recipe_preheat_unit = st.selectbox(
        "Preheat Unit",
        options=preheat_units,
        index=preheat_units.index(default_preheat_unit) if default_preheat_unit in preheat_units else None,
        accept_new_options=True,
        placeholder="Choose or type a temperature unit",
        )                         
    recipe_preheat_time = st.number_input("How long should be allowed for preheat (in minutes)?", step=1, value=selected_recipe_df['recipe_preheat_time'])
    recipe_cook_time = st.number_input("What is the approximate cook time (in minutes)?", step=1, value=selected_recipe_df['recipe_cook_time'])
    recipe_source = st.text_input("Who or where is this recipe from?", value=selected_recipe_df['recipe_source'])
    recipe_notes = st.text_area("Any extra notes you want to add?", value=selected_recipe_df['recipe_notes'])
    recipe_status = st.selectbox("Is this recipe now complete?", options=DEFAULT_STATUSES, value=selected_recipe_df['recipe_status'])
    
    # Save 
    if st.form_submit_button("Save changes"):
       edit_recipe(conn,
                   recipe_id=recipe_id,
                   recipe_name=recipe_name,
                   recipe_type=recipe_type,
                   recipe_yield=recipe_yield,
                   recipe_cooking_vessel=recipe_cooking_vessel,
                   recipe_preheat_temp=recipe_preheat_temp,
                   recipe_preheat_unit=recipe_preheat_unit,
                   recipe_preheat_time=recipe_preheat_time,
                   recipe_cook_time=recipe_cook_time,
                   recipe_source=recipe_source,
                   recipe_notes=recipe_notes,
                   recipe_status=recipe_status
                  )
       st.switch_page(pages['recipes'])
       