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
     fill_no_records_container,
     render_list)

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

# Read in dataframe
df = get_recipes_for_display(conn=conn)

# Page header
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Kitchen')

# The default section/page for the kitchen is recipes with buttons to other sections
button_container = st.container(horizontal=True)
with button_container:
    if create_button(name='recipes'):
         st.switch_page(PAGES['recipes'])

    if create_button(name='food_and_drink_secondary'):
         st.switch_page(PAGES['food_and_drink'])

    if create_button(name='menus_secondary'):
         st.switch_page(PAGES['menus'])


# No recipes
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
    create_button_container = st.container(horizontal=True)
    with create_button_container:
        if create_button(name='create_recipe'):
            st.switch_page(PAGES['create_recipe'])

    # Render table
    df = df.fillna('')

    rows = df.to_dict("records")

    columns = [
    ("Recipe", "Recipe", 4, "link"),
    ("Type", "Type", 2, "string"),
    ("Status", "Status", 2, "badge"),
    ]

    def open_recipe(recipe_id):
        st.session_state["selected_recipe_id"] = int(recipe_id)
        st.switch_page(PAGES['recipe_details'])

    render_list(rows=rows,
                columns=columns,
                id_field='Recipe ID',
                on_open=open_recipe,
                prefix='Recipes')
