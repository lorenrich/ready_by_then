# Import
import sqlite3
from pathlib import pathlib
import streamlit as st

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Set variables
conn = sqlite3.connect("ready_by_then.db")

# Load the external CSS
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)


def main():
    pass


if __name__ == "__main__":
    main()
