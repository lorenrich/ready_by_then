# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection
from database.recipes import get_selected_recipe, copy_recipe, delete_recipe
from styles.page_config import setup_page_defaults, pages, buttons, create_button

@st.dialog("Delete recipe?")
def confirm_delete(recipe_id):
    st.write("This permanently deletes the recipe. This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if create_button(name="confirm_delete"):
            deleted = delete_recipe(conn, recipe_id=recipe_id)
            if deleted:
                st.switch_page(pages["recipes"])
            else:
                st.error("Nothing was deleted. The recipe may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()

# Connect to database
conn = get_connection()

# Set up page defaults
setup_page_defaults()

# Identify selected recipe and filter dataframe
recipe_id = st.session_state.get("selected_recipe_id")

# Create dataframe
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None

# Guard against empty dataframe else filter it to the selected recipe
if recipe_id is None:
    st.warning("No recipe selected")

if selected_recipe_df is None:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(pages['recipes'])

# Title
st.title("Recipe Details")
st.space("small")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(pages['edit_recipe'])

with button_col_2:
    if create_button(name='copy'):
        st.switch_page(pages['copy_recipe'])
    
with button_col_3:
    if create_button(name='delete'):
        confirm_delete(recipe_id=int(selected_recipe_df['recipe_id']))

st.space("small")

# Recipe Details
st.write(selected_recipe_df['recipe_name'])
st.write("")

