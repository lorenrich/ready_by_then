# Import
import streamlit as st

# Pages
PAGES = {
    'home': st.Page("pages/home.py", title="Home", icon=":material/home:", url_path="home", default=True),
    'events': st.Page("pages/events.py", title="Events", icon=":material/event:", url_path="events"),
    'event_details': st.Page("pages/event_details.py", title="Event Details", url_path="event_details"),
    'copy_event': st.Page("pages/copy_event.py", title="Create Event Copy", url_path="copy_event"),
    'create_event': st.Page("pages/create_event.py", title="Create Event", url_path="create_event"),
    'edit_event': st.Page("pages/edit_event.py", title="Edit Event", url_path="edit_event"),

    'menus': st.Page("pages/menus.py", title='Menus', url_path="menus"),
    'create_menu': st.Page("pages/create_menu.py", title='Create Menu', url_path="create_menu"),

    'recipes': st.Page("pages/recipes.py", title="Recipes", icon=":material/chef_hat:", url_path="recipes"),
    'recipe_details': st.Page("pages/recipe_details.py", title="Recipe Details", url_path="recipe_details"),
    'copy_recipe': st.Page("pages/copy_recipe.py", title="Create Recipe Copy", url_path="copy_recipe"),
    'create_recipe': st.Page("pages/create_recipe.py", title="Create Recipe", url_path="create_recipe"),
    'edit_recipe': st.Page("pages/edit_recipe.py", title="Edit Recipe", url_path="edit_recipe"),

    'ingredients': st.Page("pages/ingredients.py", title="Add Ingredients", url_path="ingredients"),
    "open_full_recipe": st.Page("pages/ingredients.py", title="Add Ingredients", url_path="ingredients"),

    'custom_lists': st.Page(page="pages/custom_lists.py", title="Custom Lists", icon=":material/list_alt:", url_path="custom_lists"),
    'custom_list_details': st.Page(page="pages/custom_list_details.py", title="Custom List Details", url_path="custom_list_details"),
    'copy_custom_list': st.Page(page="pages/copy_custom_list.py", title="Copy Custom List", url_path="copy_custom_list"),
    'create_custom_list': st.Page(page="pages/create_custom_list.py", title="Create Custom List", url_path="create_custom_list"),
    'edit_custom_list': st.Page(page="pages/edit_custom_list.py", title="Edit Custom List", url_path="edit_custom_list"),

    'help': st.Page(page="pages/help.py", title="Help", icon=":material/help:")
}

BUTTONS = {
    # Basic buttons
    'back': dict(label="Back", type="secondary", icon=":material/arrow_back_ios_new:"),
    'cancel': dict(label="Cancel", type="secondary"),
    'confirm_delete': dict(label="Yes, delete", type='primary'),
    'copy': dict(label="Copy", type="secondary"),
    'delete': dict(label="Delete", type="secondary"),
    'edit': dict(label="Edit", type="secondary"),

    # Page buttons
    'custom_lists': dict(label="Custom Lists", type="primary", icon=":material/list_alt:"),
    'create_list': dict(label="Create List", type="primary", icon=':material/add:'),

    'events': dict(label="Events", type="primary", icon=":material/celebration:"),
    'create_event': dict(label="Create new event", type="primary", icon=":material/add:"),

    'recipes': dict(label="Recipes", type="primary", icon=":material/chef_hat:"),
    'create_recipe': dict(label='Create new recipe', type='primary', icon=":material/chef_hat:"),
    'save_ingredients': dict(label='Save ingredients', type='primary', icon=':material/grocery:'),

    'create_menu': dict(label="Create Menu", type="primary", icon=":material/add:"),

    'help': dict(label="Help", type="primary", icon=":material/help:")
}

CIRCULAR_ICONS = {
    "events": 'assets/circular_calendar.png',
    "menus": 'assets/circular_menu.png',
    "recipes": 'assets/circular_recipe.png',
    "lists": 'assets/circular_list.png'
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
    cfg = {**BUTTONS[name], **overrides}
    label = cfg.pop("label")
    cfg.setdefault("key", f"btn_{name}")
    return st.button(label, **cfg)


def create_big_button(key, label, dark_color, light_color, height=250):
    st.html(f"""
    <style>
    .st-key-{key} button {{
        height: {height}px;
        background: linear-gradient(to top, {dark_color} 0%, {light_color} 100%) !important;
        border: none !important;
        border-radius: 10px;
        box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.15s, box-shadow 0.15s;
    }}
    .st-key-{key} button:hover {{
        transform: translateY(-3px);
        box-shadow: 5px 9px 24px rgba(0, 0, 0, 0.22);
    }}
    .st-key-{key} button:focus,
    .st-key-{key} button:active {{
        border: none !important;
        color: white !important;
    }}
    .st-key-{key} button p {{
        color: white;
        font-size: 48px;
        margin: 0;
    }}
    </style>
    """)
    return st.button(label, key=key, width="stretch")


def create_page_header(name, dark_color, light_color):
    '''
    Header bars with color gradient
    '''
    return f"""
    <style>
    .st-key-{name} {{
        background: linear-gradient(to top, {dark_color} 0%, {light_color} 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.15);
    }}
    .st-key-{name} p {{
        color: #2E1A5E;
        font-size: 36px;
        text-align: left;
        margin: 0;
    }}
    </style>
    """


def create_subheader(text):
    st.markdown(f"""<h3 style="text-align: center; font-size: 20px; font-color: #2E1A5E;">{text}</h3>""", unsafe_allow_html=True)


def create_no_records_container(name):
    return f"""
    <style>
    .st-key-{name} {{
        background: #FFFFFF;
        align-items: center;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.15);
    }}
    </style>
    """

def fill_no_records_container(container, icon_name, header_val, caption_val, button_name, page_redirect):
        with container:
            st.image(CIRCULAR_ICONS[icon_name], width=50)

            create_subheader(header_val)
            st.caption(caption_val, text_alignment="center")

            if create_button(name=button_name):
                st.switch_page(PAGES[page_redirect])
