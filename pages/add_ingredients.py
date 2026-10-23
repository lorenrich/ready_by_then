# Import
import sys 
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.recipes import get_selected_recipe, DEFAULT_RECIPE_SECTIONS, DEFAULT_INGREDIENT_NAMES, DEFAULT_UNITS, PREP_OPTIONS, INGREDIENT_TYPE
from styles.page_config import setup_page_defaults, pages, buttons, create_button

# Connect to database
conn = get_connection()

# Identify selected recipe and filter dataframe
recipe_id = st.session_state.get("selected_recipe_id")

# Create dataframe
selected_recipe_df = get_selected_recipe(conn=conn, recipe_id=recipe_id) if recipe_id is not None else None

# Guard against empty dataframe else filter it to the selected recipe
if selected_recipe_df.empty:
    st.warning("That recipe couldn't be found.  It may have been deleted.")
    st.page_link(pages['recipes'], label="<- Back to Recipes")
    st.stop()

# Set up pages
setup_page_defaults()

# Title
st.title("Add Ingredients")
st.write(" ")

# Ingredient entry (not an st.form intentionally)
with st.expander("Instructions"):
    st.write("Enter your ingredients and their amounts.  If an item isn't in the dropdown, type to enter a new option.")
    st.write('Recipes sometimes include other recipes.  When this happens, set the ingredient type to "Recipe".  For example, if'\
            'Chicken Soup contains "Homemade Broth" as a recipe within the recipe, Ready by Then will log "Homemade Broth" as a recipe for '\
            "you to complete later.")
    st.write("Prep Timing allows you to decide when it can be prepared.  For example, the main ingredients might be able to be prepped a day in "\
            "advance but garnishes are best left to prepare at meal time.  You can assign a prep time to a specific ingredient or an entire section.")
    st.write("You can come back and edit a recipe's ingredients at any time, even if it's marked complete.  We'll remind you when you have incomplete recipes.")

st.space("small")
st.write(f"**Recipe: {selected_recipe_df['recipe_name']}**")

if "rows" not in st.session_state:
    st.session_state.rows = [0]
    st.session_state.next_row_id = 1

for rid in st.session_state.rows:
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1.25, 1, 1.5, 1.25, 0.6])

    c1.selectbox("Section", 
                 options=DEFAULT_RECIPE_SECTIONS, 
                 index=None, 
                 accept_new_options=True,
                 key=f"section_{rid}", 
                 label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c2.selectbox("Ingredient", 
                 options=DEFAULT_INGREDIENT_NAMES, 
                 index=None, 
                 accept_new_options=True, 
                 key=f"name_{rid}",
                 label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")

    c3.selectbox("Type",
                 options=INGREDIENT_TYPE,
                 accept_new_options=False,
                 key=f"type_{rid}",
                 label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c4.number_input("Amount", 
                    min_value=0.0, 
                    value=0.0, 
                    key=f"amount_{rid}",
                    label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c5.selectbox("Unit", 
                 options=DEFAULT_UNITS, 
                 index=None, 
                 accept_new_options=True, 
                 key=f"unit_{rid}",
                 label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")
    
    c6.selectbox("Prep timing", 
                 list(PREP_OPTIONS), 
                 index=None, 
                 key=f"prep_{rid}",
                 label_visibility="visible" if rid == st.session_state.rows[0] else "collapsed")

    if c7.button("", icon=":material/delete:", key=f"del_{rid}"):
        st.session_state.rows.remove(rid)
        st.rerun()

if st.button("Add ingredient", icon=":material/add:"):
    st.session_state.rows.append(st.session_state.next_row_id)
    st.session_state.next_row_id += 1
    st.rerun()

# Save and write to table



    # st.selectbox("Ready to mark this recipe as complete?")
    # Submit button - sends update to recipes table and ingredients to ingredients table
    # Take user to recipe_details page to see full content

    # Need edit_ingredients page
    