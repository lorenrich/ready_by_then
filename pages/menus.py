# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.menus import get_menus_for_display
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                create_no_records_container,
                                fill_no_records_container,
                                render_list)

# Connect to database
conn = get_connection()

# Read in dataframe
df = get_menus_for_display(conn=conn)

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Kitchen')

# The default section/page for the kitchen is recipes with buttons to other sections
button_container = st.container(horizontal=True)

with button_container:
    if create_button(name='recipes_secondary'):
         st.switch_page(PAGES['recipes'])

    if create_button(name='food_and_drink_secondary'):
         st.switch_page(PAGES['food_and_drink'])

    if create_button(name='menus'):
         st.switch_page(PAGES['menus'])

# No menus page
if df.empty:

    st.html(create_no_records_container('no_menus'))
    blank_container = st.container(height=250, key='no_menus', horizontal_alignment='center')

    fill_no_records_container(container=blank_container,
                              icon_name='menus',
                              header_val='Start your first menu',
                              caption_val='Add your favorite recipes to create the perfectly balanced meal',
                              button_name='create_menu',
                              page_redirect='create_menu')

# List recorded recipes    
else:
    # Buttons
    create_button_container = st.container(horizontal=True)
    with create_button_container:
        if create_button(name='create_menu'):
            st.switch_page(PAGES['create_menu'])

    # Render table
    df = df.fillna('')

    rows = df.to_dict("records")

    columns = [
    ("Menu", "Menu", 4, "link"),
    ("Status", "Status", 2, "badge"),
    ]

    def open_menu(row):
        st.session_state["selected_menu_id"] = row["Menu ID"]
        st.switch_page(PAGES['menu_details'])

    render_list(rows=rows,
                columns=columns,
                id_field='Menu ID',
                on_open=open_menu,
                prefix='menus')

