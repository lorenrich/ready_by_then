'''
Prep work to build schedule and shopping list
'''
import math
from collections import defaultdict, Counter
from database.events import get_selected_event
from database.menus import get_event_menus, get_menu_batches
from database.recipes import PREP_LABELS, get_selected_recipe_ingredients, get_selected_recipe
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


def build_schedule(conn, menu_recipes, menus):

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

    # Deduplicate list of recipes, preserving the original checked list
    checked_dict = dict.fromkeys(checked)

    # Set up dictionary of lists for groups
    groups = defaultdict(lambda: defaultdict(list))

    # Loop through recipes and group
    for recipe_id in checked_dict:

        # Get ingredients
        ingredients = get_selected_recipe_ingredients(conn=conn, recipe_id=recipe_id)

        # Group the tuples by prep_timing
        for i in ingredients:
            if i[2] != 'Ingredient':
                continue
            timing = i[5] if i[5] is not None else 1
            groups[recipe_id][timing].append(i)
                      
    # Build labels
    schedule = defaultdict(list)

    for recipe_id, buckets in groups.items():
        name = get_selected_recipe(conn=conn, recipe_id=recipe_id)["recipe_name"]

        if len(buckets) == 1:
            timing = next(iter(buckets))
            schedule[timing].append({"row_key": f"{recipe_id}_{timing}", "label": name})

        else:
            all_rows = [r for rows in groups[recipe_id].values() for r in rows]
            section_total = Counter(r[1] for r in all_rows)

            for timing, rows in buckets.items():
                bucket_count = Counter(r[1] for r in rows)
                parts = []
                for section in bucket_count:
                    if section is not None and bucket_count[section] == section_total[section]:
                        parts.append(section)
                    else:
                        parts.extend(r[0] for r in rows if r[1] == section)
                label = f"{name} ({', '.join(parts)})"
                schedule[timing].append({"row_key": f"{recipe_id}_{timing}", "label": label})

    # Add in menu_items
    for menu in menus:
        menu_items = get_selected_menu_items_for_edit(conn=conn, menu_id=menu)

        for item in menu_items:
            timing = item[5] if item[5] is not None else 1
            schedule[timing].append({"row_key": f"item_{menu}_{item[6]}_{timing}", "label": item[0]})

    rows = []
    for t in sorted(schedule, reverse=True):
        for entry in sorted(schedule[t], key=lambda e: e["label"].lower()):
            rows.append({"When": PREP_LABELS[t], "Task": entry["label"], "row_key": entry["row_key"]})

    return rows, checked

