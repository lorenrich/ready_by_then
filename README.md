# Ready by Then
Ready by Then is a Python-based Streamlit application for party planning.  Create events, menus, custom recipes, and food and drink items.  Tag your family and friends' favorites to menus and events and get a shopping list and prep schedule scaled to your guest count and catered to when things should be prepared.


## Features
Users can build events, menus, and recipes. Ready by Then will build a grocery list and prep schedule for the event.  Events, menus, and recipes can be repeated and modified as needed.

## How it Works
![Screenshot of completed event page](./assets/screenshot_event_page.png)

The shopping list will group items with like units across recipes (e.g. 2 cloves garlic, 3 cloves garlic) and scale with the number of batches assigned on the menu.  Additional food and drink items which don't require a recipe can be either a set amount or scaled with the guest count.

![Screenshot of shopping list](./assets/screenshot_shopping_list.png)

The schedule will summarize recipe components, sections, and ingredients and organize by "Day Before", "Day Of", and "At Serving" prep based on the user's selections.

![Screenshot of prep schedule](./assets/screenshot_prep_schedule.png)

Shopping lists and schedules are built when viewed and are not stored.  They can be exported to CSV.

Events, menus, recipes, and food and drink items can be repeated and adjusted to make the same party next year even easier.

```mermaid
erDiagram
    events ||--o{ event_menus : "plans"
    menus ||--o{ event_menus : "used in"
    menus ||--o{ menu_recipes : "contains"
    recipes ||--o{ menu_recipes : "appears in"
    menus ||--o{ menu_items : "contains"
    food_and_drinks ||--o{ menu_items : "appears in"
    recipes ||--o{ recipe_ingredients : "has"
    recipes ||--o{ recipe_sections : "has"
    recipe_sections |o--o{ recipe_ingredients : "groups"
    recipes ||--o{ recipe_components : "is parent of"
    recipes ||--o{ recipe_components : "is used as component in"

    events {
        int event_id PK
        string event_name
        string event_date
        string event_time
        string event_serving_time
        int num_adults
        int num_kids
        string event_notes
        string event_status
    }
    menus {
        int menu_id PK
        string menu_name
        string menu_notes
        string menu_status
    }
    event_menus {
        int event_id PK, FK
        int menu_id PK, FK
    }
    recipes {
        int recipe_id PK
        string recipe_name
        string recipe_type
        int recipe_yield
        string recipe_cooking_vessel
        int recipe_preheat_temp
        string recipe_preheat_unit
        int recipe_preheat_time
        int recipe_cook_time
        string recipe_source
        string recipe_notes
        string recipe_status
        int recipe_prep_time
    }
    menu_recipes {
        int menu_id PK, FK
        int recipe_id PK, FK
        string course
        float batches
    }
    recipe_sections {
        int section_id PK
        int recipe_id FK
        string section_name
        int prep_timing
    }
    recipe_ingredients {
        int ingredient_id PK
        int recipe_id FK
        int section_id FK
        string ingredient_name
        float amount
        string unit
        int prep_timing
    }
    recipe_components {
        int parent_recipe_id PK, FK
        int component_recipe_id PK, FK
        int section_id FK
        float amount
        string unit
        int prep_timing
    }
    food_and_drinks {
        int item_id PK
        string item_name
        string item_type
    }
    menu_items {
        int menu_id PK, FK
        int item_id PK, FK
        string course
        float amount
        string unit
        boolean scales_with_guests
        int prep_timing
    }
```


### Known Limitations
In the shopping list, items will only be combined for like units (i.e. 2 cloves garlic in one recipe won't combine with 1 tsp garlic in another).  Units will only convert for US Customary measures including tsp, tbsp, and cups.

The prep schedule does not provide summary of estimated time to complete prep or suggestion of when to start cooking on "Day Of" prep and does not scale with number of batches.


## Technical
Requires (see ```requirements.txt``` for exact versions):
- Git
- Python 3.12+
- Streamlit
- Pandas


## Installation & Setup
### 1. Clone the repo and create a virtual environment
#### On macOS/Linux/WSL
```
git clone https://github.com/lorenrich/ready_by_then
cd ready_by_then
python3 -m venv .venv
source .venv/bin/activate
```

#### On Windows
```
git clone https://github.com/lorenrich/ready_by_then
cd ready_by_then
python -m venv .venv
.venv\Scripts\activate
```
If PowerShell blocks activation, run ```Set-ExecutionPolicy -Scope Process RemoteSigned``` and try again.

### 2. Install requirements
Make sure the virtual environment is activate (your prompt starts with .venv), then install the packages listed in ```requirements.txt```
```
pip install -r requirements.txt
```

### 3. Seed and launch the app
An example database has been provided. To run the app using the example database, from the project root run:

```
python seed.py
streamlit run app.py
```

To run the app with an empty database, run:
```
streamlit run app.py
```

## Usage
App opens at http://localhost:8501.  Your data is saved in ```ready_by_then.db``` in the project directory.

If you wish to reset the database or if ```seed.py``` is run twice, you will be prompted to reset the database.
**--reset replaces the existing database and erases any events, menus, and recipes you have added**

To reset the database and remove all sample data, run:
```
python seed.py --reset
streamlit run app.py
```

If you don't wish to reset the database, proceed with:
```
streamlit run app.py
```

To stop the app run ```Ctrl``` + ```C```


## Roadmap
This app is v1.0 submitted for my Boot.dev capstone project which was scaled down considerably to meet a personal deadline.  Below are features tagged for future enhancements.

- 🚧 **Event Specs** - Scaling to accommodate events with "hearty eaters" and notifications for dietary restrictions.

- 🚧 **Upgraded Schedule** - Prep schedule based on event start/meal serving time to estimate when the host should start cooking and how long prep is estimated to take.

- 🚧 **Recipe Scraping and Uploading** - Users can submit URLs for their favorite recipes online or upload a photo of one and the app will translate the recipe data into the form for the user to review

- 🚧 **Custom Lists** - Build custom to-do lists for cleaning, decorations, and gifts linked to your prep schedule where you need it.

- 🚧 **Shareable Menu Template** -  When your event is potluck-style, invite your guests to sign up to bring something while ensuring you have a well-rounded menu.

- 🚧**Guest Lists** - Keep track of who's coming.

- 🚧 **Web Hosting** - An app always accessible which allows user accounts and securely stores your data in the cloud.

- 🚧 **Smart Alerts** - Notify the user when there isn't enough food on the menu for the number of guests, when the menu doesn't include drinks, or make suggestions based on the most frequently tagged recipes and items from the user.

- 🚧 **Chatbot Assistant** - Not sure what to do next?  Ask for help.

