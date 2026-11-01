# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection, DEFAULT_STATUSES
from database.recipes import get_recipes_for_menu_selection
from styles.page_config import setup_page_defaults, PAGES, create_button

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Title
st.title("Create Menu")
st.write(" ")

if create_button(name='back'):
    st.switch_page(PAGES['menus'])

# Menu creation entry
st.write("Let's get started!")

st.text_input("Menu name")
st.space("small")

# Recipe selector
recipe_selection_df = get_recipes_for_menu_selection(conn=conn)

st.write("Select your recipes")

search_col1, search_col2 = st.columns(2)

with search_col1:
    recipe_name_filter = st.text_input("Recipe name")

with search_col2:
    type_options = ['All'] + sorted(recipe_selection_df['Type'].dropna().unique())

    recipe_type_filter = st.selectbox(label='Recipe type',
                                        options=type_options)

filtered_recipe_df = recipe_selection_df

if recipe_name_filter:
    filtered_recipe_df = filtered_recipe_df[filtered_recipe_df['Recipe'].str.contains(recipe_name_filter, case=False, regex=False, na=False)]

if recipe_type_filter != 'All':
    filtered_recipe_df = filtered_recipe_df[filtered_recipe_df['Type'] == recipe_type_filter]

st.data_editor(filtered_recipe_df)

st.text_area("Any notes you want to make?")
st.selectbox("Is the menu complete?", options=DEFAULT_STATUSES, index=1)
