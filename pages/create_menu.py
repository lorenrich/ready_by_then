# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from collections import Counter
from database.database import DEFAULT_STATUSES, get_connection
from database.menus import COURSES, create_menu, save_menu
from database.recipes import get_recipes_for_menu_selection
from styles.page_config import PAGES, setup_page_defaults, create_button

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Initialize session state
if "menu_recipe_ids" not in st.session_state:
    st.session_state.menu_recipe_ids = []

# Title
st.title("Create Menu")
st.write(" ")

if create_button(name='back'):
    st.switch_page(PAGES['menus'])


# Menu creation entry
st.write("Let's get started!")

menu_name = st.text_input("Menu name")
st.space("small")

# Recipe selector
recipe_selection_df = get_recipes_for_menu_selection(conn=conn)

st.write("Select your recipes")

search_col1, search_col2 = st.columns(2)

with search_col1:
    recipe_name_filter = st.text_input("Recipe name")

with search_col2:
    type_options = ['All'] + sorted(recipe_selection_df['Type'].dropna().unique())

    recipe_type_filter = st.selectbox(label='Recipe type',
                                        options=type_options)

# Filter a copy of the dataframe based on user selection
filtered_df = recipe_selection_df

if recipe_name_filter:
    filtered_df = filtered_df[filtered_df['Recipe'].str.contains(recipe_name_filter, case=False, regex=False, na=False)]

if recipe_type_filter != 'All':
    filtered_df = filtered_df[filtered_df['Type'] == recipe_type_filter]

# Create the dataframe key
editor_key = f"menu_editor_{recipe_name_filter}_{recipe_type_filter}"

if editor_key not in st.session_state:
    base_df = filtered_df.copy()
    base_df["Add to Menu"] = base_df["Recipe ID"].isin(st.session_state.menu_recipe_ids)
    st.session_state.editor_base_df = base_df

# Guard against no filter matches and write the editor
if len(filtered_df) == 0:
    st.caption("No recipes match those filters")
else:
    edited_df = st.data_editor(
    st.session_state.editor_base_df,
    key=editor_key,
    hide_index=True,
    column_config={"Recipe ID": None},
    disabled=["Recipe", "Type"],
)
    
    # Copy user inputs to the session state list
    checked = {int(r) for r in edited_df.loc[edited_df["Add to Menu"], "Recipe ID"]}
    unchecked = {int(r) for r in edited_df.loc[~edited_df["Add to Menu"], "Recipe ID"]}
    current = set(st.session_state.menu_recipe_ids)
    st.session_state.menu_recipe_ids = sorted((current | checked) - unchecked)

# Display what's on the menu
chosen = recipe_selection_df[recipe_selection_df["Recipe ID"].isin(st.session_state.menu_recipe_ids)]
st.write(f"On this menu ({len(chosen)}): " + ", ".join(chosen["Recipe"]))
st.space("small")

# Organize menu by courses
with st.expander("Organize by course (optional)"):
    for rid, name in zip(chosen["Recipe ID"], chosen["Recipe"]):
        col_a, col_b = st.columns([3, 5])
        col_a.write(name)
        col_b.segmented_control("Course", COURSES, key=f'course_{int(rid)}', label_visibility="collapsed")

# Store the items and their selected courses
items = [{"recipe_id": int(rid), "course": st.session_state.get(f"course_{int(rid)}")}
        for rid in st.session_state.menu_recipe_ids]

# Count items per course
counts = Counter(st.session_state.get(f"course_{int(r)}") for r in st.session_state.menu_recipe_ids)
st.caption("  ·  ".join(f"{c}: {counts.get(c, 0)}" for c in COURSES))

# Rest of user input
menu_notes = st.text_area("Any notes you want to make?")
menu_status = st.selectbox("Is the menu complete?", options=DEFAULT_STATUSES, index=1)

# Save entries to table
if create_button(name='save_menu'):

    menu_id = create_menu(conn=conn,
                          menu_name=menu_name,
                          menu_notes=menu_notes,
                          menu_status=menu_status)

    save_menu(conn=conn,
              menu_id=menu_id,
              recipes=items)

    # Clear existing values
    st.session_state.menu_id = None

    st.switch_page(PAGES['menus'])
