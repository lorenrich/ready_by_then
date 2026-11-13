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
    'menu_details': st.Page("pages/menu_details.py", title='Menu Details', url_path="menu_details"),
    "copy_menu": st.Page("pages/copy_menu.py", title="Copy Menu", url_path="copy_menu"),
    'create_menu': st.Page("pages/create_menu.py", title='Create Menu', url_path="create_menu"),
    "edit_menu": st.Page("pages/edit_menu.py", title="Edit Menu", url_path="edit_menu"),

    "event_menus": st.Page("pages/event_menus.py", title="Add Event Menus", url_path="event_menus"),
    
    'recipes': st.Page("pages/recipes.py", title="Kitchen", icon=":material/chef_hat:", url_path="recipes"),
    'recipe_details': st.Page("pages/recipe_details.py", title="Recipe Details", url_path="recipe_details"),
    'copy_recipe': st.Page("pages/copy_recipe.py", title="Create Recipe Copy", url_path="copy_recipe"),
    'create_recipe': st.Page("pages/create_recipe.py", title="Create Recipe", url_path="create_recipe"),
    'edit_recipe': st.Page("pages/edit_recipe.py", title="Edit Recipe", url_path="edit_recipe"),

    'ingredients': st.Page("pages/ingredients.py", title="Add Ingredients", url_path="ingredients"),
    "open_full_recipe": st.Page("pages/ingredients.py", title="Add Ingredients", url_path="ingredients"),

    "food_and_drink": st.Page("pages/food_and_drink.py", title="Food & Drink", url_path="food_and_drink"),
    "create_food_and_drink": st.Page("pages/create_food_and_drink.py", title="Create Item", url_path="create_food_and_drink"),
    "edit_food_and_drink": st.Page("pages/edit_food_and_drink.py", title="Edit Food & Drink", url_path="edit_food_and_drink"),

    "shopping_list": st.Page("pages/shopping_list.py", title="Shopping List", url_path='shopping_list'),
    "schedule": st.Page("pages/schedule.py", title='Schedule', url_path='schedule'),

    "help": st.Page('pages/help.py', title='How to Use', icon=':material/help:', url_path='help'),
}


KITCHEN_PAGES = (PAGES['recipes'], PAGES['create_recipe'], PAGES['edit_recipe'],
                 PAGES['recipe_details'], PAGES['copy_recipe'], PAGES['ingredients'],
                 PAGES['food_and_drink'], PAGES['create_food_and_drink'],
                 PAGES['edit_food_and_drink'], PAGES['menus'], PAGES['create_menu'],
                 PAGES['edit_menu'], PAGES['menu_details'], PAGES['copy_menu'])

BUTTONS = {
    # Basic buttons
    'cancel': dict(label="Cancel", type="secondary"),
    'confirm_delete': dict(label="Yes, delete", type='primary'),
    'copy': dict(label="Copy", type="secondary", icon=":material/content_copy:"),
    'delete': dict(label="Delete", type="secondary", icon=":material/delete:"),
    'edit': dict(label="Edit", type="primary", icon=":material/edit:"),
    'shopping_list': dict(label='Get Shopping List', type='secondary', icon=":material/shopping_bag:"),
    'schedule': dict(label='Get Prep Schedule', type='secondary', icon=":material/schedule:"),
    'back_to_details': dict(label='Back to Event Details', type='secondary', icon=':material/arrow_back:'),

    # Page buttons
    'events': dict(label="Events", type="primary", icon=":material/celebration:"),
    'create_event': dict(label="Create new event", type="primary", icon=":material/add:"),

    'food_and_drink': dict(label="Food & Drink", type="primary", icon=":material/grocery:"),
    'food_and_drink_secondary': dict(label="Food & Drink", type="secondary", icon=":material/grocery:"),
    'add_food_and_drink': dict(label="Add item", type="primary", icon=":material/add:"),
    'remove_food_and_drink': dict(label="Remove item", type="primary", icon=":material/remove:"),

    'recipes': dict(label='Recipes', type='primary', icon=":material/chef_hat:"),
    'recipes_secondary': dict(label='Recipes', type='secondary', icon=":material/chef_hat:"),
    'create_recipe': dict(label='Create new recipe', type='primary', icon=":material/add:"),
    'save_ingredients': dict(label='Save ingredients', type='primary', icon=':material/grocery:'),

    'menus': dict(label='Menus', type='primary', icon=':material/menu_book_2:'),
    'menus_secondary': dict(label='Menus', type='secondary', icon=':material/menu_book_2:'),
    'create_menu': dict(label="Create new menu", type="primary", icon=":material/add:"),
    'save_menu': dict(label="Save menu", type='primary', icon=':material/menu_book_2:'),
    'add_recipes_to_menu': dict(label="Add recipes", type="primary", icon=":material/add:"),

    'add_menu_to_event': dict(label="Add menu", type="primary", icon=":material/add:"),
    'add_menus': dict(label="Add menu", type="primary", icon=":material/add:"),
    "remove_menu": dict(label="Remove menu", type="primary", icon=":material/remove:"),

}

CIRCULAR_ICONS = {
    "events": 'assets/circular_calendar.png',
    "menus": 'assets/circular_menu.png',
    "recipes": 'assets/circular_recipe.png',
    "food_and_drink": "assets/circular_food_and_drink.png"
}

BADGES = {
    "Complete":   ("#DDF3E4", "#1E6B3A"),
    "Incomplete": ("#FFDCCB", "#9A3412"),
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
    st.html("""
    <style>
    [class*="st-key-list_card_"] {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 8px 12px;
        box-shadow: 0 2px 8px rgba(40, 20, 90, 0.12);
    }
    [class*="st-key-list_card_"] [data-testid="stMarkdownContainer"] p { color: #2D1B69; margin: 0 !important; line-height: 1.5; }
    
    [class*="st-key-list_card_"] [data-testid="stMarkdownContainer"],
    [class*="st-key-list_card_"] [data-testid="stMarkdownContainer"] p {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    }

    [class*="st-key-listrow_"] { border-radius: 10px; padding: 4px 8px; }
    [class*="st-key-listrow_"]:hover { background: #F0E9FF; }
    [class*="st-key-list_card_"] { color: #2D1B69; }
    [class*="st-key-rowlink_"] button { padding: 0; min-height: 0; }
    [class*="st-key-rowlink_"] button p { font-size: 1rem; line-height: 1.5; }
    [class*="st-key-list_card_"] h3 {
    color: #2D1B69;
    font-size: 2rem;
    padding: 0.25rem 0 0.5rem 0;
    margin: 0;
    }
    </style>
    """)
    st.html(
        """
        <style>
        .st-key-detail_card { background: #FFF; border-radius: 16px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(40, 20, 90, 0.12); }
        </style>
        """
    )
    st.html("""
    <style>
    [class*="st-key-list_card_"], [class*="st-key-info_card_"] {
    background: #FFFFFF; border-radius: 16px; padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(40, 20, 90, 0.12); color: #2D1B69;
    }
    </style>
    """)


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


def badge(text):
    bg, fg = BADGES.get(text, ("#EDE7FF", "#5B3FA6"))
    if not text:
        return ""
    return (f'<span style="background:{bg};color:{fg};padding:2px 10px;'
            f'border-radius:999px;font-size:0.8rem;font-weight:600;">{text}</span>')


def section_heading(text):
    st.subheader(text, anchor=False)


def render_list(rows, columns, id_field, prefix, on_open=None, title=None, empty_message=None, subtext=None):
    widths = [c[2] for c in columns]
    with st.container(key=f"list_card_{prefix}"):
        if title:
            section_heading(title)
        if subtext:
            st.caption(subtext)
        if not rows:
            if empty_message:
                st.caption(empty_message)
            return
        for col, (title, *_) in zip(st.columns(widths), columns):
            col.caption(title)
        for row in rows:
            rid = row[id_field]
            with st.container(key=f"listrow_{prefix}_{rid}"):
                cells = st.columns(widths, vertical_alignment="center")
                for cell, (_, field, _, kind) in zip(cells, columns):
                    if kind == "link":
                        if cell.button(row[field], type="tertiary", key=f"open_{prefix}_{rid}"):
                            on_open(row)
                    elif kind == "badge":
                        cell.markdown(badge(row[field]), unsafe_allow_html=True)
                    elif kind == "integer":
                        cell.markdown(row[field])
                    else:
                        cell.write(row[field])

