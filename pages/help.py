# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from styles.page_config import setup_page_defaults, PAGES, create_button

# Set up page
setup_page_defaults()

st.write ("Coming soon!")