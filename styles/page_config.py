# Import
import streamlit as st

# Pages
pages = {
    'home': st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
    'events': st.Page("pages/events.py", title="Events", icon=":material/event:"),
    'event_details': st.Page("pages/event_details.py", title="Event Details", url_path="event_details"),
    'create_event': st.Page("pages/create_event.py", title="Create Event", url_path="create_event"),
    'edit_event': st.Page("pages/edit_event.py", title="Edit Event", url_path="edit_event"),

    'recipes': st.Page(page="pages/recipes.py", title="Recipes", icon=":material/chef_hat:"),
    'recipe_details': st.Page(page="pages/recipe_details.py", title="Recipe Details"),
    'create_recipe': st.Page(page="pages/create_recipe.py", title="Create Recipe"),
    'edit_recipe': st.Page(page="pages/edit_recipe.py", title="Edit Recipe"),

    'custom_lists': st.Page(page="pages/custom_lists.py", title="Custom Lists", icon=":material/list_alt:"),
    'custom_list_details': st.Page(page="pages/custom_list_details.py", title="Custom List Details"),
    'create_custom_list': st.Page(page="pages/create_custom_list.py", title="Create Custom List"),
    'edit_custom_list': st.Page(page="pages/edit_custom_list.py", title="Edit Custom List"),

    'help': st.Page(page="pages/help.py", title="Help", icon=":material/help:")
}


def setup_page_defaults():    
    # Custom page and header config shared on all pages
    st.set_page_config(page_title="Ready by Then", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #9d6ef7;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Buttons (note, cannot use form_button here)
buttons = {
    # Basic buttons
    'back': dict(label="Back", type="secondary", icon=":material/arrow_back_ios_new:"),
    'cancel': dict(label="Cancel", type="secondary"),
    'confirm_delete': dict(label="Yes, delete", type='primary'),
    'copy': dict(label="Copy", type="secondary"),
    'delete': dict(label="Delete", type="secondary"),
    'edit': dict(label="Edit", type="secondary"),

    # Page buttons
    'custom_lists': dict(label="Custom Lists", type="primary", icon=":material/list_alt:"),
    'events': dict(label="Events", type="primary", icon=":material/celebration:"),
    'create_event': dict(label="Create new event", type="primary", icon=":material/event:"),
    'recipes': dict(label="Recipes", type="primary", icon=":material/chef_hat:"),
    'help': dict(label="Help", type="primary", icon=":material/help:")
}

def create_button(name, **overrides):
    cfg = {**buttons[name], **overrides}
    label = cfg.pop("label")
    cfg.setdefault("key", f"btn_{name}")
    return st.button(label, **cfg)
