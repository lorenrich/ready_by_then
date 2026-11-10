# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from collections import Counter
from database.database import DEFAULT_STATUSES, get_connection, update_and_default_selectbox
from database.menus import COURSES, create_menu, save_menu
from database.recipes import DEFAULT_PREP_OPTIONS, DEFAULT_UNITS, get_recipes_for_menu_selection
from database.food_and_drink import get_items_for_menu_selection, save_menu_items
from styles.page_config import PAGES, setup_page_defaults, create_button, create_page_header

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Initialize session state
if "menu_recipe_ids" not in st.session_state:
    st.session_state.menu_recipe_ids = []

if "menu_item_ids" not in st.session_state:
    st.session_state.menu_item_ids = []

# Set up dataframes
recipe_selection_df = get_recipes_for_menu_selection(conn=conn)
item_selection_df = get_items_for_menu_selection(conn=conn)

# Update page dropdowns
amount_units = update_and_default_selectbox(conn=conn,
                                            table_name='recipe_ingredients',
                                            col_name='unit',
                                            default_options=DEFAULT_UNITS)

# Title
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Create Menu')

# Menu creation entry
st.write("Let's get started!")

menu_name = st.text_input("Create a menu name")
st.space("small")


# Recipe selector
recipe_container = st.container(border=True)
with recipe_container:
    st.markdown("**Add recipes**")

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

st.space("small")

# Food and drink item selector
item_container = st.container(border=True)
with item_container:
    st.markdown("**Add other food and drinks**")

    item_rows = st.session_state.get("item_rows")
    if item_rows is None or (item_rows and f"item_name_{item_rows[0]}" not in st.session_state):
        st.session_state.item_rows = [0]
        st.session_state.next_item_row_id = 1

    # Set up entry fields
    for rid in st.session_state.item_rows:
        c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.25, 1, 1.5, 1.25, 0.6], vertical_alignment="bottom")
        
        c1.selectbox("Item", 
                    options=item_selection_df['Item'].tolist(), 
                    index=None, 
                    accept_new_options=True, 
                    key=f"item_name_{rid}",
                    label_visibility="visible" if rid == st.session_state.item_rows[0] else "collapsed")
        
        c2.number_input("Amount", 
                        min_value=0.0, 
                        value=0.0, 
                        key=f"item_amount_{rid}",
                        label_visibility="visible" if rid == st.session_state.item_rows[0] else "collapsed")
        
        c3.selectbox("Unit", 
                    options=amount_units, 
                    index=None, 
                    accept_new_options=True, 
                    key=f"item_unit_{rid}",
                    label_visibility="visible" if rid == st.session_state.item_rows[0] else "collapsed")

        c4.selectbox("Scale amount with guest count",
                    options=['No', 'Yes'],
                    accept_new_options=False,
                    key=f"item_scale_{rid}",
                    label_visibility="visible" if rid == st.session_state.item_rows[0] else "collapsed")
        
        c5.selectbox("Prep timing", 
                    list(DEFAULT_PREP_OPTIONS), 
                    index=None, 
                    key=f"item_prep_{rid}",
                    label_visibility="visible" if rid == st.session_state.item_rows[0] else "collapsed")

        if c6.button("", icon=":material/delete:", key=f"item_del_{rid}"):
            st.session_state.item_rows.remove(rid)
            st.rerun()

    if st.button("Add item", icon=":material/add:"):
        st.session_state.item_rows.append(st.session_state.next_item_row_id)
        st.session_state.next_item_row_id += 1
        st.rerun()

st.space("small")

# Display what's on the menu
chosen = recipe_selection_df[recipe_selection_df["Recipe ID"].isin(st.session_state.menu_recipe_ids)]

item_names = [(st.session_state.get(f"item_name_{rid}") or "").strip()
              for rid in st.session_state.item_rows]
item_names = [n for n in item_names if n]

names = list(chosen["Recipe"]) + item_names
st.write(f"On this menu ({len(names)}): " + ", ".join(names))

st.space("small")

# Organize menu by courses
with st.expander("Organize your menu by course (optional)"):
    # Guard against no chosen recipes or items
    if chosen.empty and not any((st.session_state.get(f"item_name_{r}") or "").strip()
                                for r in st.session_state.item_rows):
         st.caption("Add recipes or items above to organize them by course.")

    # Populate the expander
    for rid, name in zip(chosen["Recipe ID"], chosen["Recipe"]):
        col_a, col_b = st.columns([3, 5])
        col_a.write(name)
        col_b.segmented_control("Course", COURSES, key=f'course_{int(rid)}', label_visibility="collapsed")

    for rid in st.session_state.item_rows:
        name=(st.session_state.get(f"item_name_{rid}") or "").strip()
        if not name:
            continue
        col_a, col_b = st.columns([3, 5])
        col_a.write(name)
        col_b.segmented_control("Course", COURSES, key=f'item_course_{int(rid)}', label_visibility="collapsed")

# Store the items and their selected courses
recipe_courses = [st.session_state.get(f"course_{int(r)}")
                    for r in st.session_state.menu_recipe_ids]

item_courses = [st.session_state.get(f"item_course_{rid}")
                for rid in st.session_state.item_rows
                if (st.session_state.get(f"item_name_{rid}") or "").strip()]

items = [{"recipe_id": int(rid), "course": st.session_state.get(f"course_{int(rid)}")}
         for rid in st.session_state.menu_recipe_ids]

# Count items per course
counts = Counter(recipe_courses + item_courses)
st.caption("  ·  ".join(f"{c}: {counts.get(c, 0)}" for c in COURSES))

# Rest of user input
menu_notes = st.text_area("Any notes you want to make?")
menu_status = st.selectbox("Is the menu complete?", options=DEFAULT_STATUSES, index=1)


# Save entries to tables
if create_button(name='save_menu'):
    
    # Build dictionary of items
    menu_items = []
    for rid in st.session_state.item_rows:
        name = (st.session_state.get(f"item_name_{rid}") or "").strip()
        if not name:
            continue
        menu_items.append({
            "name": name,
            "course": st.session_state.get(f"item_course_{rid}"),
            "amount": st.session_state.get(f"item_amount_{rid}"),
            "unit": st.session_state.get(f"item_unit_{rid}"),
            "scales": 1 if st.session_state.get(f"item_scale_{rid}") == "Yes" else 0,
            "prep": DEFAULT_PREP_OPTIONS.get(st.session_state.get(f"item_prep_{rid}")),
        })

    # Guard against no menu name
    if not menu_name.strip():
        st.error("Please give the menu a name")
        st.stop()

    lowered = [i["name"].lower() for i in menu_items]
    if len(lowered) != len(set(lowered)):
        st.warning("An item appears more than once. Remove or combine the duplicates.")
        st.stop()

    # Run save functions
    menu_id = create_menu(conn=conn,
                          menu_name=menu_name,
                          menu_notes=menu_notes,
                          menu_status=menu_status)

    save_menu(conn=conn,
              menu_id=menu_id,
              recipes=items)

    save_menu_items(conn=conn,
                    menu_id=menu_id,
                    items=menu_items)

    # Clear existing values
    st.session_state.menu_recipe_ids = []
    st.session_state.pop("item_rows", None)

    st.switch_page(PAGES['menus'])
