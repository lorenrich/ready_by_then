# Walk up path to root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Continue import statements after locating root
import streamlit as st
from database.database import get_connection, update_and_default_selectbox, DEFAULT_STATUSES
from database.menus import get_selected_menu, get_selected_menu_recipes, copy_menu
from pages.menu_details import menu_id as copied_menu_id
from styles.page_config import setup_page_defaults, PAGES

# Connect to database
conn = get_connection()

# Set up page
setup_page_defaults()

