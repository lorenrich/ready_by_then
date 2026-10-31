# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.recipes import get_recipes_for_display
from styles.page_config import (
     PAGES, 
     setup_page_defaults,
     create_button,
     create_page_header,
     create_no_records_container,
     fill_no_records_container)

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

# Read in dataframe
df = get_recipes_for_display(conn=conn)

# Page header
st.html(create_page_header('recipes_page_header', '#CC0099', '#FF85DF'))

header_container = st.container(key='recipes_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Recipes')

# No recipes page
if df.empty:

    st.html(create_no_records_container('no_recipes'))
    blank_container = st.container(height=250, key='no_recipes', horizontal_alignment='center')

    fill_no_records_container(container=blank_container,
                              icon_name='recipes',
                              header_val='Create your first recipe',
                              caption_val='Add ingredients and prep timing preferences all in one place',
                              button_name='create_recipe',
                              page_redirect='create_recipe')

# List recorded recipes    
else:
    # Buttons
    col1, col2 = st.columns([1, 8], gap="small")
    with col1:
        if create_button(name='back'):
            st.switch_page(PAGES['home'])
    with col2:
        if create_button(name='create_recipe'):
                st.switch_page(PAGES['create_recipe'])

    # Data table
    recipe_table = st.dataframe(
             df, 
             on_select="rerun",
             selection_mode="single-row",
             hide_index=True, 
             width="stretch")
    
    selected = recipe_table.selection.rows
    if selected:
        st.session_state["selected_recipe_id"] = int(df.iloc[selected[0]]["Recipe ID"])
        st.switch_page(PAGES['recipe_details'])
    