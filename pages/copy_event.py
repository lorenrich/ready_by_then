# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from database.database import get_connection, DEFAULT_STATUSES
from database.events import get_selected_event, create_event
from pages.event_details import event_id as copied_event_id
from styles.page_config import setup_page_defaults, pages

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Create dataframe based on copied event data excluding the new ID to be generated
selected_event_df = get_selected_event(conn=conn, event_id=copied_event_id) if copied_event_id is not None else None

# Guard against empty dataframe else filter it to the selected event
if selected_event_df.empty:
    st.warning("That event couldn't be found.  It may have been deleted.")
    st.page_link(pages['events'], label="<- Back to Events")
    st.stop()

# Title
st.title("Copy Event")
st.space("small")

# Identify default index values for form selectbox
kids_menu_default_value = selected_event_df["need_kids_menu"]  # 1 or 0
if kids_menu_default_value == 1:  # Yes
    kids_menu_default_idx = 0  # Yes is first index
else:
    kids_menu_default_idx = 1

event_occurred_default_value = selected_event_df["event_occurred"]
if event_occurred_default_value == 1:
    event_occurred_default_idx = 0
else:
    event_occurred_default_idx = 1

# Form
with st.form("copy_event"):
    event_name = st.text_input("Event name", 
                               value=f"Copy of {selected_event_df["event_name"]}")
    event_date = st.datetime_input("Event Date", 
                                   value=selected_event_df["event_date"])
    num_adults = st.number_input("Number of adults attending", 
                                 step=1, 
                                 value=selected_event_df["num_adults"])
    num_kids = st.number_input("Number of kids attending", 
                               step=1, 
                               value=selected_event_df["num_kids"])
    num_hearty_eaters = st.number_input("How many of your guests are hearty eaters?", step=1, value=selected_event_df["num_hearty_eaters"])
    need_kids_menu = st.selectbox("Do you need a separate kids' menu (who doesn't love chicken nuggets and fries)?",
                                 ["Yes", "No"],
                                 index=kids_menu_default_idx,
                                 accept_new_options=False)
    kids_menu = 1 if need_kids_menu == "Yes" else 0
    dietary_needs = st.text_area("Does anyone have dietary needs or preferences?", 
                                 value=selected_event_df["dietary_needs"])
    event_occurred = st.selectbox("Has this event already happened?",
                                  ["Yes", "No"],
                                  index=event_occurred_default_idx,
                                  accept_new_options=False)
    event_occurred = 1 if event_occurred == "Yes" else 0
    event_notes = st.text_area("Any notes you want to make?", 
                               value=selected_event_df["event_notes"])
    event_status = st.selectbox("Are the event details complete?", options=DEFAULT_STATUSES, index=1)

    # Save 
    if st.form_submit_button("Save changes"):
       create_event(conn,
                  event_name=event_name, 
                  event_date=event_date, 
                  num_adults=num_adults, 
                  num_kids=num_kids, 
                  num_hearty_eaters=num_hearty_eaters,
                  need_kids_menu=kids_menu, 
                  dietary_needs=dietary_needs,
                  event_occurred=event_occurred,
                  event_notes=event_notes,
                  event_status=event_status)
       st.switch_page(pages['events'])
       