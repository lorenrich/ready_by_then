# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection, DEFAULT_STATUSES
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

# Form
with st.form("create_menu"):
    st.write("Let's get started!")