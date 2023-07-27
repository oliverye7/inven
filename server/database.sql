CREATE DATABASE inven_app;

CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(100) NOT NULL,
    ingredient_count NUMERIC(10, 2) NOT NULL,
    purchase_date DATE NOT NULL
);

CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(100) NOT NULL
);

CREATE TABLE recipeIngredients (
    recipe_id INT NOT NULL,
    ingredient_name VARCHAR(100) NOT NULL,
    ingredient_count INT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
    PRIMARY KEY (recipe_id, ingredient_name)
);