PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_time TEXT,
        event_serving_time TEXT,
        num_adults INTEGER NOT NULL,
        num_kids INTEGER NOT NULL,
        event_notes TEXT,
        event_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
INSERT INTO events VALUES(1,'A Taco Thanksgiving 🌮','2026-11-27','13:00','13:30',6,4,'A day to be thankful for family and tacos!','Incomplete');
CREATE TABLE menus (
        menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
        menu_name TEXT NOT NULL,
        menu_notes TEXT,
        menu_status TEXT NOT NULL DEFAULT 'Incomplete'
        );
INSERT INTO menus VALUES(1,'Taco menu','Review toppings - do we have everything?','Incomplete');
CREATE TABLE menu_recipes (
        menu_id INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        course TEXT,
        batches REAL DEFAULT 1.0,
        PRIMARY KEY (menu_id, recipe_id),
        FOREIGN KEY (menu_id) REFERENCES menus(menu_id) ON DELETE CASCADE,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE RESTRICT
        );
INSERT INTO menu_recipes VALUES(1,1,'Main',1.0);
CREATE TABLE event_menus (
        event_id INTEGER NOT NULL,
        menu_id INTEGER NOT NULL,
        PRIMARY KEY (event_id, menu_id),
        FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
        FOREIGN KEY (menu_id) REFERENCES menus(menu_id) ON DELETE CASCADE
        );
INSERT INTO event_menus VALUES(1,1);
CREATE TABLE recipes (
        recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        recipe_type TEXT,
        recipe_yield INTEGER,
        recipe_cooking_vessel TEXT,
        recipe_preheat_temp INTEGER,
        recipe_preheat_unit TEXT,
        recipe_preheat_time INTEGER,
        recipe_cook_time INTEGER,
        recipe_source TEXT,
        recipe_notes TEXT,
        recipe_status TEXT NOT NULL DEFAULT 'Incomplete',
        recipe_prep_time INTEGER
        );
INSERT INTO recipes VALUES(1,'Taco meat','Entree',8,'Cooktop',0,NULL,0,10,'Natasha''s Kitchen','','Incomplete',20);
INSERT INTO recipes VALUES(2,'Taco seasoning',NULL,3,NULL,0,NULL,NULL,NULL,'Natasha''s Kitchen','Yields 3 tbsp','Complete',NULL);
CREATE TABLE recipe_ingredients (
        ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        section_id INTEGER,
        ingredient_name TEXT NOT NULL,
        amount REAL,
        unit TEXT,
        prep_timing INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        FOREIGN KEY (section_id) REFERENCES recipe_sections(section_id) 
            ON DELETE SET NULL
        );
INSERT INTO recipe_ingredients VALUES(1,1,1,'Ground beef 93/7',1.0,'lb',1);
INSERT INTO recipe_ingredients VALUES(2,1,1,'Yellow onion',1.0,NULL,1);
INSERT INTO recipe_ingredients VALUES(3,1,1,'Garlic',2.0,'cloves',1);
INSERT INTO recipe_ingredients VALUES(4,1,1,'Tomato paste',1.0,'Tbsp',1);
INSERT INTO recipe_ingredients VALUES(5,1,1,'Taco shells',1.0,'pkg',1);
INSERT INTO recipe_ingredients VALUES(6,1,2,'Lettuce',2.0,'cup(s)',1);
INSERT INTO recipe_ingredients VALUES(7,1,2,'Tomato',2.0,'cup(s)',1);
INSERT INTO recipe_ingredients VALUES(8,1,2,'Shredded cheese',1.0,'pkg',0);
INSERT INTO recipe_ingredients VALUES(9,1,3,'Taco sauce',1.0,NULL,0);
INSERT INTO recipe_ingredients VALUES(10,1,3,'Cholula',1.0,NULL,0);
INSERT INTO recipe_ingredients VALUES(11,1,2,'Avocado',2.0,NULL,0);
INSERT INTO recipe_ingredients VALUES(12,1,2,'Lime',2.0,NULL,0);
INSERT INTO recipe_ingredients VALUES(13,2,4,'Chili powder',1.0,'Tbsp',2);
INSERT INTO recipe_ingredients VALUES(14,2,4,'Ground cumin',2.0,'tsp',2);
INSERT INTO recipe_ingredients VALUES(15,2,4,'Smoked or regular paprika',1.0,'tsp',2);
INSERT INTO recipe_ingredients VALUES(16,2,4,'Salt',0.75,'tsp',2);
INSERT INTO recipe_ingredients VALUES(17,2,4,'Black pepper',0.5,'tsp',2);
INSERT INTO recipe_ingredients VALUES(18,2,4,'Garlic powder',0.5,'tsp',2);
INSERT INTO recipe_ingredients VALUES(19,2,4,'Onion powder',0.5,'tsp',2);
INSERT INTO recipe_ingredients VALUES(20,2,4,'Dried oregano',0.5,'tsp',2);
INSERT INTO recipe_ingredients VALUES(21,2,4,'Red pepper flakes',0.100000000000000005,'tsp',2);
CREATE TABLE recipe_components (
        parent_recipe_id INTEGER NOT NULL,
        component_recipe_id INTEGER NOT NULL,
        section_id INTEGER,
        amount REAL,
        unit TEXT,
        prep_timing INTEGER,
        PRIMARY KEY (parent_recipe_id, component_recipe_id),
        CHECK (parent_recipe_id != component_recipe_id),
        FOREIGN KEY (parent_recipe_id) REFERENCES recipes(recipe_id) 
            ON DELETE CASCADE,
        FOREIGN KEY (component_recipe_id) REFERENCES recipes(recipe_id) 
            ON DELETE RESTRICT,
        FOREIGN KEY (section_id) REFERENCES recipe_sections(section_id) 
            ON DELETE SET NULL
        );
INSERT INTO recipe_components VALUES(1,2,1,3.0,'Tbsp',2);
CREATE TABLE recipe_sections (
        section_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        section_name TEXT NOT NULL,
        prep_timing INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
        UNIQUE (recipe_id, section_name)
        );
INSERT INTO recipe_sections VALUES(1,1,'Main ingredients',NULL);
INSERT INTO recipe_sections VALUES(2,1,'Garnish',NULL);
INSERT INTO recipe_sections VALUES(3,1,'Sauce',NULL);
INSERT INTO recipe_sections VALUES(4,2,'Main ingredients',NULL);
CREATE TABLE food_and_drinks (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
        item_type TEXT
        );
INSERT INTO food_and_drinks VALUES(1,'Water','Drink');
INSERT INTO food_and_drinks VALUES(2,'Diet Pepsi','Drink');
INSERT INTO food_and_drinks VALUES(3,'Red Wine','Drink');
CREATE TABLE menu_items (
        menu_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        course TEXT,
        amount REAL,
        unit TEXT,
        scales_with_guests BOOLEAN DEFAULT 0,
        prep_timing INTEGER,
        PRIMARY KEY (menu_id, item_id),
        FOREIGN KEY (menu_id) REFERENCES menus(menu_id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES food_and_drinks(item_id) 
            ON DELETE RESTRICT
        );
INSERT INTO menu_items VALUES(1,1,'Drink',1.0,NULL,1,2);
INSERT INTO menu_items VALUES(1,2,'Drink',5.0,NULL,0,2);
INSERT INTO menu_items VALUES(1,3,'Drink',2.0,NULL,0,0);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('events',1);
INSERT INTO sqlite_sequence VALUES('menus',1);
INSERT INTO sqlite_sequence VALUES('food_and_drinks',3);
INSERT INTO sqlite_sequence VALUES('recipes',2);
INSERT INTO sqlite_sequence VALUES('recipe_sections',4);
INSERT INTO sqlite_sequence VALUES('recipe_ingredients',21);
COMMIT;
