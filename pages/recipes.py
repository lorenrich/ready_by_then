# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection
from database.recipes import get_recipes_for_display
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Create the connection to the database
conn = get_connection()

# Set up page defaults
setup_page_defaults()

# Read in dataframe
df = get_recipes_for_display(conn=conn)

# Title
st.title("Recipes")
st.space("small")

# Buttons
col1, col2 = st.columns([1, 8], gap="small")
with col1:
    if create_button(name='back'):
        st.switch_page(pages['home'])
with col2:
    if create_button(name='create_recipe'):
            st.switch_page(pages['create_recipe'])

# Table of events
if df.empty:
    st.write("You do not have any recipes logged")
    st.write(" ")
    
else:
    recipe_table = st.dataframe(
         df, 
         on_select="rerun",
         selection_mode="single-row",
         hide_index=True, 
         width="stretch")

    selected = recipe_table.selection.rows
    if selected:
        st.session_state["selected_recipe_id"] = int(df.iloc[selected[0]]["Recipe ID"])
        st.switch_page(pages['recipe_details'])
