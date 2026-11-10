"""
Streamlit app
"""
# Import
import streamlit as st
from database.database import get_connection
from styles.page_config import PAGES, KITCHEN_PAGES

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
    PAGES['menu_details'],
    PAGES['copy_menu'],
    PAGES['edit_menu'],
    PAGES['create_menu'],
    PAGES['event_menus'],
    PAGES['recipes'],
    PAGES['recipe_details'],
    PAGES['copy_recipe'],
    PAGES['create_recipe'],
    PAGES['edit_recipe'],
    PAGES['ingredients'],
    PAGES['food_and_drink'],
    PAGES['create_food_and_drink'],
    PAGES['edit_food_and_drink']
], position="hidden")

# Sidebar config
with st.sidebar:
    st.page_link(PAGES['home'])
    st.page_link(PAGES['events'])

    if pg in KITCHEN_PAGES:
        st.page_link(PAGES['recipes'], label='Recipes')
        st.page_link(PAGES['food_and_drink'], label='Food & Drink')
        st.page_link(PAGES['menus'], label='Menus')
    else:
        st.page_link(PAGES['recipes'], label='Kitchen')

# Run
pg.run()