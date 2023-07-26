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
        const {ingredients} = req.body;

        const addIngredient = "INSERT INTO ingredients (ingredient_name, ingredient_count, purchase_date) VALUES($1, $2, $3) RETURNING *;";
        for (const ingredient of ingredients) {
            await db.query(addIngredient, [ingredient.name, ingredient.count, ingredient.date]);
        }
        const allRows = await db.query("SELECT * FROM ingredients;");
        console.log(allRows.rows);
        
        res.json("successfully added ingredients")
    } catch (error) {
        console.error(error.message);
    }
})

// REMOVE ingredients and counts from the db
app.put("/removeIngredients", async(req, res) => {
    try {
        console.log("update ingredients");
        console.log(req.body);
        const {name, count, date} = req.body;
        const ingredientQuery = await db.query(
            "SELECT ingredient_id, ingredient_name, purchase_date FROM ingredients WHERE ingredient_name = $1;",
            [name]
        );
        console.log(ingredientQuery.rows);
        const currentIngredientCount = ingredientQuery.rows[0].ingredient_count;
        const updatedCount = Math.max(0, currentIngredientCount - count);
        
        const updateQuery = await db.query(
            "UPDATE ingredients SET ingredient_count = $1 WHERE ingredient_name = $2;",
            [updatedCount, name]
        );

        res.json("successfully removed ingredients")
    } catch (error) {
        console.error(error.message);
    }
})

// USE a recipe (consumes ingredients)

// VIEW the current state of the pantry (counts of ingredients and # of days ago it was bought)
app.get("/pantry", async(req, res) => {
    try {
        console.log("pantry view request");
        console.log(req.body);
        const viewPantry = await db.query(
            "SELECT * FROM ingredients;"
        );
        console.log(viewPantry.rows)
        res.json(viewPantry.rows)
        //res.json("Pantry request received")
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