const express = require("express");
const cors = require("cors"); // can be removed if only CLI (@kumarbros)
const db = require("./db");

const app = express();

//middleware
app.use(cors());
app.use(express.json())

// HELPER(s)
function getMostRecentlyAdded(ingredientList) {
    const sortedIngredients = ingredientList.sort((a, b) => {
      const dateComparison = new Date(b.purchase_date) - new Date(a.purchase_date);
      if (dateComparison === 0) {
        return b.ingredient_id - a.ingredient_id;
      }
      return dateComparison;
    });
  
    return sortedIngredients[0];
}

async function getIngredientTotal(ingredient) {
    const ingredientQuery = await db.query(
        "SELECT * FROM ingredients WHERE ingredient_name = $1;",
        [ingredient]
    );
    console.log(ingredientQuery.rows)
    let sum = 0;
    for (const i of ingredientQuery.rows) {
        sum += i.ingredient_count;
    }
    return sum;
}

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
        let {name, count} = req.body;
        const totalCount = await getIngredientTotal(name);
        let ingredientQuery = await db.query(
            "SELECT * FROM ingredients WHERE ingredient_name = $1;",
            [name]
        );

        if (ingredientQuery.rows.length == 0) {
            res.status(404).json("ingredient not in pantry")
        } else if (count > totalCount) {
            res.status(400).json("attempted to remove too many items from pantry")
        } else {
            while (count > 0) {
                console.log("removed entry")
                ingredientQuery = await db.query(
                    "SELECT * FROM ingredients WHERE ingredient_name = $1;",
                    [name]
                );
                let latestIngredient = getMostRecentlyAdded(ingredientQuery.rows)
                let currentIngredientCount = latestIngredient.ingredient_count;
                let updatedCount = Math.max(0, currentIngredientCount - count);
                count -= currentIngredientCount

                if (updatedCount === 0) {
                    await db.query(
                      "DELETE FROM ingredients WHERE ingredient_name = $1 AND ingredient_id = $2;",
                      [name, latestIngredient.ingredient_id]
                    );
                } else {
                    await db.query(
                      "UPDATE ingredients SET ingredient_count = $1 WHERE ingredient_name = $2 AND ingredient_id = $3;",
                      [updatedCount, name, latestIngredient.ingredient_id]
                    );
                }
            }
        }
        res.status(200).json("consumed ingredient")
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