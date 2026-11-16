 # Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import html
import math
import pandas as pd
from datetime import date
from database.database import get_connection
from database.events import get_selected_event
from database.menus import get_event_menus, get_menu_batches
from database.recipes import get_selected_recipe_ingredients, get_selected_recipe, get_component_ids
from database.food_and_drink import get_selected_menu_items_for_edit
from database.schedule_and_shopping import build_schedule_and_shopping_prep, build_schedule
from styles.page_config import (
    PAGES,
    setup_page_defaults,
    create_page_header,
    create_button,
    render_list,
    badge,
    section_heading)


def export_schedule(schedule_rows):
    df = pd.DataFrame(schedule_rows)[["When", "Task"]]
    return df.to_csv(index=False).encode("utf-8")


# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

event_id = st.session_state.get('selected_event_id')
today = date.today()

# Call functions to build shopping list and schedule
selected_event = get_selected_event(conn=conn, event_id=event_id)
guest_count, menu_recipes, menus = build_schedule_and_shopping_prep(conn, event_id)
schedule, checked = build_schedule(conn=conn, menu_recipes=menu_recipes, menus=menus)

# Structure schedule for page render
schedule_rows, last = [], None

for r in schedule:
    schedule_rows.append({
        "When": r["When"] if r["When"] != last else "",
        "Task": r["Task"],
        "row_key": r["row_key"],
    })
    last = r["When"]

schedule_columns = [("When", "When", 2, "string"),
                    ("Task", "Task", 5, "string")]


# Render to page
# Page header
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/schedule: Events')

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
            label='Export Schedule',
            data=export_schedule(schedule_rows=schedule_rows),
            file_name=f'{selected_event['event_name']} Prep Schedule {today}.csv',
            mime="text/csv",
            icon=":material/download:"
            )

# Alert the user of assumptions
with st.expander(label='About scheduling'):
    st.write(
        "If there are recipes with no data entered for preheat, prep, or cook times, you will see them below and have a chance to make edits to them."\
            "If you proceed with no data in those fields, Ready by Then will assume that preheat and cook time are zero and allot 10 minutes per recipe "\
                "for prep time."
    )

# If event has recipes missing times, alert the user and guide them to fix it
missing_info = []

for recipe_id in checked:
    df = get_selected_recipe(conn=conn, recipe_id=recipe_id)
    issues = []

    if df['recipe_cooking_vessel'] != '' and df['recipe_cook_time'] == 0:
        issues.append('cook time')
    if df['recipe_preheat_temp'] > 0 and df['recipe_preheat_time'] == 0:
        issues.append("preheat time")
    if df['recipe_prep_time'] == 0:
        issues.append("prep time")

    if issues:
        missing_info.append({
            "Name": df['recipe_name'],
            "Status": f"Missing {', '.join(issues)}",
            "recipe_id": recipe_id,
            "row_key": recipe_id
        })


if missing_info:
    columns = [
            ("Name", "Name", 5, "link"),
            ("Status", "Status", 2, "string")
            ]

    def open_entry(row):
        st.session_state["selected_recipe_id"] = int(row["recipe_id"])
        st.switch_page(PAGES['edit_recipe'])

    render_list(rows=missing_info, 
                columns=columns, 
                id_field="row_key",
                on_open=open_entry, 
                prefix='missing_times',
                title="Wait, some recipes are missing times",
                subtext="Click to fix. Until then, the schedule assumes 10 minutes of prep and no preheat or cook time for each recipe.")


# Render schedule to page
render_list(rows=schedule_rows, 
            columns=schedule_columns, 
            id_field="row_key",
            prefix="schedule", 
            title="Prep Schedule",
            empty_message="There are no menu items assigned to this event yet.")

 