 # Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
import sqlite3
import html
from database.database import get_connection
from database.menus import (COURSES, 
                            get_selected_menu, 
                            get_selected_menu_recipes, 
                            get_menu_events, 
                            delete_menu, 
                            render_menu)
from database.food_and_drink import get_selected_menu_items
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                badge,
                                render_list)

@st.dialog("Delete menu?")
def confirm_delete(menu_id):
    st.write("This permanently deletes the menu. This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if create_button(name="confirm_delete"):
            events = get_menu_events(conn=conn, menu_id=menu_id)
            if events:
                st.warning("This menu is used by: " + ", ".join(name for _, name in events) + ". Deleting it removes it from those events.")

            deleted = delete_menu(conn, menu_id=menu_id)
            if deleted:
                st.switch_page(PAGES["menus"])
            else:
                st.error("Nothing was deleted. The menu may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()


# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Identify selected recipe and filter dataframe
menu_id = st.session_state.get("selected_menu_id")

# Create dataframes
selected_menu_df = get_selected_menu(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_recipes = get_selected_menu_recipes(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_items = get_selected_menu_items(conn=conn, menu_id=menu_id) if menu_id is not None else None

# Guard against empty dataframe else filter it to the selected menu
if menu_id is None:
    st.warning("No menu selected")

if selected_menu_df is None:
    st.warning("That menu couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['menus'], label="<- Back to Menus")
    st.stop()

# Page header
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Kitchen')

title_col, action_col = st.columns([5, 3], vertical_alignment='center')
with title_col:
    title_col.markdown(
        f"<h2 style='margin:0'>{html.escape(selected_menu_df['menu_name'])} {badge(selected_menu_df['menu_status'])}</h2>", 
        unsafe_allow_html=True,
        )

with action_col:
    button_container = st.container(horizontal=True, horizontal_alignment='right')
    with button_container:
        if create_button(name='edit'):
            st.switch_page(PAGES['edit_menu'])

        if create_button(name='copy'):
            st.switch_page(PAGES['copy_menu'])

        if create_button(name='delete'):
            confirm_delete(menu_id=int(selected_menu_df['menu_id']))

st.space("small")

# Write menu notes
if selected_menu_df['menu_notes']:
    st.markdown("**Notes**")
    st.write(selected_menu_df['menu_notes'])

# Write menu details to page
menu_info_col, menu_recipe_col = st.columns(2, border=True)



with menu_recipe_col:
    st.markdown("**What's cooking**")
    st.space("small")

    if not selected_menu_recipes and not selected_menu_items:
        st.caption("No items have been added.")

        if create_button(name='add_recipes_to_menu'):
            st.switch_page(PAGES['edit_menu'])

    else:
        render_menu(recipes=selected_menu_recipes,
                    items=selected_menu_items)
        

st.space("small")

with st.container(border=True):
    st.markdown("**Events**")
