 # Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
import sqlite3
from database.database import get_connection
from database.menus import COURSES, get_selected_menu, get_selected_menu_recipes, get_menu_events, delete_menu
from styles.page_config import PAGES, setup_page_defaults, create_button

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


def format_item(recipe_name, recipe_status):
    if recipe_status == 'Complete':
        return recipe_name
    else:
        return f"{recipe_name} ({recipe_status})"


# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Identify selected recipe and filter dataframe
menu_id = st.session_state.get("selected_menu_id")

# Create dataframes
selected_menu_df = get_selected_menu(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_recipes = get_selected_menu_recipes(conn=conn, menu_id=menu_id) if menu_id is not None else None

# Guard against empty dataframe else filter it to the selected menu
if menu_id is None:
    st.warning("No menu selected")

if selected_menu_df is None:
    st.warning("That menu couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['menus'], label="<- Back to Menus")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(PAGES['menus'])

# Title
st.title("Menu Details")
st.space("small")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(PAGES['edit_menu'])

with button_col_2:
    if create_button(name='copy'):
        st.switch_page(PAGES['copy_menu'])
    
with button_col_3:
    if create_button(name='delete'):
        confirm_delete(menu_id=int(selected_menu_df['menu_id']))

st.space("small")

# Write menu details to page
menu_info_col, menu_recipe_col = st.columns(2, border=True)
with menu_info_col:
    info_col1, info_col2 = st.columns([1, 3], gap="small")
    with info_col1:
        st.markdown("**Menu:**", text_alignment="right")
        st.markdown("**Menu Notes:**", text_alignment="right")
        st.space("small")
        st.markdown("**Menu Status:**", text_alignment="right")

    with info_col2:
        st.write(selected_menu_df['menu_name'] if selected_menu_df['menu_name'] else "&nbsp;")
        st.write(selected_menu_df['menu_notes'] if selected_menu_df['menu_notes'] else "&nbsp;")
        st.space("small")
        st.write(selected_menu_df['menu_status'] if selected_menu_df['menu_status'] else "&nbsp;")

with menu_recipe_col:
    st.markdown("**Recipes**")
    st.space("small")

    if not selected_menu_recipes:
        st.caption("No recipes have been added.")

        if create_button(name='add_recipes_to_menu'):
            st.switch_page(PAGES['edit_menu'])

    else:
        has_courses = any(course for recipe_id, recipe_name, recipe_status, course in selected_menu_recipes)

        if has_courses:
            by_course = {}
            for recipe_id, recipe_name, recipe_status, course in selected_menu_recipes:
                by_course.setdefault(course or "Unassigned", []).append((recipe_name, recipe_status))

            course_order = [c for c in COURSES if c in by_course] + [c for c in by_course if c not in COURSES]

            for course in course_order:
                label_col, items_col = st.columns([1, 4])
                label_col.markdown(f"**{course}**")
                with items_col:
                    for recipe_name, recipe_status in by_course[course]:
                        st.write(format_item(recipe_name=recipe_name, recipe_status=recipe_status))

        else:
            for recipe_id, recipe_name, recipe_status, course in selected_menu_recipes:
                st.write(format_item(recipe_name=recipe_name, recipe_status=recipe_status))
        

st.space("small")

with st.container(border=True):
    st.markdown("**Events**")
