const express = require("express");
const cors = require("cors"); // can be removed if only CLI (@kumarbros)
const db = require("./db");
const axios = require("axios");

const app = express();

//middleware
app.use(cors());
app.use(express.json());
// app.use(async (req, res, next) => {
//   if (!req.body.access_token) {
//     res.status(401).end();
//     return;
//   }
//   try {
//     await authenticate(req.body.access_token);
//   } catch (error) {
//     res.status(401).end();
//     return;
//   }
//   next();
// });

// HELPER(s)
async function authenticate(token) {
  const r = await axios.get("https://api.github.com/user", {
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${token}`,
    },
  });
  const login = r.data.login;

  const userQuery = await db.query(
    "SELECT * FROM users WHERE login = $1 LIMIT 1;",
    [login]
  );
  if (userQuery.rows.length !== 1) {
    const msg = `User ${login} is not authorized to use inven.`;
    console.log(msg);
    throw new Error(msg);
  }
  return login;
}

function getMostRecentlyAdded(ingredientList) {
  const sortedIngredients = ingredientList.sort((a, b) => {
    const dateComparison =
      new Date(b.purchase_date) - new Date(a.purchase_date);
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
  let sum = 0;
  for (const i of ingredientQuery.rows) {
    sum += i.ingredient_count;
  }
  return sum;
}

//ROUTES

app.get("/ingredientTotal", async (req, res) => {
  const { ingredient } = req.body;
  const count = await getIngredientTotal(ingredient);
  res.json(count);
});

// ADD ingredients and counts to the db
app.post("/addIngredients", async (req, res) => {
  try {
    console.log("add ingredients");
    const { ingredients } = req.body;

    const addIngredient =
      "INSERT INTO ingredients (ingredient_name, ingredient_count, purchase_date) VALUES($1, $2, $3) RETURNING *;";
    for (const ingredient of ingredients) {
      await db.query(addIngredient, [
        ingredient.name,
        ingredient.count,
        ingredient.date,
      ]);
    }

    res.status(200).json("successfully added ingredients");
  } catch (error) {
    console.error(error.message);
  }
});

// REMOVE ingredients and counts from the db
app.put("/removeIngredients", async (req, res) => {
  try {
    console.log("update ingredients");
    let { name, count } = req.body;
    count = parseFloat(count);
    const totalCount = await getIngredientTotal(name);
    let ingredientQuery = await db.query(
      "SELECT * FROM ingredients WHERE ingredient_name = $1;",
      [name]
    );

    if (ingredientQuery.rows.length == 0) {
      res.status(404).json("ingredient not in pantry");
    } else if (count > totalCount) {
      res.status(400).json("attempted to remove too many items from pantry");
    } else {
      while (count > 0) {
        console.log("removed entry");
        ingredientQuery = await db.query(
          "SELECT * FROM ingredients WHERE ingredient_name = $1;",
          [name]
        );
        let latestIngredient = getMostRecentlyAdded(ingredientQuery.rows);
        let currentIngredientCount = latestIngredient.ingredient_count;
        let updatedCount = Math.max(0, currentIngredientCount - count);
        count -= currentIngredientCount;

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
    res.status(200).json("consumed ingredient");
  } catch (error) {
    console.error(error.message);
  }
});

// VIEW the current state of the pantry (counts of ingredients and # of days ago it was bought)
app.get("/pantry", async (req, res) => {
  try {
    console.log("pantry view request");
    const viewPantry = await db.query("SELECT * FROM ingredients;");
    console.log(viewPantry.rows);
    res.json(viewPantry.rows);
  } catch (error) {
    console.error(error.message);
  }
});

// CREATE a new recipe
app.post("/addRecipe", async (req, res) => {
  try {
    const { recipe_name, ingredients } = req.body;

    await deleteRecipe(recipe_name);

    const createRecipe = await db.query(
      "INSERT INTO recipes (recipe_name) VALUES ($1) RETURNING recipe_id;",
      [recipe_name]
    );
    const recipeId = createRecipe.rows[0].recipe_id;

    const addIngredientToRecipe =
      "INSERT INTO recipeIngredients (recipe_id, ingredient_name, ingredient_count, ingredient_quantity_str, optional) VALUES ($1, $2, $3, $4, $5);";
    for (const ingredient of ingredients) {
      await db.query(addIngredientToRecipe, [
        recipeId,
        ingredient.ingredient_name,
        ingredient.ingredient_count || null,
        ingredient.ingredient_quantity_str || null,
        ingredient.optional || false,
      ]);
    }
    res.json("successfully added recipe to pantry");
  } catch (error) {
    console.error(error.message);
  }
});

app.delete("/removeRecipe", async (req, res) => {
  try {
    const { recipe } = req.body;

    let getRecipe = await db.query(
      "SELECT recipe_id FROM recipes WHERE recipe_name = $1;",
      [recipe]
    );
    console.log(getRecipe.rows);
    if (getRecipe.rows.length === 0) {
      return res.status(404).json({ error: "Recipe is not in the db" });
    }

    const recipeId = getRecipe.rows[0].recipe_id;

    // Delete the recipe ingredients from the recipeIngredients table
    await db.query("DELETE FROM recipeIngredients WHERE recipe_id = $1;", [
      recipeId,
    ]);

    // Delete the recipe from the recipes table
    await db.query("DELETE FROM recipes WHERE recipe_id = $1;", [recipeId]);

    res.json("successfully removed recipe");
  } catch (error) {
    console.error(error.message);
  }
});

async function deleteRecipe(recipe) {
  try {
    let getRecipe = await db.query(
      "SELECT recipe_id FROM recipes WHERE recipe_name = $1;",
      [recipe]
    );
    console.log(getRecipe.rows);
    if (getRecipe.rows.length === 0) {
      throw new Error(`recipe ${recipe} not found`);
    }

    const recipeId = getRecipe.rows[0].recipe_id;

    // Delete the recipe ingredients from the recipeIngredients table
    await db.query("DELETE FROM recipeIngredients WHERE recipe_id = $1;", [
      recipeId,
    ]);

    // Delete the recipe from the recipes table
    await db.query("DELETE FROM recipes WHERE recipe_id = $1;", [recipeId]);
  } catch (error) {
    console.error(error.message);
  }
}

// VIEW all available recipes
app.get("/recipes", async (req, res) => {
  try {
    console.log("recipe view request");
    const recipes = await db.query("SELECT recipe_name FROM recipes;");
    res.json(recipes.rows);
    //res.json("Pantry request received")
  } catch (error) {
    console.error(error.message);
  }
});

app.get("/recipeIngredients", async (req, res) => {
  try {
    const { recipe } = req.body;
    let recipeId = await db.query(
      "SELECT recipe_id FROM recipes WHERE recipe_name = $1",
      [recipe]
    );
    recipeId = recipeId.rows[0]["recipe_id"];

    let ingredients = await db.query(
      "SELECT ingredient_name, ingredient_count, ingredient_quantity_str, optional FROM recipeIngredients WHERE recipe_id = $1",
      [recipeId]
    );

    res.json(ingredients.rows);
  } catch (error) {
    console.error(error.message);
  }
});

// USE a recipe (consumes ingredients)
app.put("/useRecipe", async (req, res) => {
  try {
    console.log("using recipe");
    const { recipe } = req.body;
    let recipeId = await db.query(
      "SELECT recipe_id FROM recipes WHERE recipe_name = $1",
      [recipe]
    );
    recipeId = recipeId.rows[0]["recipe_id"];

    let ingredients = await db.query(
      "SELECT ingredient_name, ingredient_count FROM recipeIngredients WHERE recipe_id = $1 AND ingredient_count IS NOT NULL AND optional = FALSE",
      [recipeId]
    );
    let canUseRecipe = true;
    let missingIngredients = [];
    for (const ingredient of ingredients.rows) {
      const avail = await getIngredientTotal(ingredient["ingredient_name"]);
      if (ingredient["ingredient_count"] > avail) {
        canUseRecipe = false;
        missingIngredients.push({
          [ingredient["ingredient_name"]]:
            ingredient["ingredient_count"] - avail,
        });
      }
    }
    if (!canUseRecipe) {
      res.status(400).json({
        message: `cannot use recipe ${recipe}. missing the following ingredients:`,
        missing: missingIngredients,
      });
    } else {
      consumed = [];
      for (const ingredient of ingredients.rows) {
        body = {
          name: ingredient["ingredient_name"],
          count: ingredient["ingredient_count"],
        };
        consumed.push(body);
        axios
          .put("http://localhost:4000/removeIngredients", body)
          .catch((err) => {
            console.error(err.message);
          });
      }
      console.log(consumed);
      res.json({ message: recipe + " consumed.", consumed: consumed });
    }
  } catch (error) {
    console.error(error.message);
  }
});

// GET a shoppinglist of ingredients/counts given a recipe/what's in the pantry

app.listen(4000, () => {
  console.log("db listening on port 4000");
});
