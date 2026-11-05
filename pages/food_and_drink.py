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
                                fill_no_records_container)

# Connect to database
conn = get_connection()

# Read in dataframe TODO
#df = get_menus_for_display(conn=conn)

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Kitchen')

# The default section/page for the kitchen is recipes with buttons to other sections
col1, col2, col3 = st.columns([1, 3, 3], gap="small")

with col1:
    if create_button(name='recipes_secondary'):
         st.switch_page(PAGES['recipes'])

with col2:
    if create_button(name='food_and_drink'):
         st.switch_page(PAGES['food_and_drink'])

with col3:
    if create_button(name='menus_secondary'):
         st.switch_page(PAGES['menus'])