# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection
from database.events import get_selected_event, delete_event
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Connect to database
conn = get_connection()

# Set up page defaults
setup_page_defaults()

# Identify selected event and filter dataframe
event_id = st.session_state.get("selected_event_id")

# Create dataframe
selected_event_df = get_selected_event(conn=conn, event_id=event_id) if event_id is not None else None

# Guard against empty dataframe else filter it to the selected event
if selected_event_df is None:
    st.warning("That event couldn't be found.  It may have been deleted.")
    st.page_link(pages['events'], label="<- Back to Events")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(pages['events'])

# Title
st.title("Event Details")
st.space("small")

if event_id is None:
    st.warning("No event selected")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(pages['edit_event'])
with button_col_2:
    create_button(name='copy')  # Functionality not built, add into if statement when ready
with button_col_3:
    if create_button(name='delete'):

        @st.dialog("Delete event?")

        def confirm_delete(id):
            st.write("This permanently deletes the event and its menu.  This action cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                create_button(name='confirm_delete')
                delete_event(conn, event_id=id)
                st.switch_page(pages['events'])
            with col2:
                create_button(name='cancel')
                st.rerun()
        
        confirm_delete(id=selected_event_df['Event ID'])

st.space("small")

# Event Details
st.write(selected_event_df['Event'])
st.write("")

