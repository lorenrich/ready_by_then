# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.events import create_event
from styles.page_config import setup_page_defaults, pages, buttons

# Connect to database
conn = get_connection()

# Set up pages
setup_page_defaults()

# Title
st.title("Create New Event")
st.write(" ")

# Form
with st.form("create_event"):
    st.write("Let's get started!")
    event_name = st.text_input("What should we call the event?")
    event_date = st.datetime_input("When is your event?")
    num_adults = st.number_input("Number of adults attending", 
                                 step=1)
    num_kids = st.number_input("Number of kids attending", 
                               step=1)
    num_hearty_eaters = st.number_input("How many of your guests are hearty eaters?",
                                        step=1)
    need_kids_menu = st.selectbox("Do you need a separate kids' menu (who doesn't love chicken nuggets and fries)?",
                                 ["Yes", "No"],
                                 index=None,
                                 accept_new_options=False)
    kids_menu = 1 if need_kids_menu == "Yes" else 0
    dietary_needs = st.text_area("Does anyone have dietary needs or preferences?")
    event_complete = st.selectbox("Has this event already happened?",
                                  ["Yes", "No"],
                                  index=None,
                                  accept_new_options=False)
    event_complete = 1 if event_complete == "Yes" else 0
    event_notes = st.text_area("Any notes you want to make?")

    # Submit
    if st.form_submit_button("Submit"):
       create_event(conn,
                    event_name=event_name, 
                    event_date=event_date, 
                    num_adults=num_adults, 
                    num_kids=num_kids, 
                    num_hearty_eaters=num_hearty_eaters,
                    need_kids_menu=kids_menu, 
                    dietary_needs=dietary_needs,
                    event_complete=event_complete,
                    event_notes=event_notes)
       st.switch_page(pages['events'])
       