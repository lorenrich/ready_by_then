'''
Prep work to build schedule and shopping list
'''
import math
from collections import defaultdict
from database.events import get_selected_event
from database.menus import get_event_menus, get_menu_batches
from database.recipes import get_selected_recipe_ingredients
from database.food_and_drink import get_selected_menu_items_for_edit


def build_schedule_and_shopping_prep(conn, event_id):
    # Calculate number of guests including kids and hearty eaters
    selected_event = get_selected_event(conn=conn, event_id=event_id)

    guest_count = int(selected_event['num_adults']) + int(selected_event['num_hearty_eaters']) + int(selected_event['num_kids'])

    # Pull event data
    event_menus = get_event_menus(conn=conn, event_id=event_id)

    menus = [x[0] for x in event_menus]

    # Pull recipes and batches
    menu_recipes = []
    for menu_id, name, _status in event_menus:
        for recipe_id, batches in get_menu_batches(conn=conn, menu_id=menu_id):
            menu_recipes.append((recipe_id, batches or 1.0))

    return guest_count, menu_recipes, menus


def build_shopping_list(conn, menu_recipes, guest_count, menus):

    unchecked = [x[0] for x in menu_recipes]
    batch_multiplier = [x[1] for x in menu_recipes]

    shopping_list = []
    checked_recipes = []

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
    unchecked, checked, batch_multiplier, shopping_list = find_nested_components(
        unchecked=unchecked,
        checked=checked_recipes,
        batch_multiplier=batch_multiplier,
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

    # checked = every recipe visited (menu recipes and nested components)
    return final_shopping_list, checked


def build_schedule(conn, menu_recipes):

    unchecked = [x[0] for x in menu_recipes]
    checked = []

    # Recursively check for recipe components and add to unchecked recipes
    def find_nested_components_only(unchecked, checked):
        # Base case
        if unchecked == []:
            return unchecked, checked

        # Build recipe ingredients
        recipe_ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=unchecked[0])

        checked.append(unchecked[0])

        for ingredient in recipe_ingredients:

            if ingredient[2] == 'Recipe':
                unchecked.append(ingredient[6])

        del unchecked[0]
        return find_nested_components_only(unchecked, checked)


    # Build list of recipes
    unchecked, checked = find_nested_components_only(unchecked=unchecked, checked=checked)

    # Deduplicate list of recipes
    checked = dict.fromkeys(checked)

    # Set up dictionary of lists for groups
    groups = defaultdict(list)

    # Loop through recipes and group by timing
    for recipe_id in checked:

        # Get ingredients
        ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=recipe_id)
        print("\nrecipe ingredients: ", ingredients)

        # Group the tuples by prep_timing
        for i in ingredients:
            timing = i[5] if i[5] is not None else 1
            groups[(recipe_id, timing)].append(i)
    print("\ngroups by timing: ", groups)
   
    
    return groups
    


'''
 - Prep Timing Section Logic
elif all ingredients in a recipe section (if section) have the same prep timing, schedule shows recipe name, section, and its ingredients?
    under respective prep timing section

elif all recipe ingredients have the same prep timing, schedule shows recipe name under the respective prep timing section

else group together ingredients by prep timing section and list them in parentheses with the recipe name 
    (e.g. Veggie flatbread (carrots, broccoli, etc.) under Day Before and Veggie flatbread (flatbread) under Day of)


Label. If a bucket covers the whole recipe, show the name only. Otherwise show the name plus a parenthetical, using section or 
component names where the bucket fully contains them and ingredient names only for the leftovers.

Your Veggie flatbread example falls out naturally: one task under Day Before, one under Day Of. I’d also drop 
“section and its ingredients” from case 3. The ingredient list already lives on the recipe page, and a schedule 
is a checklist, so a section name is enough. Show ingredients only when a section is split across buckets.

'''