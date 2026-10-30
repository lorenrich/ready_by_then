# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from styles.page_config import PAGES, setup_page_defaults, create_big_button

# Set up page
setup_page_defaults()

# Structure containers to hold home page objects
home_row1_col1, home_row1_col2 = st.columns(2, gap="small")

with home_row1_col1:
    # Title
    st.title("Ready by")
    st.title("Then")
    st.space("small")
    st.write("Your personal party planner!")

with home_row1_col2:
    home_button1, home_button2 = st.columns(2, gap="large")

    with home_button1:
        if create_big_button('event', 'Events', '#FE936A', '#FFAD94'):
            st.switch_page(PAGES['events'])


    with home_button2:
        if create_big_button('menu', 'Menus', '#45A5ED', '#8FC9F4'):
            st.switch_page(PAGES['menus'])


home_row2_col1, home_row2_col2 = st.columns(2, gap="small")

# Skip putting anything in row 2 col 1
with home_row2_col2:
    home_button3, home_button4 = st.columns(2, gap="large")

    with home_button3:
        if create_big_button('Recipes', 'Recipes', '#CC0099', '#FF85DF'):
            st.switch_page(PAGES['recipes'])

    with home_button4:
         if create_big_button('custom_lists', 'Task Lists', '#7EC234', '#BCE292'):
              st.switch_page(PAGES['custom_lists'])
