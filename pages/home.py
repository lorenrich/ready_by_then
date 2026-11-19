# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, 
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_title_header,
                                create_tagline,
                                create_big_button)

# Set up page
setup_page_defaults()

# Structure containers to hold home page objects
home_row1_col1, home_row1_col2 = st.columns([1, 2], gap="medium")

with home_row1_col1:
    create_title_header("Ready by\nThen")
    create_tagline("a personal event planning app")

with home_row1_col2:
    home_button1, home_button2, home_button3 = st.columns(3, gap="large")

    with home_button1:
        if create_big_button(key='event', 
                             label='🎉\n\nEvents',
                             light_color= '#FFAD94',
                             dark_color='#FE936A'):
            st.switch_page(PAGES['events'])

    with home_button2:
        if create_big_button(key='kitchen', 
                             label='🥗\n\nKitchen',
                             light_color='#8FC9F4',
                             dark_color= '#45A5ED'):
            st.switch_page(PAGES['recipes'])

    with home_button3:
            if create_big_button(key="help",
                                 label='❔\n\nHelp',
                                 light_color='#BCE292',
                                 dark_color='#7EC234'):
                st.switch_page(PAGES['help'])


