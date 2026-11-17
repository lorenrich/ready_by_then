# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, 
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import DEFAULT_STATUSES, get_connection
from database.events import create_event
from styles.page_config import PAGES, setup_page_defaults, create_page_header

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Title
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/today: Events')

# Form
with st.form("create_event"):
    st.write("Let's get started!")
    event_name = st.text_input("What should we call the event?")
    event_date = st.datetime_input("When is your event?")
    event_serving_time = st.time_input("What time are you serving food?")
    num_adults = st.number_input("Number of adults attending", 
                                 step=1)
    num_kids = st.number_input("Number of kids attending", 
                               step=1)
    event_notes = st.text_area("Any notes you want to make?")

    event_status = st.selectbox("Are the event details complete?", 
                                options=DEFAULT_STATUSES, 
                                index=1)

   # Take user to add_ingredients or submit as-is
    col1, col2 = st.columns([1, 7], gap="small")

    with col1:
        add_now = st.form_submit_button("Add menus", type="primary")
    with col2:
        add_later = st.form_submit_button("I'll add menus later")

    if add_now or add_later:
        if not event_name.strip():
            st.error("Please give the event a name.")
            st.stop()

        new_event_id = create_event(conn,
                                    event_name=event_name, 
                                    event_date=event_date, 
                                    num_adults=num_adults, 
                                    num_kids=num_kids,
                                    event_notes=event_notes,
                                    event_status=event_status,
                                    event_serving_time=event_serving_time)

        if add_now:
            st.session_state["selected_event_id"] = new_event_id
            st.switch_page(PAGES["event_menus"])
        else:
            st.switch_page(PAGES["events"])
          
       