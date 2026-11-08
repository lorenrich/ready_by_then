# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from collections import Counter
from database.database import DEFAULT_STATUSES, get_connection, update_and_default_selectbox
from database.menus import COURSES, get_selected_menu, get_selected_menu_recipes, edit_menu, save_menu
from database.recipes import DEFAULT_UNITS, DEFAULT_PREP_OPTIONS, PREP_LABELS, get_recipes_for_menu_selection
from database.food_and_drink import get_items_for_menu_selection, get_selected_menu_items_for_edit, save_menu_items
from styles.page_config import PAGES, setup_page_defaults, create_button

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Initialize session states
menu_id = st.session_state.get("selected_menu_id")

if "menu_recipe_ids" not in st.session_state:
    st.session_state.menu_recipe_ids = []

if "menu_item_ids" not in st.session_state:
    st.session_state.menu_item_ids = []

# Create dataframes
selected_menu_df = get_selected_menu(conn=conn, menu_id=menu_id) if menu_id is not None else None
selected_menu_recipes = get_selected_menu_recipes(conn=conn, menu_id=menu_id) if menu_id is not None else None
recipe_selection_df = get_recipes_for_menu_selection(conn=conn)
item_selection_df = get_items_for_menu_selection(conn=conn)

# Update page dropdowns
amount_units = update_and_default_selectbox(conn=conn,
                                            table_name='recipe_ingredients',
                                            col_name='unit',
                                            default_options=DEFAULT_UNITS)

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
st.title("Edit Menu")
st.space("small")

menu_name = st.text_input("Menu name", value=menu_name)
st.space("small")

# Display existing recipe data
recipe_container = st.container(border=True)
with recipe_container:
    st.markdown("**Edit your recipes**")

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


# Get current food and drink items or initialize a fresh entry section if item_id doesn't match, wasn't selected, or if user returned to 
# ingredients page after previously leaving it without saving
item_rows = st.session_state.get("item_rows")
item_widgets_gone = bool(item_rows) and f"item_name_{item_rows[0]}" not in st.session_state

if st.session_state.get("item_rows_for_menu") != menu_id or item_widgets_gone:
    # Clear previously seeded entries
    prefixes = ("item_name_", "item_amount_", "item_unit_",
                "item_scale_", "item_prep_", "item_course_")
    for key in [k for k in st.session_state.keys() if k.startswith(prefixes)]:
        del st.session_state[key]

    # Seed entries
    current_items = get_selected_menu_items_for_edit(conn=conn, menu_id=menu_id)

    if current_items:
        st.session_state.item_rows = list(range(len(current_items)))
        st.session_state.next_item_row_id = len(current_items)

        for i, (name, course, amount, unit, scales, prep) in enumerate(current_items):
            st.session_state[f"item_name_{i}"] = name
            st.session_state[f"item_amount_{i}"] = amount or 0.0
            st.session_state[f"item_scale_{i}"] = "Yes" if scales else "No"
            if unit:
                st.session_state[f"item_unit_{i}"] = unit
            if prep is not None:
                label = PREP_LABELS.get(prep)
                if label:
                    st.session_state[f"item_prep_{i}"] = label
            if course in COURSES:
                st.session_state[f"item_course_{i}"] = course
    else:
        st.session_state.item_rows = [0]
        st.session_state.next_item_row_id = 1

    st.session_state.item_rows_for_menu = menu_id


# Set up entry fields
item_container = st.container(border=True)
with item_container:
    st.markdown("**Add other food and drinks**")

    item_rows = st.session_state.get("item_rows")

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
item_names = [(st.session_state.get(f"item_name_{rid}") or "").strip()
              for rid in st.session_state.item_rows]

chosen = recipe_selection_df[recipe_selection_df["Recipe ID"].isin(st.session_state.menu_recipe_ids)]
names = list(chosen["Recipe"]) + [n for n in item_names if n]
st.write(f"On this menu ({len(names)}): " + ", ".join(names))
st.space("small")

# Organize menu by courses
with st.expander("Organize by course (optional)"):
    for rid, name in zip(chosen["Recipe ID"], chosen["Recipe"]):
        col_a, col_b = st.columns([3, 5])
        col_a.write(name)
        col_b.segmented_control("Course", COURSES, key=f'course_{int(rid)}', label_visibility="collapsed")

    for rid, name in zip(st.session_state.item_rows, item_names):
        if not name:
            continue
        col_a, col_b = st.columns([3, 5])
        col_a.write(name)
        col_b.segmented_control("Course", COURSES, key=f"item_course_{rid}",
                                label_visibility="collapsed")

# Store the items and their selected courses
items = [{"recipe_id": int(rid), "course": st.session_state.get(f"course_{int(rid)}")}
        for rid in st.session_state.menu_recipe_ids]

# Count items per course
recipe_courses = [st.session_state.get(f"course_{int(r)}")
                  for r in st.session_state.menu_recipe_ids]
item_courses = [st.session_state.get(f"item_course_{rid}")
                for rid, name in zip(st.session_state.item_rows, item_names) if name]

counts = Counter(recipe_courses + item_courses)
st.caption("  ·  ".join(f"{c}: {counts.get(c, 0)}" for c in COURSES))

# Rest of user input
menu_notes = st.text_area("Any notes you want to make?", value=menu_notes, key="edit_menu_notes")
menu_status = st.selectbox("Is the menu complete?", options=DEFAULT_STATUSES, index=menu_status_idx)

# Save entries to table
if create_button(name='save_menu'):
    # Guard against no name
    if not menu_name.strip():
        st.error("Please give the menu a name")
        st.stop()

    menu_items = []
    for rid in st.session_state.item_rows:
        name = (st.session_state.get(f"item_name_{rid}") or "").strip()
        if not name:
            continue
        menu_items.append({
            "name": name,
            "course": st.session_state.get(f"item_course_{rid}"),
            "amount": st.session_state.get(f"item_amount_{rid}") or None,
            "unit": st.session_state.get(f"item_unit_{rid}"),
            "scales": 1 if st.session_state.get(f"item_scale_{rid}") == "Yes" else 0,
            "prep": DEFAULT_PREP_OPTIONS.get(st.session_state.get(f"item_prep_{rid}")),
        })

    lowered = [i["name"].lower() for i in menu_items]
    if len(lowered) != len(set(lowered)):
        st.warning("An item appears more than once. Remove or combine the duplicates.")
        st.stop()

    # Write entries to tables
    if not edit_menu(conn=conn,
                     menu_name=menu_name.strip(),
                     menu_notes=menu_notes,
                     menu_status=menu_status,
                     menu_id=menu_id):
        st.error("Nothing was updated. The menu may have been deleted.")
        st.stop()

    save_menu(conn=conn, menu_id=menu_id, recipes=items)
    save_menu_items(conn=conn, menu_id=menu_id, items=menu_items)

    # Reset
    st.session_state.menu_for_id = None
    st.session_state.item_rows_for_menu = None
    st.switch_page(PAGES['menus'])

    