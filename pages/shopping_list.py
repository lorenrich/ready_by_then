# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
import html
import math
from database.database import get_connection
from database.events import get_selected_event
from database.menus import get_event_menus, get_menu_batches
from database.recipes import get_selected_recipe_ingredients
from database.food_and_drink import get_selected_menu_items_for_edit
from styles.page_config import (
     PAGES, 
     setup_page_defaults,
     create_button,
     create_page_header,
     create_no_records_container,
     fill_no_records_container,
     render_list,
     badge)

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

event_id = st.session_state.get('selected_event_id')

# Calculate number of guests including kids and hearty eaters
selected_event = get_selected_event(conn=conn, event_id=event_id)

guest_count = int(selected_event['num_adults']) + int(selected_event['num_hearty_eaters']) + int(selected_event['num_kids'])

# Create empty data structures
shopping_list = []
checked_recipes = []

# Pull data
event_menus = get_event_menus(conn=conn, event_id=event_id)

menus = [x[0] for x in event_menus]

# Pull recipes and batches
menu_recipes = []
for menu_id, name, _status in event_menus:
    for recipe_id, batches in get_menu_batches(conn=conn, menu_id=menu_id):
        menu_recipes.append((recipe_id, batches or 1.0))

unchecked_recipes = [x[0] for x in menu_recipes]
batches = [x[1] for x in menu_recipes]

# Recursively check for recipe components and ingredients and nested ingredients to shopping list
def find_nested_components(unchecked, checked, batch_multiplier, shopping_list):
    # Base case
    if unchecked == []:
        return unchecked, checked, batch_multiplier, shopping_list

    # Build recipe ingredients
    recipe_ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=unchecked[0])

    checked.append(unchecked[0])
    
    for ingredient in recipe_ingredients:

        if ingredient[2] == 'Recipe':
            unchecked.append(ingredient[6])
            batch_multiplier.append(batch_multiplier[0])

        elif ingredient[2] == 'Ingredient':
            event_amount = ingredient[3] * batch_multiplier[0]
            shopping_list.append((ingredient[0], event_amount, ingredient[4]))

    del unchecked[0]
    del batch_multiplier[0]
    return find_nested_components(unchecked, checked, batch_multiplier, shopping_list)


# Build shopping list of recipe ingredients
unchecked, checked, batches, shopping_list = find_nested_components(unchecked=unchecked_recipes,
                                                           checked=checked_recipes,
                                                           batch_multiplier=batches,
                                                           shopping_list=shopping_list)


# Pull additional food and drink items from menu
for menu in menus:
    menu_items = get_selected_menu_items_for_edit(conn=conn, menu_id=menu)

    # Scale with guest count
    for item in menu_items:
        if item[4] == 1:
            item_amount = item[2] * guest_count
        else:
            item_amount = item[2]
        shopping_list.append((item[0], item_amount, item[3]))


# Convert shopping list to mutable list
editable_shopping_list = [list(t) for t in shopping_list]

# Clean up list
for item in editable_shopping_list:
    if item[2] is not None:
        item[2] = item[2].strip().lower()
    item[0] = item[0].strip().lower()
    

# Normalize ingredient amounts by converting US customary units to teaspoons
TO_TSP = {"cup(s)": 48, "tbsp": 3, "tsp": 1}

totals = {}
no_amount = set()

for name, amount, unit in editable_shopping_list:
    key_name = name.strip().lower()
    if amount is None:
        no_amount.add(key_name)
        continue
    factor = TO_TSP.get(unit or "")
    if factor:
        key = (key_name, "tsp")
        amount = amount * factor
    else:
        key = (key_name, unit)
    totals[key] = totals.get(key, 0) + amount


# Convert back to more human-friendly units
def round_to(value, step):
    return math.floor(value / step + 0.5) * step

def tsp_to_display(total_tsp):
    if total_tsp >= 12:
        cups = round_to(total_tsp / 48, 0.125)
        return f"{cups:g} {'cup' if cups <= 1 else 'cups'}"
    if total_tsp >= 3:
        tbsp = round_to(total_tsp / 3, 0.5)
        return f"{tbsp:g} Tbsp"
    tsp = max(round_to(total_tsp, 0.25), 0.25)
    return f"{tsp:g} tsp"

final_shopping_list = []
for (name, unit), amount in totals.items():
    if unit == 'tsp':
        quantity = tsp_to_display(amount)
    else:
        quantity = f"{amount:g} {unit or ''}".strip()

    final_shopping_list.append([name, quantity])

# Alphabetize the shopping list
final_shopping_list.sort()

# Render data to the page
# Page header
st.html(create_page_header('events_page_header', '#FE936A', '#FFAD94'))

header_container = st.container(key='events_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/shopping_bag: Shopping List')

title_col, action_col = st.columns([5, 3], vertical_alignment='center')
with title_col:
    title_col.markdown(
        f"<h2 style='margin:0'>{html.escape(selected_event['event_name'])} {badge(selected_event['event_status'])}</h2>", 
        unsafe_allow_html=True,
        )

# Render shopping list
rows = [{"Item": name.title(), "Amount": quantity, "row_key": i}
        for i, (name, quantity) in enumerate(final_shopping_list)]

columns = [
        ("Item", "Item", 1, "string"),
        ("Amount", "Amount", 2, "string")
        ]

def open_entry(row):
    pass

render_list(rows=rows, 
            columns=columns, 
            id_field="row_key",
            on_open=open_entry, 
            prefix='shopping',
            title='Shopping List', 
            empty_message="There are no menu items assigned to this event yet.")

