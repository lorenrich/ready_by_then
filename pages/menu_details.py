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
    notes_container = st.container(horizontal=True, border=True, key='detail_card')
    with notes_container:
        st.markdown("**Notes:**")
        st.write(selected_menu_df['menu_notes'])

# Write menu details to page
st.space("small")
st.markdown("**What's cooking**")

menu_container = st.container(horizontal=True)
with menu_container:
    

    if not selected_menu_recipes and not selected_menu_items:
            st.caption("No items have been added.")
    else:
        entries = []
        for recipe_id, name, status, course in selected_menu_recipes:
            entries.append({"kind": "recipe", "id": recipe_id, "name": name,
                            "status": status, "course": course})
        for item_id, name, course in selected_menu_items:
            entries.append({"kind": "item", "id": item_id, "name": name,
                            "status": "", "course": course})

        def course_rank(course):
            return COURSES.index(course) if course in COURSES else len(COURSES)

        entries.sort(key=lambda e: (course_rank(e["course"]), e["name"].lower()))

        rows, last = [], None
        for e in entries:
            label = e["course"] or "Unassigned"
            rows.append({
                "Course": label if label != last else "",
                "Name": e["name"],
                "Status": e["status"],
                "kind": e["kind"],
                "id": e["id"],
                "row_key": f"{e['kind']}-{e['id']}",
            })
            last = label

        columns = [
        ("Course", "Course", 2, "string"),
        ("Name", "Name", 5, "link"),
        ("Status", "Status", 2, "badge")
        ]

        def open_entry(row):
            if row["kind"] == "recipe":
                st.session_state["selected_recipe_id"] = int(row["id"])
                st.switch_page(PAGES['recipe_details'])
            else:
                st.session_state["selected_item_id"] = int(row["id"])
                st.switch_page(PAGES['edit_food_and_drink'])

        render_list(rows=rows, 
                    columns=columns,
                    id_field='row_key',
                    on_open=open_entry,
                    prefix='items')
      

st.space("small")

with st.container(border=True):
    st.markdown("**Events**")
