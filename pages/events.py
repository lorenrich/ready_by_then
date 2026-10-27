# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection
from database.events import get_events_for_display
from styles.page_config import (
     setup_page_defaults, 
     pages, buttons, create_button, create_page_header, no_data_container, create_no_entries_container, CIRCULAR_ICONS, create_subheader
)

# Create the connection to the database
conn = get_connection()

# Set up page defaults
setup_page_defaults()

# Read in dataframe
df = get_events_for_display(conn=conn)

# Page header
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/today: Events')

# No events page
if df.empty:
    st.html(create_no_entries_container("no_events"))
    blank_container = st.container(height=250, key="no_events", horizontal_alignment='center')

    with blank_container:
        col1, col2, col3 = st.columns(3)

        with col2:
            st.image(CIRCULAR_ICONS['events'], width=50)

            create_subheader('Create your first event')
            st.caption("Plan menus, guests, and to-do lists all in one place")

            if create_button(name='create_event'):
                st.switch_page(pages['create_event'])
    
else:
    # Buttons
    col1, col2 = st.columns([1, 11])
    with col1:
        if create_button(name='back'):
            st.switch_page(pages['home'])
    with col2:
        if create_button(name='create_event'):
                st.switch_page(pages['create_event'])

    # Data table
    event_table = st.dataframe(
        df, 
        on_select="rerun",
        selection_mode="single-row",
        hide_index=True, 
        width="stretch")

    selected = event_table.selection.rows
    if selected:
        st.session_state["selected_event_id"] = int(df.iloc[selected[0]]["Event ID"])
        st.switch_page(pages['event_details'])
