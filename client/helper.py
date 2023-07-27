import requests
from datetime import datetime
import toml

url = "http://localhost:4000/"


def inven_add_ingredient(args):
    route = 'addIngredients'
    args = ' '.join(args.ingredient)
    ingredients = args.split(", ")
    date = str(datetime.today().date())

    data = {"ingredients": []}
    for i in ingredients:
        count, name = i.split(" ")
        ingredient_data = {
            "name": name,
            "count": count,
            "date": date,
        }
        data["ingredients"].append(ingredient_data)
    try:
        res = requests.post(url + route, json=data)
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_use_ingredient(args):
    args = [args.quantity, args.ingredient]
    route = 'removeIngredients'
    data = {
        "name": args[1],
        "count": args[0]
    }
    try:
        res = requests.put(url + route, json=data)
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_see_aggregate_pantry():
    route = 'pantry'
    pantry = {}
    try:
        res = requests.get(url + route)
        if res.status_code == 200:
            print("AGGREGATE PANTRY CONTENTS:")
            for i in res.json():
                name = i['ingredient_name']
                count = i['ingredient_count']
                if name in pantry:
                    pantry[name] += count
                else:
                    pantry[name] = count
            for i in pantry:
                print(i + ", " + str(pantry[i]) + " units.")
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_see_pantry():
    route = 'pantry'
    try:
        res = requests.get(url + route)
        if res.status_code == 200:
            print("PANTRY CONTENTS")
            for i in res.json():
                ingredient_str = i['ingredient_name'] + \
                    ", " + str(i['ingredient_count']) + " units."
                purchase_date_str = "purchase date: " + \
                    i['purchase_date'][0:10]
                print(f"{ingredient_str.ljust(30)} {purchase_date_str}")
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_add_recipe(args):
    route = "recipes"
    try:
        res = requests.get(url + route)
        if res.status_code == 200:
            for recipe in res.json():
                if (recipe['recipe_name'] == args.recipe):
                    print(
                        "ERR: Recipe already exists in the database. Perhaps you want to try rerunning with 'update' instead.")
                    return
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    route = "addRecipe"
    path = "./recipes/" + args.recipe + ".toml"
    with open(path, "r") as file:
        toml_data = toml.load(file)

    recipe = {
        "recipe_name": args.recipe,
        "ingredients": []
    }

    for i in toml_data['ingredients']:
        if (type(toml_data['ingredients'][i]) == int):
            ingredient_data = {
                "ingredient_name": i,
                "ingredient_count": toml_data['ingredients'][i],
            }
            recipe["ingredients"].append(ingredient_data)

    try:
        res = requests.post(url + route, json=recipe)
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_use_recipe(args):
    route = 'recipes'
    isRecipeKnown = False
    try:
        res = requests.get(url + route)
        if res.status_code == 200:
            for recipe in res.json():
                if (args.recipe == recipe['recipe_name']):
                    isRecipeKnown = True
                    break
            if (not isRecipeKnown):
                print(f"ERR. Inven does not contain recipe: {args.recipe}")
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    route = 'useRecipe'
    try:
        res = requests.put(url + route, json={"recipe": args.recipe})
        if res.status_code == 200:
            print(res.json()['message'])
            print("CONSUMED:")
            for i in res.json()['consumed']:
                print(i)
        else:
            print(res.json()["message"])
            print(res.json()["missing"])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_update_recipe(args):
    inven_remove_recipe(args)
    inven_add_recipe(args)
    print(args.recipe + " has been updated ")


def inven_remove_recipe(args):
    route = "removeRecipe"
    try:
        res = requests.delete(url + route, json={"recipe": args.recipe})
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_shopping_list(args):
    recipes = ' '.join(args.shoppingList).split(", ")
    buy = {}
    for r in recipes:
        try:
            route = "recipeIngredients"
            res = requests.get(url + route, json={"recipe": r})
            if res.status_code == 200:
                if (res.json()):
                    for i in res.json():
                        route = "ingredientTotal"
                        ingredient_count = requests.get(
                            url + route, json={"ingredient": i['ingredient_name']})
                        name = i['ingredient_name']
                        count = max(0, i['ingredient_count'] -
                                    ingredient_count.json())
                        if (count != 0):
                            if name in buy:
                                buy[name] += count
                            else:
                                buy[name] = count
            else:
                print("ERR " + str(res.status_code) + ": " + res.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    print(buy)
