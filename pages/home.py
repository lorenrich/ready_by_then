# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from styles.page_config import setup_page_defaults, pages, buttons, create_button

setup_page_defaults()

# Title
st.title("Ready")
st.title("by")
st.title("Then")
st.write(" ")
st.write("Your personal party planner!")
st.write(" ")

# Buttons and navigation
if create_button(name='events'):
    st.switch_page(pages['events'])

if create_button(name="recipes"):
    st.switch_page(pages['recipes'])

if create_button(name='custom_lists'):
    st.switch_page(pages['custom_lists'])

if create_button(name='help'):
    st.switch_page(pages['help'])

