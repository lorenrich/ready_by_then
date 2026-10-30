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
from database.recipes import get_selected_recipe, get_selected_recipe_ingredients, delete_recipe
from styles.page_config import setup_page_defaults, PAGES, create_button

@st.dialog("Delete recipe?")
def confirm_delete(recipe_id):
    st.write("This permanently deletes the recipe. This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if create_button(name="confirm_delete"):
            try:
                deleted = delete_recipe(conn, recipe_id=recipe_id)
            except sqlite3.IntegrityError:
                st.error("This recipe is used as a component in another recipe. Remove it there first.")
                st.stop()
            if deleted:
                st.switch_page(PAGES["recipes"])
            else:
                st.error("Nothing was deleted. The recipe may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()


def format_item(name, amount, unit):
    parts = []
    if amount is not None:
        parts.append(f"{amount:g}")
    if unit:
        parts.append(unit)
    quantity = " ".join(parts)
    return f"{name}, {quantity}" if quantity else name


def section_sort_key(section_name):
    lowered = section_name.lower()
    if lowered == "main":
        return (0, lowered)
    if lowered.startswith("garnish"):
        return (2, lowered)
    return (1, lowered)


# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Identify selected recipe and filter dataframe
recipe_id = st.session_state.get("selected_recipe_id")

# Create dataframes
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None
selected_recipe_ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None

# Guard against empty dataframe else filter it to the selected recipe
if recipe_id is None:
    st.warning("No recipe selected")

if selected_recipe_df is None:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['recipes'], label="<- Back to Recipes")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(PAGES['recipes'])

# Title
st.title("Recipe Details")
st.space("small")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(PAGES['edit_recipe'])

with button_col_2:
    if create_button(name='copy'):
        st.switch_page(PAGES['copy_recipe'])
    
with button_col_3:
    if create_button(name='delete'):
        confirm_delete(recipe_id=int(selected_recipe_df['recipe_id']))

st.space("small")

# Recipe details prep work
cooktops = [
        'burner',
        'cooktop',
        'stove'
    ]

if selected_recipe_df['recipe_cooking_vessel']:
    cooking_vessel = selected_recipe_df['recipe_cooking_vessel'].lower()
else:
    cooking_vessel = None

# Write recipe details to page
recipe_info_col, recipe_ingredient_col = st.columns(2, border=True)
with recipe_info_col:
    info_col1, info_col2 = st.columns([1, 3], gap="small")
    with info_col1:
        st.markdown("**Recipe:**", text_alignment="right")
        st.markdown("**Recipe Type:**", text_alignment="right")
        st.markdown("**Servings:**", text_alignment="right")
        st.markdown("**Cooking:**", text_alignment="right")
        st.markdown("**Source:**", text_alignment="right")
        st.markdown("**Recipe Notes:**", text_alignment="right")
        st.space("small")
        st.markdown("**Recipe Status:**", text_alignment="right")

    with info_col2:
        st.write(selected_recipe_df['recipe_name'])
        st.write(selected_recipe_df['recipe_type'] if selected_recipe_df['recipe_type'] else "&nbsp;")
        st.write(selected_recipe_df['recipe_yield'] if selected_recipe_df['recipe_yield'] else "&nbsp;")

        if not cooking_vessel:
            st.write("&nbsp;")
        elif cooking_vessel == 'oven':
            st.write(f"Bake at {selected_recipe_df['recipe_preheat_temp']} degrees {selected_recipe_df["recipe_preheat_unit"]} in {selected_recipe_df["recipe_cooking_vessel"]} for {selected_recipe_df['recipe_cook_time']}")
        elif cooking_vessel in cooktops:
            st.write(f"Cook on stove for {selected_recipe_df['recipe_cook_time']} (includes preheat time)")
            

        st.write(selected_recipe_df["recipe_source"] if selected_recipe_df['recipe_source'] else "&nbsp;")
        st.write(selected_recipe_df['recipe_notes'] if selected_recipe_df['recipe_notes'] else "&nbsp;")
        st.space("small")
        st.write(selected_recipe_df['recipe_status'] if selected_recipe_df['recipe_status'] else "&nbsp;")

with recipe_ingredient_col:
    st.markdown("**Ingredients**")
    st.space("small")

    sections = {}
    for name, section, item_type, amount, unit, prep, component_id in selected_recipe_ingredients:
        sections.setdefault(section or "Main", []).append(
            (name, item_type, amount, unit, component_id)
        )

    for section_name in sorted(sections, key=section_sort_key):
        label_col, items_col = st.columns([1, 4])
        label_col.markdown(f"**{section_name}**")
        with items_col:
            for name, item_type, amount, unit, component_id in sections[section_name]:
                if item_type == "Recipe":
                    with st.expander(f"{format_item(name, amount, unit)} (see recipe)"):
                        component_ingredients = get_selected_recipe_ingredients(conn, component_id)
                        if len(component_ingredients) == 0:
                            st.caption("No ingredients have been added.")
                        else:
                            for sub_name, sub_section, sub_item_type, sub_amount, sub_unit, sub_prep, sub_component_id in component_ingredients:
                                st.write(format_item(sub_name, sub_amount, sub_unit))
                            if st.button('Go to Recipe', key=f"open_{component_id}"):
                                st.session_state["selected_recipe_id"] = component_id
                                st.rerun()
                else:
                    st.write(format_item(name, amount, unit))

st.space("small")

with st.container():
    usage_menus, usage_events = st.columns(2, border=True)

    with usage_menus:
        st.markdown("**Menus**")

    with usage_events:
        st.markdown("**Events**")




