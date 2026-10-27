# Import
import streamlit as st

# Pages
pages = {
    'home': st.Page("pages/home.py", title="Home", icon=":material/home:", url_path="home", default=True),
    'events': st.Page("pages/events.py", title="Events", icon=":material/event:", url_path="events"),
    'event_details': st.Page("pages/event_details.py", title="Event Details", url_path="event_details"),
    'copy_event': st.Page("pages/copy_event.py", title="Create Event Copy", url_path="copy_event"),
    'create_event': st.Page("pages/create_event.py", title="Create Event", url_path="create_event"),
    'edit_event': st.Page("pages/edit_event.py", title="Edit Event", url_path="edit_event"),

    'recipes': st.Page("pages/recipes.py", title="Recipes", icon=":material/chef_hat:", url_path="recipes"),
    'recipe_details': st.Page("pages/recipe_details.py", title="Recipe Details", url_path="recipe_details"),
    'copy_recipe': st.Page("pages/copy_recipe.py", title="Create Recipe Copy", url_path="copy_recipe"),
    'create_recipe': st.Page("pages/create_recipe.py", title="Create Recipe", url_path="create_recipe"),
    'edit_recipe': st.Page("pages/edit_recipe.py", title="Edit Recipe", url_path="edit_recipe"),

    'add_ingredients': st.Page("pages/add_ingredients.py", title="Add Ingredients", url_path="add_ingredients"),
    'edit_ingredients': st.Page("pages/edit_ingredients.py", title="Edit Ingredients", url_path="edit_ingredients"),

    'custom_lists': st.Page(page="pages/custom_lists.py", title="Custom Lists", icon=":material/list_alt:", url_path="custom_lists"),
    'custom_list_details': st.Page(page="pages/custom_list_details.py", title="Custom List Details", url_path="custom_list_details"),
    'copy_custom_list': st.Page(page="pages/copy_custom_list.py", title="Copy Custom List", url_path="copy_custom_list"),
    'create_custom_list': st.Page(page="pages/create_custom_list.py", title="Create Custom List", url_path="create_custom_list"),
    'edit_custom_list': st.Page(page="pages/edit_custom_list.py", title="Edit Custom List", url_path="edit_custom_list"),

    'help': st.Page(page="pages/help.py", title="Help", icon=":material/help:")
}

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
    'create_recipe': dict(label='Create new recipe', type='primary', icon=":material/chef_hat:"),
    'save_ingredients': dict(label='Save ingredients', type='primary', icon=':material/grocery:'),

    'help': dict(label="Help", type="primary", icon=":material/help:")
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


def create_button(name, **overrides):
    cfg = {**buttons[name], **overrides}
    label = cfg.pop("label")
    cfg.setdefault("key", f"btn_{name}")
    return st.button(label, **cfg)


def create_page_header(name, dark_color, light_color):
    return f"""
    <style>
    .st-key-{name} {{
        background: linear-gradient(to top, {dark_color} 0%, {light_color} 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.15);
    }}
    .st-key-{name} p {{
        color: white;
        font-size: 36px;
        text-align: left;
        margin: 0;
    }}
    </style>
    """

