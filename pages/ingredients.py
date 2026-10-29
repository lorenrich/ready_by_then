# Import
import sys 
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from collections import Counter
from database.database import get_connection, update_and_default_selectbox
from database.recipes import (get_selected_recipe, 
                              get_selected_recipe_ingredients, 
                              save_ingredients, 
                              DEFAULT_RECIPE_SECTIONS, 
                              DEFAULT_INGREDIENT_NAMES, 
                              DEFAULT_UNITS, 
                              DEFAULT_PREP_OPTIONS, 
                              DEFAULT_INGREDIENT_TYPE,
                              PREP_LABELS)
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Connect to database
conn = get_connection()

# Identify selected recipe and filter dataframe.  Guard against user accessing page without being passed a recipe_id
if st.session_state.get("selected_recipe_id") is None:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

else:
    recipe_id = int(st.session_state.get("selected_recipe_id"))

# Guard against empty dataframe else filter it to the selected recipe
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id)

if selected_recipe_df is None:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

# Set up page
setup_page_defaults()

# Update page dropdowns
recipe_sections = update_and_default_selectbox(conn=conn, 
                                               table_name='recipe_sections', 
                                               col_name='section_name', 
                                               default_options=DEFAULT_RECIPE_SECTIONS)

ingredient_names = update_and_default_selectbox(conn=conn, 
                                                table_name='recipe_ingredients',
                                                col_name='ingredient_name', 
                                                default_options=DEFAULT_INGREDIENT_NAMES)

amount_units = update_and_default_selectbox(conn=conn,
                                            table_name='recipe_ingredients',
                                            col_name='unit',
                                            default_options=DEFAULT_UNITS)

# Title
st.title("Ingredients")
st.write(" ")

# Ingredient entry
with st.expander("Instructions"):
    st.write("Enter your ingredients and their amounts.  If an item isn't in the dropdown, type to enter a new option.")
    st.write('Recipes sometimes include other recipes.  When this happens, set the ingredient type to "Recipe".  For example, if '\
            'Chicken Soup contains "Homemade Broth" as a recipe within the recipe, Ready by Then will log "Homemade Broth" as a recipe for '\
            "you to complete later.")
    st.write("Prep Timing allows you to decide when it can be prepared.  For example, the main ingredients might be able to be prepped a day in "\
            "advance but garnishes are best left to prepare at meal time.  You can assign a prep time to a specific ingredient or an entire section.")
    st.write("You can come back and edit a recipe's ingredients at any time, even if it's marked complete.  We'll remind you when you have incomplete recipes.")

st.space("small")
st.write(f"**Recipe: {selected_recipe_df['recipe_name']}**")


'''
Get current recipe ingredients or initialize a fresh entry section if recipe_id doesn't match, wasn't selected, or if user returned to 
ingredients page after previously leaving it without saving
'''
rows = st.session_state.get("rows")
widgets_gone = bool(rows) and f"name_{rows[0]}" not in st.session_state

if st.session_state.get("rows_for_recipe") != recipe_id or widgets_gone:
    # Get current ingredients
    current_ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None
    if current_ingredients:
            st.session_state.rows = list(range(len(current_ingredients)))
            st.session_state.next_row_id = len(current_ingredients)

            for i, (name, section, item_type, amount, unit, prep, component_id) in enumerate(current_ingredients):
                st.session_state[f"name_{i}"] = name
                st.session_state[f"section_{i}"] = section
                st.session_state[f"type_{i}"] = item_type
                st.session_state[f"amount_{i}"] = amount
                st.session_state[f"unit_{i}"] = unit
                st.session_state[f"prep_{i}"] = PREP_LABELS.get(prep)
                st.session_state[f"component_id_{i}"] = component_id

    else:
        # Initialize a fresh entry section
        st.session_state.rows=[0]
        st.session_state.next_row_id = 1
    st.session_state.rows_for_recipe = recipe_id

# Set up entry fields
for rid in st.session_state.rows:
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1.25, 1, 1.5, 1.25, 0.6], vertical_alignment="bottom")

    c1.selectbox("Section", 
                options=recipe_sections, 
                index=None, 
                accept_new_options=True,
                key=f"section_{rid}", 
                label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c2.selectbox("Ingredient", 
                options=ingredient_names, 
                index=None, 
                accept_new_options=True, 
                key=f"name_{rid}",
                label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")

    c3.selectbox("Type",
                options=DEFAULT_INGREDIENT_TYPE,
                accept_new_options=False,
                key=f"type_{rid}",
                label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c4.number_input("Amount", 
                    min_value=0.0, 
                    value=None, 
                    key=f"amount_{rid}",
                    label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c5.selectbox("Unit", 
                options=amount_units, 
                index=None, 
                accept_new_options=True, 
                key=f"unit_{rid}",
                label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c6.selectbox("Prep timing", 
                list(DEFAULT_PREP_OPTIONS), 
                index=None, 
                key=f"prep_{rid}",
                label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")

    if c7.button("", icon=":material/delete:", key=f"del_{rid}"):
        st.session_state.rows.remove(rid)
        st.rerun()

if st.button("Add ingredient", icon=":material/add:"):
    st.session_state.rows.append(st.session_state.next_row_id)
    st.session_state.next_row_id += 1
    st.rerun()


'''
Save and write to tables
'''
if create_button(name='save_ingredients'):
    items = []
    for rid in st.session_state.rows:
        name = (st.session_state.get(f"name_{rid}") or "").strip()

        if not name:
            continue  # Skip blank rows

        items.append({
            "section": (st.session_state.get(f"section_{rid}") or "").strip() or None,
            "name": name,
            "type": st.session_state[f"type_{rid}"],
            "amount": st.session_state[f"amount_{rid}"],
            "unit": st.session_state[f"unit_{rid}"],
            "prep": DEFAULT_PREP_OPTIONS.get(st.session_state.get(f"prep_{rid}")),
        })

    # Guard against no data
    if not items:
        st.warning("Add at least one ingredient."); st.stop()
        
    # Guard against duplicates
    values = [d['name'] for d in items]
    duplicates = [k for k, v in Counter(values).items() if v > 1]

    if not duplicates:
        # Save ingredients
        try:
            save_ingredients(conn, recipe_id, items)
        except ValueError as e: st.error(str(e)); st.stop()

        # Start the next visit cleanly
        st.session_state.rows_for_recipe = None

        st.switch_page(pages['recipe_details'])
    else:
        st.warning("It looks like you have duplicate ingredients in your recipe. Remove or combine them before saving.")

  
    