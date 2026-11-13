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

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

event_id = st.session_state.get('selected_event_id')
today = date.today()

# Call functions to build shopping list
selected_event = get_selected_event(conn=conn, event_id=event_id)
guest_count, menu_recipes, menus = build_schedule_and_shopping_prep(conn, event_id)


build_schedule(conn=conn, menu_recipes=menu_recipes)














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

# Alert the user of assumptions
with st.expander(label='About scheduling'):
    st.write(
        "If there are recipes with no data entered for preheat, prep, or cook times, you will see them below and have a chance to make edits to them."\
            "If you proceed with no data in those fields, Ready by Then will assume that preheat and cook time are zero and allot 10 minutes per recipe "\
                "for prep time."
    )

# If event has recipes missing times, alert the user and guide them to fix it
missing_times = {}

'''
for recipe in recipes, if recipe_cooking_vessel != "" and recipe_cook_time is 0, flag as missing cook time
for recipe in recipes, if recipe_preheat_temp > 0 and recipe_preheat_time == 0, flag as missing preheat time
for recipe in recipes, if recipe_prep_time == 0 and recipe_id not in recipe_component_ids, flag as missing prep time
'''


if missing_times:
    rows = [{"Name": name, "Status": "Incomplete", "id": rid, "row_key": rid}
            for rid, name in missing_times.items()]

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


'''
 - On the page
Alert the user of incomplete recipes in their menu and recipes which do not contain a value for cook or preheat time and
provide a list for them to click on to edit items (similar to shopping list page).  Alert them of assumptions made about
blank entries for preheat, prep, and cook times.

Use unchecked, checked list similar to shopping list logic (I can share how this was structured)




 - Time Calculation Logic 
TABLE CHANGE - I need a field for prep time for each recipe (e.g. a soup takes 15 minutes of prep, 20 minutes to boil (what I would enter into preheat), and 20 minutes to cook.)
This should really only apply to the recipes table since we only think about prep times associated with a whole recipe, not ingredients or sections.

Assume that all things with a cook time can be cooked simultaneously.  The logic should take the max cook time of everything in that prep section
    and use it as the allotted cook time.  Repeat this logic for preheat time.  If no preheat or cook time was entered, the app will assume these as zero.

Assume all things with prep time cannot be done simultaneously and add the prep times together.  If no prep time was entered, the app will assume 10 minutes
    for full recipes and five minutes per food/drink item.

DESIGN DILEMMA - In recipes like veggie flatbread, the recipe prep time is 20 minutes and part of the main ingredients section can be prepped the day 
before (veggies) but part of them are to be prepped the day of (flatbread and recipe components).  The app shouldn't allow twenty minutes each day of the prep schedule.
  It also isn't clear when the cook time should be applied as it's only tagged to the recipe as a whole.  If we consider something like Reuben sandwiches where I make 
my own bread, prep time including proof time is three hours.  That three hours should all be banked towards the day before prep when the bread is made, not the day of, 
and then day-of assembly comes with its own separate prep time.

Personally, I always need to know when I should start cooking on the day of the event and have to calculate it out.  Maybe the result is a table of what's left to 
prep the day of and we then ask the user to allot times for each or they can leave it as-is.  Then we aren't making incorrect assumptions about how long prep will 
take.  We only make assumptions on time when an entire recipe happens in the same prep_timing section but allow the user to overwrite that if they choose.  I like this, but
will need to build a way to log their entries.  Then, if they come back later and have adjusted the menu, what they had before is still there and what's newly added
is on the schedule with an option for them to include a prep time.



Will need
Events
Event date and start time (one field, event_date)

event_menus
menu_id
menu_recipes (function?)

Recipes
recipe_id
recipe_cooking_vessel
recipe_preheat_temp
recipe_preheat_unit
recipe_preheat_time
recipe_cook_time
recipe_status

recipe_ingredients
ingredient_id
section_id
ingredient_name
prep_timing

recipe_components
component_recipe_id
section_id
prep_timing

recipe_sections
section_id
section_name
prep_timing

menu_items
item_id
prep_timing

'''