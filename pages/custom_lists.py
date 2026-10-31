# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.lists import get_lists_for_display
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                create_no_records_container,
                                fill_no_records_container)

# Connect to database
conn = get_connection()

# Read in dataframe
df = get_lists_for_display(conn=conn)

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('lists_page_header', '#7EC234', '#BCE292'))

header_container = st.container(key='lists_page_header')

with header_container:
     st.write(':material/list_alt: Lists')

if create_button(name='back'):
    st.switch_page(PAGES['custom_lists'])

# No menus page
if df.empty:

    st.html(create_no_records_container('no_lists'))
    blank_container = st.container(height=250, key='no_lists', horizontal_alignment='center')

    fill_no_records_container(container=blank_container,
                              icon_name='lists',
                              header_val='Build your first to-do list',
                              caption_val='Organize decorations, cleaning, and party prep.',
                              button_name='create_list',
                              page_redirect='create_list')

# List recorded recipes    
else:
    # Buttons
    col1, col2 = st.columns([1, 8], gap="small")
    with col1:
        if create_button(name='back'):
            st.switch_page(PAGES['home'])
    with col2:
        if create_button(name='create_list'):
                st.switch_page(PAGES['create_list'])

    # Data table
    menu_table = st.dataframe(
         df, 
         on_select="rerun",
         selection_mode="single-row",
         hide_index=True, 
         width="stretch")
    
    selected = menu_table.selection.rows
    if selected:
        st.session_state["selected_list_id"] = int(df.iloc[selected[0]]["List ID"])
        st.switch_page(PAGES['list_details'])
