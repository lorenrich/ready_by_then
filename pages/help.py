# Import
import sys
import os

# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection
from database.food_and_drink import get_items_for_display
from styles.page_config import (PAGES, 
                                setup_page_defaults, 
                                create_button, 
                                create_page_header,
                                create_no_records_container,
                                fill_no_records_container,
                                render_list,
                                section_heading)

HOW_IT_WORKS = [
     (":material/menu_book:", 'Recipes', "Add custom recipes with all of those subtle tweaks your family loves and their favorite food and drinks"),
     (":material/chef_hat:", "Menus", "Tag recipes, food, and drinks to menus to use for an event or save for the future"),
     (":material/celebration:", "Events", "Tag menus to your event so your family's favorite dishes and drinks are never forgotten")
]

WHAT_YOU_GET = [
     (":material/shopping_bag:", 'Shopping list', "Generate an exportable shopping list with everything you need for your event"),
     (":material/schedule:", "Prep schedule", "Get a schedule of food preparation"),
     (":material/content_copy:", "Reuse", "Repeat any event and modify it for next time")
]

QUESTIONS = {
     'How are amounts scaled?':
     'Recipe ingredients are scaled by the number of batches called for when the recipe is added to a menu.  Food and drink items "\
        "can be a fixed amount or set to be scaled with the number of guests attending the event.',

     'What if a recipe is incomplete?':
     'Before you build a shopping list, the app will alert you of anything tagged to your event marked as Incomplete so you can make changes.',

     'What if I need to make changes but my item is marked complete?':
     'Complete and Incomplete statuses are only there to remind you where something is.  You can change them and make edits to an item at any time.',

     'Where is my data stored?':
     'The app writes your data to disk so data never leaves your device.'
}

ROADMAP = [
     ("🚧 Custom Lists", "Build custom to-do lists for cleaning, decorations, and gifts linked to your prep schedule where you need it"),
     ("🚧 Shareable Menu Template", "When your event is a potluck, invite your guests to sign up to bring something"),
     ("🚧 Guest Lists", "Keep track of who's coming"),
     ("🚧 Web Hosting", "An app always accessible which allows user accounts and securely stores your data in the cloud"),
     ("🚧 Chatbot Assistant", "Not sure what to do next?  Ask a robot."),
]

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

# Page header
st.html(create_page_header('help_page_header', '#7EC234', '#BCE292'))

header_container = st.container(key='help_page_header')

with header_container:
     icon_calendar = ''
     st.write(':material/help: Help')

with st.container(key="info_card_1"):
     section_heading("What is Ready by Then?")

     st.write(
          "Plan the party.  Ready by Then handles the shopping list and the schedule."
     )

# How it works
st.space("medium")
section_heading("How it works")

for col, (icon, how_title, text) in zip(st.columns(3), HOW_IT_WORKS):
    with col:
         with st.container(key=f"info_card_{how_title}"):
              st.markdown(f"### {icon} {how_title}")
              st.caption(text)


# What you get
st.space("medium")
section_heading("What you get")

for col, (icon, what_title, text) in zip(st.columns(3), WHAT_YOU_GET):
    with col:
         with st.container(key=f"info_card_{what_title}"):
              st.markdown(f"### {icon} {what_title}")
              st.caption(text)


# Questions
st.space("medium")
with st.container(key='info_card_8'):
    section_heading("Questions")

    for key, value in QUESTIONS.items():
        with st.expander(
            label=key
        ):
            st.write(value)


    
# Roadmap
st.space("medium")
with st.container(key="info_card_9"):
     st.markdown(f"### {":material/pin_road:"} Roadmap")
     st.caption("Features for a future release")

     for (roadmap_title, text) in ROADMAP:
        st.write(roadmap_title)
        st.caption(f'<span style="margin-left: 20px;">{text}</span>', unsafe_allow_html=True)

