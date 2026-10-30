"""
Streamlit app
"""
# Import
import streamlit as st
from database.database import get_connection
from styles.page_config import PAGES

# Connect to database
conn = get_connection()


# Site navigation
pg = st.navigation([
    PAGES['home'],
    PAGES['events'],
    PAGES['event_details'],
    PAGES['copy_event'],
    PAGES['create_event'],
    PAGES['edit_event'],
    PAGES['menus'],
    PAGES['create_menu'],
    PAGES['recipes'],
    PAGES['recipe_details'],
    PAGES['copy_recipe'],
    PAGES['create_recipe'],
    PAGES['edit_recipe'],
    PAGES['ingredients'],
    PAGES['custom_lists'],
    PAGES['custom_list_details'],
    PAGES['create_custom_list'],
    PAGES['edit_custom_list'],
    PAGES['help']
], position="hidden")

# Sidebar config
with st.sidebar:
    st.page_link(PAGES['home'])

    st.page_link(PAGES['events'])
    if pg in (PAGES['events'], PAGES['create_event']):
        st.page_link(PAGES['event_details'], label="Event Details")
        st.page_link(PAGES['create_event'], label="Create Event")
        
    st.page_link(PAGES['recipes'])

    st.page_link(PAGES['custom_lists'])

    st.page_link(PAGES['help'])


# Run
pg.run()