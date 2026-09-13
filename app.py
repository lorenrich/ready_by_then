"""
Streamlit home page and navigation
"""
# Import
import streamlit as st
from events import create_event
from database import get_connection

conn = get_connection()

# --- PAGE CONFIG ---
home_page = st.Page("pages/home_page.py", title="Home", icon=":material/home:", default=True)
events_page = st.Page("pages/events_page.py", title="Events", icon=":material/event:")
create_event_page = st.Page("pages/create_event_page.py", title="Create Event Test", url_path="create_event")
recipe_page = st.Page(page="pages/recipes_page.py", title="Recipes", icon=":material/chef_hat:")
custom_lists_page = st.Page(page="pages/custom_lists_page.py", title="Custom Lists", icon=":material/list_alt:")
help_page = st.Page(page="pages/help_page.py", title="Help", icon=":material/help:")

# --- HIDE SPECIFIED PAGES FROM NAVIGATION ---
st.html("""
<style>
    [data-testid="stSidebarNavLink"][href$="create_event"] {
        display: none;
    }
</style>
""")

# --- SITE NAVIGATION ---
pg = st.navigation([
    home_page,
    events_page,
    create_event_page,
    recipe_page,
    custom_lists_page,
    help_page
])

# --- RUN NAVIGATION ---
pg.run()