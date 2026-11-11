# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.events import get_selected_event
from database.menus import get_event_menus, get_selected_menu_recipes, get_menu_batches
from database.recipes import get_selected_recipe_ingredients
from database.food_and_drink import get_selected_menu_items_for_edit
from styles.page_config import (
     PAGES, 
     setup_page_defaults,
     create_button,
     create_page_header,
     create_no_records_container,
     fill_no_records_container,
     render_list)

# Create the connection to the database
conn = get_connection()

# Set up page
setup_page_defaults()

event_id = st.session_state.get('selected_event_id')

# Calculate number of guests including kids and hearty eaters
selected_event =get_selected_event(conn=conn, event_id=event_id)

guest_count = int(selected_event['num_adults']) + int(selected_event['num_hearty_eaters']) + (int(selected_event['num_kids']) / 2)

# Create empty data structures
shopping_list = []
checked_recipes = []

# Pull menus
event_menus = get_event_menus(conn=conn, event_id=event_id)

menus = [x[0] for x in event_menus]

# Pull recipes
menu_recipes = []
for menu in menus:
    recipes = get_selected_menu_recipes(conn=conn, menu_id=menu)
    for recipe in recipes:
        recipe_batches = get_menu_batches(conn=conn, menu_id=menu)
        recipes = recipes + recipe_batches
    menu_recipes = menu_recipes + recipes

print("menu_recipe check: ", menu_recipes)

unchecked_recipes = [x[0] for x in menu_recipes]

# Recursively check for recipe components and ingredients and nested ingredients to shopping list
def find_nested_components(unchecked, checked, shopping_list, guest_count):
    # Base case
    if unchecked == []:
        return unchecked, checked, shopping_list

    # Build recipe ingredients
    recipe_ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=unchecked[0])

    checked.append(unchecked[0])
    
    for ingredient in recipe_ingredients:

        if ingredient[2] == 'Recipe':
            unchecked.append(ingredient[6])

        elif ingredient[2] == 'Ingredient':
            event_amount = ingredient[3] * guest_count
            shopping_list.append((ingredient[0], event_amount, ingredient[4]))

    del unchecked[0]
    return find_nested_components(unchecked, checked, shopping_list, guest_count)


# Build shopping list of recipe ingredients
unchecked, checked, shopping_list = find_nested_components(unchecked=unchecked_recipes,
                                                           checked=checked_recipes,
                                                           shopping_list=shopping_list,
                                                           guest_count=guest_count)


# Pull additional food and drink items from menu
for menu in menus:
    menu_items = get_selected_menu_items_for_edit(conn=conn, menu_id=menu)

    # Scale with guest count
    for item in menu_items:
        print("item: ", item)
        if item[4] == 1:
            item_amount = item[2] * guest_count
        else:
            item_amount = item[2]
        shopping_list.append((item[0], item_amount, item[3]))

print("guest_count: ", guest_count)
print("recipe_ids checked: ", checked)
print("shopping_list final: ")
for i in shopping_list:
    print(i)


