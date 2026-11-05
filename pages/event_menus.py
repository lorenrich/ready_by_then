# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import pandas as pd
from datetime import datetime
from collections import Counter
from database.database import DEFAULT_STATUSES, get_connection
from database.events import get_selected_event
from database.menus import (COURSES, 
                            get_event_menus, 
                            get_selected_menu_recipes, 
                            get_menus_for_display,
                            render_menu, 
                            remove_menu_from_event, 
                            add_menu_to_event)
from styles.page_config import PAGES, setup_page_defaults, create_button, create_page_header

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Initialize session state
raw_id = st.session_state.get("selected_event_id")
if raw_id is None:
    st.warning("No event selected.")
    st.page_link(PAGES['events'], label="<- Back to Events")
    st.stop()
event_id = int(raw_id)

selected_event_df = get_selected_event(conn=conn, event_id=event_id)
if selected_event_df is None:
    st.warning("That event couldn't be found. It may have been deleted.")
    st.page_link(PAGES['events'], label="<- Back to Events")
    st.stop()

# Create event dataframe
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

# Event Details
col1, col2 = st.columns(2, border=True)

with col1:
    info_col1, info_col2 = st.columns([1, 3], gap="small")
    with info_col1:
        st.markdown("**Event:**", text_alignment="right")
        st.markdown("**Date:**", text_alignment="right")
        st.markdown("**Time:**", text_alignment="right")
        st.markdown("**Guests:**", text_alignment="right")

    with info_col2:
        st.write(selected_event_df['event_name'])
        st.write(f'{month} {day}, {year}')
        st.text(event_time)
        st.write(f"{selected_event_df['num_adults']} adults{kids_amt}")

with col2:
    st.markdown("**Notes**")
    st.write(selected_event_df['event_notes'])
    st.write(" ")
    st.markdown("**Dietary restrictions/preferences**")
    st.write(selected_event_df['dietary_needs'])

# Menu review and selection
event_menus = get_event_menus(conn=conn, event_id=event_id)

for mid, mname, mstatus in event_menus:
    with st.expander(mname):
        render_menu(get_selected_menu_recipes(conn=conn, menu_id=mid))
        if create_button(name='remove_menu', key=f"remove_menu_{mid}"):
            remove_menu_from_event(conn, event_id, mid)
            st.rerun()

attached = {mid for mid, _, _ in event_menus}
menu_display_df = get_menus_for_display(conn=conn)
available = menu_display_df[~menu_display_df["Menu ID"].isin(attached)]
names = dict(zip(available["Menu ID"].tolist(), available["Menu"]))

pick_key = f"add_menu_pick_{st.session_state.get('menu_pick_version', 0)}"
picked = st.selectbox("Add a menu", options=list(names), format_func=lambda m: names[m], 
                      index=None, placeholder="Choose a menu", key=pick_key)

if picked is not None:
    with st.container(border=True):
        render_menu(get_selected_menu_recipes(conn=conn, menu_id=picked))
    if create_button(name='add_menu_to_event'):
        add_menu_to_event(conn, event_id, picked)
        st.session_state.menu_pick_version = st.session_state.get("menu_pick_version", 0) + 1
        st.rerun()
