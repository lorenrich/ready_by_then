# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from datetime import datetime
from database.database import get_connection
from database.events import get_selected_event, delete_event
from styles.page_config import PAGES, setup_page_defaults, create_button, create_page_header, create_subheader

@st.dialog("Delete event?")
def confirm_delete(event_id):
    st.write("This permanently deletes the event. This action cannot be undone.")
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

# Prep data before rendering
kids_amt = f", {selected_event_df['num_kids']} kids" if selected_event_df['num_kids'] > 0 else ""

event_date = datetime.strptime(selected_event_df['event_date'], "%Y-%m-%d %H:%M:%S").date()
event_time = datetime.strptime(selected_event_df['event_date'], "%Y-%m-%d %H:%M:%S").time()
event_time = event_time.strftime("%I:%M %p")

month = event_date.strftime("%B")
day = event_date.strftime("%d")
year = event_date.strftime("%Y")

# Page header
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/today: Events')

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
col1, col2 = st.columns(2, border=True)

with col1:
    info_col1, info_col2 = st.columns([1, 3], gap="small")
    with info_col1:
        st.markdown("**Event:**", text_alignment="right")
        st.markdown("**Date:**", text_alignment="right")
        st.markdown("**Time:**", text_alignment="right")
        st.markdown("**Guests:**", text_alignment="right")
        st.space("small")
        st.markdown("**Event Status:**", text_alignment="right")

    with info_col2:
        st.write(selected_event_df['event_name'])
        st.write(f'{month} {day}, {year}')
        st.text(event_time)
        st.write(f"{selected_event_df['num_adults']} adults{kids_amt}")
        st.space("small")
        st.write(selected_event_df['event_status'])

with col2:
    st.write("On the menu")

    if create_button(name='add_menu_to_event'):
        st.switch_page(PAGES['event_menus'])
    

container = st.container(border=True)

with container:
    st.markdown("**Notes:**")
    st.write(selected_event_df['event_notes'])
 
