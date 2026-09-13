# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database import get_connection
from events import create_event

# Configure browser tab
st.set_page_config(page_title="Ready by Then", layout="wide")

# Title
st.title("Ready by Then")
st.write(" ")
st.write("Welcome to your personal party planning app!")
st.write(" ")

# Buttons and navigation
if st.button("Events", type="primary", icon=":material/celebration:"):
    st.switch_page("pages/events_page.py")

if st.button("Recipes", type="primary", icon=":material/chef_hat:"):
    st.switch_page("pages/recipes_page.py")

if st.button("Custom Lists", type="primary", icon=":material/list_alt:"):
    st.switch_page("pages/custom_lists_page.py")

if st.button("Help", type="primary", icon=":material/help:"):
    st.switch_page("pages/help_page.py")

