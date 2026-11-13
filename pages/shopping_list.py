# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import html
import pandas as pd
from datetime import date
from database.database import get_connection
from database.events import get_selected_event
from database.recipes import get_selected_recipe
from database.schedule_and_shopping import build_schedule_and_shopping_prep, build_shopping_list
from styles.page_config import (
    PAGES,
    setup_page_defaults,
    create_page_header,
    create_button,
    render_list,
    badge)

def export_shopping_list():
    df = pd.DataFrame(data=final_shopping_list, columns=['Item', 'Amount'])
    return df.to_csv().encode("utf-8")

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

event_id = st.session_state.get('selected_event_id')
today = date.today()

# Call functions to build shopping list
selected_event = get_selected_event(conn=conn, event_id=event_id)
guest_count, menu_recipes, menus = build_schedule_and_shopping_prep(conn, event_id)
final_shopping_list, checked = build_shopping_list(conn, menu_recipes, guest_count, menus)


# Render data to the page
# Page header
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/shopping_bag: Events')

title_col, action_col = st.columns([5, 3], vertical_alignment='center')
with title_col:
    title_col.markdown(
        f"<h2 style='margin:0'>{html.escape(selected_event['event_name'])} {badge(selected_event['event_status'])}</h2>", 
        unsafe_allow_html=True,
        )

with action_col:
    button_container = st.container(horizontal=True)
    with button_container:
        if create_button('back_to_details'):
            st.switch_page(PAGES['event_details'])

        st.download_button(
            label='Export Shopping List',
            data=export_shopping_list(),
            file_name=f'{selected_event['event_name']} Shopping List {today}.csv',
            mime="text/csv",
            icon=":material/download:"
            )

# If event has recipes or nested recipes which are incomplete, alert the user and guide them to fix it
incomplete = {}

for recipe_id in dict.fromkeys(checked):
    recipe = get_selected_recipe(conn=conn, recipe_id=recipe_id)
    if recipe is not None and recipe["recipe_status"] == "Incomplete":
        incomplete[recipe_id] = recipe["recipe_name"]


if incomplete:
    rows = [{"Name": name, "Status": "Incomplete", "id": rid, "row_key": rid}
            for rid, name in incomplete.items()]

    columns = [
            ("Name", "Name", 5, "link"),
            ("Status", "Status", 2, "badge")
            ]
    
    def open_entry(row):
        st.session_state["selected_item_id"] = int(row["recipe_id"])
        st.switch_page(PAGES['edit_recipe'])

    render_list(rows=rows, 
                columns=columns, 
                id_field="row_key",
                on_open=open_entry, 
                prefix='incomplete_recipe',
                title="Wait, you have incomplete recipes",
                subtext="Click below to review. Some recipes listed may be nested within other recipes such as a dressing within a salad.")


# Render shopping list
rows = [{"Item": name.title(), "Amount": quantity, "row_key": i}
        for i, (name, quantity) in enumerate(final_shopping_list)]

columns = [
        ("Item", "Item", 1, "string"),
        ("Amount", "Amount", 2, "string")
        ]

render_list(rows=rows, 
            columns=columns, 
            id_field="row_key",
            prefix='shopping',
            title='Shopping List', 
            empty_message="There are no menu items assigned to this event yet.")


