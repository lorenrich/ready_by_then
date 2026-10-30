# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.events import get_selected_event, delete_event
from styles.page_config import setup_page_defaults, PAGES, create_button

@st.dialog("Delete event?")
def confirm_delete(event_id):
    st.write("This permanently deletes the event and its menu. This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if create_button(name="confirm_delete"):
            deleted = delete_event(conn, event_id=event_id)
            if deleted:
                st.switch_page(PAGES["events"])
            else:
                st.error("Nothing was deleted. The event may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Identify selected event and filter dataframe
event_id = st.session_state.get("selected_event_id")

# Create dataframe
selected_event_df = get_selected_event(conn=conn, event_id=event_id) if event_id is not None else None

# Guard against empty dataframe else filter it to the selected event
if event_id is None:
    st.warning("No event selected")

if selected_event_df is None:
    st.warning("That event couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['events'], label="<- Back to Events")
    st.stop()

# Page navigation
if create_button(name='back'):
    st.switch_page(PAGES['events'])

# Title
st.title("Event Details")
st.space("small")

# Modify buttons
button_col_1, button_col_2, button_col_3 = st.columns(3, gap="small", vertical_alignment="top")

with button_col_1:
    if create_button(name='edit'):
        st.switch_page(PAGES['edit_event'])

with button_col_2:
    if create_button(name='copy'):
        st.switch_page(PAGES['copy_event'])
    
with button_col_3:
    if create_button(name='delete'):
        confirm_delete(event_id=int(selected_event_df['event_id']))

st.space("small")

# Event Details
st.write(selected_event_df['event_name'])
st.write("")

