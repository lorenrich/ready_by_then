# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection, DEFAULT_STATUSES
from styles.page_config import setup_page_defaults, PAGES, create_button, create_page_header

# Connect to database
conn = get_connection()

# Read in dataframe TODO activate once written
#df = get_events_for_display(conn=conn)

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('menus_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='menus_page_header')

with header_container:
     st.write(':material/yoshoku: Menus')

if create_button(name='back'):
    st.switch_page(PAGES['menus'])

