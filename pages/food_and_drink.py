# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.food_and_drink import get_items_for_display
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                create_no_records_container,
                                fill_no_records_container)

# Connect to database
conn = get_connection()

# Read in dataframe
df = get_items_for_display(conn=conn)

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('kitchen_page_header', '#45A5ED', '#8FC9F4'))

header_container = st.container(key='kitchen_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/chef_hat: Kitchen')

# The default section/page for the kitchen is recipes with buttons to other sections
col1, col2, col3 = st.columns([1, 3, 3], gap="small")

with col1:
    if create_button(name='recipes_secondary'):
         st.switch_page(PAGES['recipes'])

with col2:
    if create_button(name='food_and_drink'):
         st.switch_page(PAGES['food_and_drink'])

with col3:
    if create_button(name='menus_secondary'):
         st.switch_page(PAGES['menus'])

# No recipes
if df.empty:

    st.html(create_no_records_container('no_items'))
    blank_container = st.container(height=250, key='no_items', horizontal_alignment='center')

    fill_no_records_container(container=blank_container,
                            icon_name='recipes',
                            header_val='Create your first food or drink item',
                            caption_val="Log dinner rolls, a bottle of wine, and your family's favorite sodas all in one place",
                            button_name='add_food_and_drink',
                            page_redirect='create_food_and_drink')

# List recorded items    
else:
    # Buttons
    col4, col5 = st.columns([1, 8], gap="small")
    with col4:
        if create_button(name='add_food_and_drink'):
            st.switch_page(PAGES['create_food_and_drink'])

    # Data table
    item_table = st.dataframe(
             df, 
             on_select="rerun",
             selection_mode="single-row",
             hide_index=True, 
             width="stretch")
    
    selected = item_table.selection.rows
    if selected:
        st.session_state["selected_item_id"] = int(df.iloc[selected[0]]["Item ID"])
        st.switch_page(PAGES['create_food_and_drink'])