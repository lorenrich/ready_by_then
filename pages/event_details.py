# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from datetime import datetime
import html
from database.database import get_connection
from database.events import get_selected_event, delete_event
from database.menus import COURSES, get_selected_menu_recipes, get_event_menus
from database.food_and_drink import get_selected_menu_items
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                badge,
                                render_list,
                                section_heading,
                                create_no_records_container,
                                fill_no_records_container)

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
selected_event_menus = get_event_menus(conn=conn, event_id=event_id) if event_id is not None else None

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

title_col, action_col = st.columns([5, 3], vertical_alignment='center')
with title_col:
    title_col.markdown(
        f"<h2 style='margin:0'>{html.escape(selected_event_df['event_name'])} {badge(selected_event_df['event_status'])}</h2>", 
        unsafe_allow_html=True,
        )

with action_col:
    button_container = st.container(horizontal=True, horizontal_alignment='right')
    with button_container:
        if create_button(name='edit'):
            st.switch_page(PAGES['edit_event'])

        if create_button(name='copy'):
            st.switch_page(PAGES['copy_event'])

        if create_button(name='delete'):
            confirm_delete(event_id=int(selected_event_df['event_id']))

        if create_button(name='shopping_list'):
            st.switch_page(PAGES['shopping_list'])

st.space("small")

# Event Details
details_container = st.container(horizontal=True, border=True, key='detail_card')
with details_container:
    

    col1, col2 = st.columns(2)
    with col1:
        info_col1, info_col2 = st.columns([1, 3], gap="small")
        with info_col1:
            st.markdown("**Date:**", text_alignment="right")
            st.markdown("**Time:**", text_alignment="right")
            st.markdown("**Guests:**", text_alignment="right")

        with info_col2:
            st.write(f'{month} {day}, {year}')
            st.text(event_time)
            st.write(f"{selected_event_df['num_adults']} adults{kids_amt}")


# Write menu
if not selected_event_menus:
    st.html(create_no_records_container('no_menus'))
    no_menus_container = st.container(key='no_menus', height=250, horizontal_alignment='center')

    fill_no_records_container(container=no_menus_container,
                              icon_name='menus',
                              header_val='No Menus Added',
                              caption_val='Start tagging menus to your event',
                              button_name='add_menus',
                              page_redirect=PAGES['event_menus'])

else:
    for menu_id, menu_name, menu_status in selected_event_menus:
        recipes = get_selected_menu_recipes(conn=conn, menu_id=menu_id)
        items = get_selected_menu_items(conn=conn, menu_id=menu_id)

        entries = []
        for recipe_id, name, status, course in recipes:
            entries.append({"kind": "recipe", "id": recipe_id, "name": name,
                            "status": status, "course": course})
        for item_id, name, course in items:
            entries.append({"kind": "item", "id": item_id, "name": name,
                            "status": "", "course": course})

        def course_rank(course):
            return COURSES.index(course) if course in COURSES else len(COURSES)

        entries.sort(key=lambda e: (course_rank(e["course"]), e["name"].lower()))

        rows, last = [], None
        for e in entries:
            label = e["course"] or "Unassigned"
            rows.append({
                "Course": label if label != last else "",
                "Name": e["name"],
                "Status": e["status"],
                "kind": e["kind"],
                "id": e["id"],
                "row_key": f"{e['kind']}-{e['id']}",
            })
            last = label

        columns = [
                ("Course", "Course", 2, "string"),
                ("Name", "Name", 5, "link"),
                ("Status", "Status", 2, "badge")
                ]
        
        def open_entry(row):
            if row["kind"] == "recipe":
                st.session_state["selected_recipe_id"] = int(row["id"])
                st.switch_page(PAGES['recipe_details'])
            else:
                st.session_state["selected_item_id"] = int(row["id"])
                st.switch_page(PAGES['edit_food_and_drink'])

        render_list(rows=rows, columns=columns, id_field="row_key",
                    on_open=open_entry, prefix=f"menu_{menu_id}",
                    title=menu_name, empty_message="Nothing on this menu yet.")


# Write menu notes
if selected_event_df['event_notes']:
    notes_container = st.container(horizontal=True, border=True, key='detail_card')
    with notes_container:
        st.write(selected_event_df['event_notes'])
