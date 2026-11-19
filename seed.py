'''
Script to seed example database with event, recipes, and menus.  See README
for instructions.
'''
# Import
import sqlite3
import os
import sys

# Identify directory path
DB_PATH = "ready_by_then.db"

# If path exists, prompt user to either reset it if they want
if os.path.exists(DB_PATH):
    if "--reset" not in sys.argv:
        print("A database already exists. Re-run with --reset to replace it.")
        sys.exit(1)
    os.remove(DB_PATH)

# Seed the database
conn = sqlite3.connect(DB_PATH)
with open("seed.sql") as f:
    conn.executescript(f.read())
conn.close()
print("Sample data loaded.")
print("You may now launch the application.  See README for instructions.")
