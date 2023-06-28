const express = require("express");
const cors = require("cors"); // can be removed if only CLI (@kumarbros)
const db = require("./db");

const app = express();

//middleware
app.use(cors());
app.use(express.json())

//ROUTES

// ADD ingredients and counts to the db
app.post("/addIngredients", async(req, res) => {
    try {
        console.log("add ingredients");
        console.log(req.body);
        const {name, count, date} = req.body;
        const newIngredient = await db.query(
            "INSERT INTO ingredients (ingredient_name, ingredient_count, purchase_date) VALUES($1, $2, $3) RETURNING *;",
            [name, count, date]
        );
        console.log(newIngredient.rows[0])
        res.json("successfully added ingredients")
    } catch (error) {
        console.error(error.message);
    }
})

// REMOVE ingredients and counts from the db

// USE a recipe (consumes ingredients)

// VIEW the current state of the pantry (counts of ingredients and # of days ago it was bought)
app.get("/pantry", async(req, res) => {
    try {
        console.log("pantry view request");
        console.log(req.body);
        res.json("Pantry request received")
    } catch (error) {
        console.error(error.message);
    }
})

// CREATE a new recipe
app.post("/addRecipe", async(req, res) => {
    try {
        const {recipe_name, ingredients} = req.body;

        const createRecipe = await db.query(
            "INSERT INTO recipes (recipe_name) VALUES ($1) RETURNING recipe_id;",
            [recipe_name]
        );
        const recipeId = createRecipe.rows[0].recipe_id;

        const addIngredientToRecipe =  "INSERT INTO recipeIngredients (recipe_id, ingredient_name, ingredient_count) VALUES ($1, $2, $3);"
        for (const ingredient of ingredients) {
            await db.query(addIngredientToRecipe, [recipeId, ingredient.ingredient_name, ingredient.ingredient_count]);
        }
        res.json("successfully added ingredients")
    } catch (error) {
        console.error(error.message);
    }
})

// GET a shoppinglist of ingredients/counts given a recipe/what's in the pantry

app.listen(4000, () => {
    console.log("db listening on port 4000");
});