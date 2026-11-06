# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import sqlite3
from database.database import get_connection, update_and_default_selectbox
from database.food_and_drink import DEFAULT_ITEM_TYPES, get_selected_item, edit_item, delete_item, get_item_usage
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header)


@st.dialog("Delete recipe?")
def confirm_delete(item_id):
    st.write("This permanently deletes the item. This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if create_button(name="confirm_delete"):
            try:
                deleted = delete_item(conn, item_id=item_id)
            except sqlite3.IntegrityError:
                menus, events = get_item_usage(conn, item_id)
                if menus:
                    st.error("This item is used in: " + ", ".join(name for _, name in menus) + ". Remove it there first.")
                    st.stop()
                if events:
                    st.error("This item is used in: " + ", ".join(name for _, name in events) + ". Remove it there first.")
            if deleted:
                st.switch_page(PAGES["food_and_drink"])
            else:
                st.error("Nothing was deleted. The item may already be gone.")
    with col2:
        if create_button(name="cancel"):
            st.rerun()


# Connect to database
conn = get_connection()

# Identify selected event and filter dataframe
item_id = st.session_state.get("selected_item_id")

# Get data
selected_item_df = get_selected_item(conn=conn, item_id=item_id)

# Guard against empty dataframe
if selected_item_df.empty:
    st.warning("That item couldn't be found.  It may have been deleted.")
    st.page_link(PAGES['food_and_drink'], label="<- Back to Food & Drink")
    st.stop()

# Update values of item_type select box with any submitted user entries
item_types = update_and_default_selectbox(conn=conn,
                                          table_name='food_and_drinks',
                                          col_name='item_type',
                                          default_options=DEFAULT_ITEM_TYPES)

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

# Allow user to edit item
with st.form("create_item", clear_on_submit=True):
    st.write("Edit your item")

    # Identify the default type
    default_item_type = selected_item_df['item_type']

    item_name = st.text_input('Name your item (you can include your favorite brands or keep names generic like "dinner rolls")',
                              value=selected_item_df['item_name'])
    
    item_type = st.selectbox("Select the item type or add a new one",
                             index=item_types.index(default_item_type) if default_item_type in item_types else None,
                             options=item_types,
                             accept_new_options=True)

    st.space("small")
    st.write("Don't worry about amounts just yet.  You can edit those when the item is tagged to a menu or event.")

    col4, col5 = st.columns([1, 3])
    with col4:
        # Save or delete item
        if st.form_submit_button("Save changes"):
            edit_item(conn=conn,
                    item_name=item_name,
                    item_type=item_type,
                    item_id=item_id)

            st.switch_page(PAGES['food_and_drink'])

    with col5:
        if st.form_submit_button("Delete item"):
            confirm_delete(item_id=int(selected_item_df['item_id']))
