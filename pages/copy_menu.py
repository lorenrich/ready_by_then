# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from collections import Counter
from database.database import DEFAULT_STATUSES, get_connection
from database.menus import COURSES, get_selected_menu, get_selected_menu_recipes, create_menu, save_menu
from database.recipes import get_recipes_for_menu_selection
from database.food_and_drink import get_selected_menu_items
from styles.page_config import PAGES, setup_page_defaults, create_button

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Initialize session states
menu_id = st.session_state.get("selected_menu_id")

if "menu_recipe_ids" not in st.session_state:
    st.session_state.menu_recipe_ids = []

# Create dataframes
selected_menu_df = get_selected_menu(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_recipes = get_selected_menu_recipes(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_items = get_selected_menu_items(conn=conn, menu_id=menu_id) if menu_id is not None else None
recipe_selection_df = get_recipes_for_menu_selection(conn=conn)

# Guard against empty dataframe else filter it to the selected menu
if menu_id is None:
    st.warning("No menu selected")

if selected_menu_df is None:
    st.warning("That menu couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['menus'], label="<- Back to Menus")
    st.stop()

# Determine if initializing is needed
needs_init = (st.session_state.get("menu_for_id") != menu_id or "edit_menu_notes" not in st.session_state)

# Seed existing recipes tagged to menu
if needs_init:
    # Clear leftovers from any previously viewed menu
    stale = [k for k in st.session_state.keys()
            if k.startswith("course_") or k.startswith("menu_editor_") or k == "editor_base_df"]
    for key in stale:
        del st.session_state[key]

    # Load the saved recipe IDs into the list
    st.session_state.menu_recipe_ids = [int(rid) for rid, name, status, course in selected_menu_recipes]

    # Seed each saved course into its widget key
    for rid, name, status, course in selected_menu_recipes:
        if course in COURSES:
            st.session_state[f"course_{int(rid)}"] = course

    st.session_state.menu_for_id = menu_id

# Remaining user selections
menu_name = selected_menu_df['menu_name']
menu_notes = selected_menu_df['menu_notes']

if selected_menu_df['menu_status'] == 'Complete':
    menu_status_idx = 0
else:
    menu_status_idx = 1

# Title
st.title("Copy Menu")
st.space("small")

# Display existing menu data
menu_name = st.text_input("Menu name", value=f"Copy of {menu_name}")
st.space("small")

st.write("Edit your recipes")

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
menu_notes = st.text_area("Any notes you want to make?", value=menu_notes, key="edit_menu_notes")
menu_status = st.selectbox("Is the menu complete?", options=DEFAULT_STATUSES, index=menu_status_idx)

# Save entries to table
if create_button(name='save_menu'):
    if not menu_name.strip():
        st.error("Please give the menu a name")
        st.stop()

    new_menu_id = create_menu(conn=conn,
                            menu_name=menu_name.strip(),
                            menu_notes=menu_notes,
                            menu_status=menu_status)

    save_menu(conn=conn,
              menu_id=new_menu_id,
              recipes=items)

    # Clear existing values
    st.session_state.menu_for_id = None

    st.session_state["selected_menu_id"] = new_menu_id

    st.switch_page(PAGES['menus'])
