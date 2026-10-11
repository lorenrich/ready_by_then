# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database import get_connection
from recipes import create_recipe

# Create the connection to the database
conn = get_connection()

# Convert events table from db to a dataframe
df = pd.read_sql_query("SELECT * FROM recipes", conn)

# Configure browser tab
st.set_page_config(page_title="Ready by Then", layout="wide")

# Title
st.title("Recipes")
st.write(" ")

# Buttons
if st.button("Create new recipe", type="primary", icon=":material/event:"):
    st.switch_page("pages/create_recipe_page.py")

# Table of events
if df.empty:
    st.write("You do not have any recipes logged")
else:
    st.dataframe(df, use_container_width=True)
