# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database import get_connection
from events import create_event

# Create the connection to the database
conn = get_connection()

# Configure browser tab
st.set_page_config(page_title="Ready by Then", layout="wide")

# Title
st.title("Create New Event")
st.write(" ")

# Form
with st.form("create_event"):
    st.write("Let's get started!")
    event_name = st.text_input("Give your event a name")
    event_date = st.datetime_input("When is your event?")
    num_adults = st.number_input("Number of adults attending", step=1)
    num_kids = st.number_input("Number of kids attending", step=1)
    kids_eat_meal = st.selectbox("Will the kids eat the main meal (select no if the kids need separate food just for them)?",
                                 ["Yes", "No"],
                                 index=None,
                                 accept_new_options=False)
    will_kids_eat_adult_meal = 1 if kids_eat_meal == "Yes" else 0
    dietary_needs = st.text_area("Does anyone have dietary needs or preferences?")
    event_complete = st.selectbox("Has this event already happened?",
                                  ["Yes", "No"],
                                  index=None,
                                  accept_new_options=False)
    event_complete_final = 1 if event_complete == "Yes" else 0
    notes = st.text_area("Any extra notes you want to add?")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
       create_event(conn,
                    name=event_name, 
                    event_date=event_date, 
                    num_adults=num_adults, 
                    num_kids=num_kids, 
                    will_kids_eat_adult_meal=will_kids_eat_adult_meal, 
                    dietary_needs=dietary_needs,
                    event_complete=event_complete_final,
                    notes=notes)
       