'''
Create and alter recipe data
'''
def create_recipe(conn,
                  name,
                  recipe_type, 
                  recipe_yield,
                  recipe_cooking_vessel,
                  recipe_preheat_temp,
                  recipe_preheat_unit,
                  recipe_preheat_time,
                  recipe_cook_time,
                  recipe_source,
                  notes):
    conn.execute(
        "INSERT INTO recipes (name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source, notes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, recipe_type, recipe_yield, recipe_cooking_vessel, recipe_preheat_temp, recipe_preheat_unit, recipe_preheat_time, recipe_cook_time, recipe_source,notes)
    )
    conn.commit()

    