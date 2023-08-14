CREATE DATABASE inven_app;

CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(127) NOT NULL,
    ingredient_count NUMERIC NOT NULL,
    purchase_date DATE NOT NULL
);

CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(100) NOT NULL
);

CREATE TABLE recipeIngredients (
    recipe_id INT NOT NULL,
    ingredient_name VARCHAR(127) NOT NULL,
    ingredient_count NUMERIC,
    ingredient_quantity_str VARCHAR(127),
    optional BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
    PRIMARY KEY (recipe_id, ingredient_name)
);

CREATE TABLE users (
  login TEXT PRIMARY KEY
);

INSERT INTO users (login) VALUES ('rahulk29');
INSERT INTO users (login) VALUES ('rohanku');
INSERT INTO users (login) VALUES ('oliverye7');
INSERT INTO users (login) VALUES ('oliver-ye7');

