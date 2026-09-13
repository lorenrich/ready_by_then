# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database import get_connection
from events import create_event

# Create the connection to the database
conn = get_connection()

# Convert events table from db to a dataframe
df = pd.read_sql_query("SELECT * FROM events", conn)

# Configure browser tab
st.set_page_config(page_title="Ready by Then", layout="wide")

# Title
st.title("Events")
st.write(" ")

# Buttons
if st.button("Create new event", type="primary", icon=":material/event:"):
    st.switch_page("pages/create_event_page.py")

# Table of events
if df.empty:
    st.write("You do not have any events logged")
else:
    st.dataframe(df, use_container_width=True)
