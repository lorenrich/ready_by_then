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
from database.recipes import get_selected_recipe, get_selected_recipe_ingredients, copy_recipe, delete_recipe
from styles.page_config import setup_page_defaults, pages, buttons, create_button

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
                st.switch_page(pages["recipes"])
            else:
                st.error("Nothing was deleted. The recipe may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()

# Connect to database
conn = get_connection()

# Set up page defaults
setup_page_defaults()

# Identify selected recipe and filter dataframe
recipe_id = st.session_state.get("selected_recipe_id")

# Create dataframes
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None
selected_recipe_ingredients_df = get_selected_recipe_ingredients(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None

# Guard against empty dataframe else filter it to the selected recipe
if recipe_id is None:
    st.warning("No recipe selected")

if selected_recipe_df is None:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(pages['recipes'])

# Title
st.title("Recipe Details")
st.space("small")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(pages['edit_recipe'])

with button_col_2:
    if create_button(name='copy'):
        st.switch_page(pages['copy_recipe'])
    
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

    ingredient_col1, ingredient_col2 = st.columns([1, 7], gap="small")  # ingredient_col1 intentionally left blank

    with ingredient_col2:
        if selected_recipe_ingredients_df is None:
            st.markdown("*No ingredients listed.  Select **Edit** to start adding.*")
        else:
            for row in selected_recipe_ingredients_df.itertuples():
                parts = [row.ingredient_name]
                if pd.notna(row.amount):
                    parts.append(f"{row.amount:g}")
                if pd.notna(row.unit):
                    parts.append(row.unit)
                st.write(" ".join(parts))

st.space("small")

with st.container():
    usage_menus, usage_events = st.columns(2, border=True)

    with usage_menus:
        st.markdown("**Menus**")

    with usage_events:
        st.markdown("**Events**")




