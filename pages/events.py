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
     PAGES, 
     setup_page_defaults,
     create_button, 
     create_page_header, 
     create_no_records_container,  
     fill_no_records_container,
     render_list
)

# Create the connection to the database
conn = get_connection()

# Set up page
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

    st.html(create_no_records_container('no_events'))
    blank_container = st.container(height=250, key='no_events', horizontal_alignment='center')

    fill_no_records_container(container=blank_container,
                              icon_name='events',
                              header_val='Create your first event',
                              caption_val='Plan menus, guests, and to-do lists all in one place',
                              button_name='create_event',
                              page_redirect='create_event')

# List recorded events    
else:
    # Buttons
    create_button_container = st.container(horizontal=True)
    with create_button_container:
        if create_button(name='create_event'):
            st.switch_page(PAGES['create_event'])

    # Render table
    df = df.fillna('')

    rows = df.to_dict("records")

    columns = [
    ("Event", "Event", 4, "link"),
    ("Event Date", "Event Date", 2, "date"),
    ("Guests", "Guests", 2, "integer"),
    ("Status", "Status", 2, "badge"),
    ]

    def open_event(event_id):
        st.session_state["selected_event_id"] = int(event_id)
        st.switch_page(PAGES['event_details'])

    render_list(rows=rows,
                columns=columns,
                id_field='Event ID',
                on_open=open_event,
                prefix='Events')
