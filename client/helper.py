import requests
from datetime import datetime
import toml
from client import auth

# url = "https://inven.fly.dev/"
url = "http://localhost:4000/" #(for local testing)

def inven_add_ingredient(args):
    route = 'addIngredients'
    args = ' '.join(args.ingredient)
    ingredients = args.split(", ")
    date = str(datetime.today().date())

    data = {"ingredients": [], "access_token": auth.get_token() }
    for i in ingredients:
        count, name = i.split(" ")
        ingredient_data = {
            "name": name,
            "count": float(count),
            "date": date,
        }
        data["ingredients"].append(ingredient_data)
    try:
        res = requests.post(url + route, json=data)
        res.raise_for_status()
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
        "count": args[0],
        "access_token": auth.get_token(),
    }
    try:
        res = requests.put(url + route, json=data)
        res.raise_for_status()
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
        res = requests.get(url + route, json={"access_token": auth.get_token()})
        res.raise_for_status()
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
        res = requests.get(url + route, json={"access_token": auth.get_token()})
        res.raise_for_status()
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
        res = requests.get(url + route, json={"access_token": auth.get_token()})
        res.raise_for_status()
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
    with open(args.recipe, "r") as file:
        toml_data = toml.load(file)

    name = toml_data["name"]
    recipe = {
        "recipe_name": name,
        "ingredients": [],
        "access_token": auth.get_token(),
    }

    for i in toml_data['ingredients']:
        ingredient = toml_data['ingredients'][i]
        if (type(ingredient) == int or type(ingredient) == float):
            ingredient_data = {
                "ingredient_name": i,
                "ingredient_count": ingredient,
            }
        elif type(ingredient) == str:
            ingredient_data = {
                "ingredient_name": i,
                "ingredient_quantity_str": ingredient,
            }
        else:
            quantity = ingredient["quantity"]
            optional = ingredient.get("optional", False)
            if type(quantity) == int or type(quantity) == float:
                quantity_dict = {"ingredient_count": quantity}
            elif type(quantity) == str:
                quantity_dict = {"ingredient_quantity_str": quantity}
            else:
                raise Exception('ingredient quantity must be an integer, decimal, or string')
            ingredient_data = {"ingredient_name": i}
            ingredient_data.update(quantity_dict)
            ingredient_data["optional"] = optional
        recipe["ingredients"].append(ingredient_data)


    try:
        res = requests.post(url + route, json=recipe)
        res.raise_for_status()
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def inven_list_recipes(args):
    route = "recipes"
    try:
        res = requests.get(url + route, json={"access_token": auth.get_token()})
        res.raise_for_status()
        if res.status_code == 200:
            for recipe in res.json():
                name = recipe['recipe_name']
                print(name)
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_use_recipe(args):
    route = 'recipes'
    isRecipeKnown = False
    try:
        res = requests.get(url + route, json={"access_token": auth.get_token()})
        res.raise_for_status()
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
        res = requests.put(url + route, json={"recipe": args.recipe, "access_token": auth.get_token()})
        if res.status_code == 200:
            print(res.json()['message'])
            print("CONSUMED:")
            for i in res.json()['consumed']:
                print(i)
        else:
            print(res.json()["message"])
            print(res.json()["missing"])
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        pass

def inven_view_recipe(args):
    route = 'useRecipe'
    recipe = args.recipe
    try:
        route = "recipeIngredients"
        res = requests.get(url + route, json={"recipe": recipe, "access_token": auth.get_token()})
        res.raise_for_status()
        if res.status_code == 200:
            for i in res.json():
                name = i['ingredient_name']
                count, optional, unchecked = i.get('ingredient_count', 0), i['optional'], i.get('ingredient_quantity_str', None) is not None
                if count is None:
                    count = 0
                count = int(count)
                quantity_str = i.get('ingredient_quantity_str', '')

                line = f'{name}:'
                if count != 0:
                    line += f' {count}'
                else:
                    line += f' {quantity_str}'

                if optional:
                    line += f' (optional)'

                if unchecked:
                    line += f', must be manually checked due to non-numeric units'
                print(line)
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def inven_update_recipe(args):
    inven_remove_recipe(args)
    inven_add_recipe(args)
    print(args.recipe + " has been updated ")


def inven_remove_recipe(args):
    route = "removeRecipe"
    try:
        res = requests.delete(url + route, json={"recipe": args.recipe, "access_token": auth.get_token()})
        res.raise_for_status()
        if res.status_code == 200:
            print(res.json())
        else:
            print("ERR " + str(res.status_code) + ": " + res.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_shopping_list(args):
    recipes = args.shoppingList
    # dict: ingredient name => dict(required count, optional count, required set flag, optional set flag)
    buy = {}
    for r in recipes:
        try:
            route = "recipeIngredients"
            res = requests.get(url + route, json={"recipe": r, "access_token": auth.get_token()})
            res.raise_for_status()
            if res.status_code == 200:
                for i in res.json():
                    route = "ingredientTotal"
                    name = i['ingredient_name']
                    count, optional, unchecked = i.get('ingredient_count', 0), i['optional'], i.get('ingredient_quantity_str', None) is not None
                    if count is None:
                        count = 0
                    count = int(count)
                    if name not in buy:
                        buy[name] = {"required": 0, "optional": 0, "required_unchecked": False, "optional_unchecked": False}
                    if optional:
                        buy[name]["optional"] += count
                        if unchecked:
                            buy[name]["optional_unchecked"] = True
                    else:
                        buy[name]["required"] += count
                        if unchecked:
                            buy[name]["required_unchecked"] = True
            else:
                print("ERR " + str(res.status_code) + ": " + res.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    for ingredient in buy:
        data = buy[ingredient]
        req, opt, required_unchecked, optional_unchecked = data["required"], data["optional"], data["required_unchecked"], data["optional_unchecked"]
        ingredient_count = requests.get(
                url + "ingredientTotal", json={"ingredient": ingredient, "access_token": auth.get_token()})
        ingredient_count = ingredient_count.json()
        req = max(0, req - ingredient_count)
        opt = max(0, opt - ingredient_count)

        line = f"{ingredient}: "
        sep = False

        if req > 0:
            line += f"{req}"
            sep = True
        if opt > 0:
            if sep:
                line += " + "
            line += f"{opt} optional"
            sep = True

        if required_unchecked:
            if sep:
                line += ", "
            line += f"manually check availability"
        elif optional_unchecked:
            if sep:
                line += ", "
            line += f"manually check availability (optional)"

        emit = req > 0 or opt > 0 or required_unchecked or optional_unchecked
        if emit:
            print(line)

def inven_login(args):
    auth.login()

def inven_whoami(args):
    login = auth.github_username()
    print(f"Logged in as {login}")
