# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, 
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import DEFAULT_STATUSES, get_connection
from database.events import get_selected_event, create_event
from styles.page_config import PAGES, setup_page_defaults, create_page_header

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

copied_event_id = st.session_state.get("selected_event_id")

# Create dataframe based on copied event data
selected_event_df = \
    get_selected_event(conn=conn, 
                       event_id=copied_event_id) \
                        if copied_event_id is not None else None

# Guard against empty dataframe else filter it to the selected event
if selected_event_df.empty:
    st.warning("That event couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['events'], label="<- Back to Events")
    st.stop()

# Title
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/today: Events')
st.space("small")


# Form
with st.form("copy_event"):
    event_name = \
        st.text_input("Event name", 
                      value=f"Copy of {selected_event_df["event_name"]}")
    event_date = st.datetime_input("Event Date", 
                                   value=selected_event_df["event_date"])
    event_serving_time = st.time_input("Food Serve Time",
                                       value=selected_event_df['serving_time'])
    num_adults = st.number_input("Number of adults attending", 
                                 step=1, 
                                 value=selected_event_df["num_adults"])
    num_kids = st.number_input("Number of kids attending", 
                               step=1, 
                               value=selected_event_df["num_kids"])
    event_notes = st.text_area("Any notes you want to make?", 
                               value=selected_event_df["event_notes"])
    event_status = st.selectbox("Are the event details complete?", 
                                options=DEFAULT_STATUSES, 
                                index=1)

    # Save 
    if st.form_submit_button("Save changes"):
       create_event(conn,
                  event_name=event_name, 
                  event_date=event_date, 
                  num_adults=num_adults, 
                  num_kids=num_kids,
                  event_notes=event_notes,
                  event_status=event_status,
                  event_serving_time=event_serving_time)
       st.switch_page(PAGES['events'])
       