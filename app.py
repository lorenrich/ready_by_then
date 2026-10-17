"""
Streamlit app
"""
# Import
import streamlit as st
from database.database import get_connection
from styles.page_config import pages

# Connect to database
conn = get_connection()


# Site navigation
pg = st.navigation([
    pages['home'],
    pages['events'],
    pages['event_details'],
    pages['create_event'],
    pages['edit_event'],
    pages['recipes'],
    pages['recipe_details'],
    pages['create_recipe'],
    pages['edit_recipe'],
    pages['custom_lists'],
    pages['custom_list_details'],
    pages['create_custom_list'],
    pages['edit_custom_list'],
    pages['help']
], position="hidden")

# Sidebar config
with st.sidebar:
    st.page_link(pages['home'])

    st.page_link(pages['events'])
    if pg in (pages['events'], pages['create_event']):
        st.page_link(pages['event_details'], label="Event Details")
        st.page_link(pages['create_event'], label="Create Event")
        
    st.page_link(pages['recipes'])

    st.page_link(pages['custom_lists'])

    st.page_link(pages['help'])


# Run
pg.run()