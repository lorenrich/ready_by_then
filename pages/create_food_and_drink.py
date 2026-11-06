# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import time
from database.database import get_connection, update_and_default_selectbox
from database.food_and_drink import DEFAULT_ITEM_TYPES, create_item
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header)

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Update values of item_type select box with any submitted user entries
item_types = update_and_default_selectbox(conn=conn,
                                          table_name='food_and_drinks',
                                          col_name='item_type',
                                          default_options=DEFAULT_ITEM_TYPES)

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

# Create item form
with st.form("create_item", clear_on_submit=True):
    st.write("Let's get started!")
    item_name = st.text_input('Name your item (you can include your favorite brands or keep names generic like "dinner rolls")')
    
    item_type = st.selectbox("Select the item type or add a new one",
                             options=item_types,
                             accept_new_options=True)

    st.space("small")
    st.write("Don't worry about amounts just yet.  You can edit those when the item is tagged to a menu or event.")
    
   # Take user to add_ingredients or submit as-is
    col1, col2 = st.columns([1, 5], gap="small")

    with col1:
        add_another = st.form_submit_button("Create another item", type="primary")
    with col2:
        done_adding = st.form_submit_button("I'm finished")

    if add_another or done_adding:
        if not item_name.strip():
            st.error("Please give the item a name.")
            st.stop()

        new_item_id = create_item(conn,
                                  item_name=item_name, 
                                  item_type=item_type)
        if add_another:
            # Display msg that item was saved
            st.toast(f"{item_name} saved successfully!")
            time.sleep(1.0)

            # Refresh to new form
            st.session_state["selected_item_id"] = new_item_id
            st.switch_page(PAGES["create_food_and_drink"])
            
        else:
            st.switch_page(PAGES["food_and_drink"])