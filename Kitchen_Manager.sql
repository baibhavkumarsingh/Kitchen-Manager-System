-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS pantry_chef_db;
USE pantry_chef_db;

-- 2. Create the Table for Ingredients (The Dictionary)
-- We use AUTO_INCREMENT so you don't have to manually invent IDs.
CREATE TABLE Ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 3. Create the Table for Recipes (The Menu)
CREATE TABLE Recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instructions TEXT
);

-- 4. Create the Junction Table (The Map)
-- This links Recipes to Ingredients.
CREATE TABLE Recipe_Ingredients (
    recipe_id INT,
    ingredient_id INT,
    quantity VARCHAR(50), -- e.g. "200g", "2 pcs"
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- 5. Create Your Pantry Table (Your Fridge)
CREATE TABLE My_Pantry (
    ingredient_id INT PRIMARY KEY,
    quantity_available VARCHAR(50),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- =============================================
-- SEED DATA (Let's put some food in the system)
-- =============================================

-- A. Insert Ingredients
INSERT INTO Ingredients (name) VALUES 
('Egg'), ('Bread'), ('Milk'), ('Tomato'), 
('Cheese'), ('Pasta'), ('Salt'), ('Butter');

-- B. Insert Recipes
INSERT INTO Recipes (name, instructions) VALUES 
('Scrambled Eggs', 'Whisk eggs with milk and salt. Fry in butter.'),
('Grilled Cheese', 'Place cheese between bread. Fry in butter.'),
('Pasta', 'Boil pasta. Add cheese and tomato.');

-- C. Link them (The Logic)
-- Note: You might need to check IDs if you change the order, but usually they start at 1.

-- Scrambled Eggs (Recipe 1) needs: Egg (1), Milk (3), Salt (7), Butter (8)
INSERT INTO Recipe_Ingredients (recipe_id, ingredient_id, quantity) VALUES 
(1, 1, '2'), (1, 3, '50ml'), (1, 7, 'pinch'), (1, 8, '10g');

-- Grilled Cheese (Recipe 2) needs: Bread (2), Cheese (5), Butter (8)
INSERT INTO Recipe_Ingredients (recipe_id, ingredient_id, quantity) VALUES 
(2, 2, '2 slices'), (2, 5, '1 slice'), (2, 8, '10g');

-- Pasta (Recipe 3) needs: Pasta (6), Cheese (5), Tomato (4)
INSERT INTO Recipe_Ingredients (recipe_id, ingredient_id, quantity) VALUES 
(3, 6, '100g'), (3, 5, '50g'), (3, 4, '1');

select * from my_pantry;

select * from ingredients;