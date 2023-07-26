import requests
from datetime import datetime

url = "http://localhost:4000/"


def inven_add_ingredient(args):
    print("add ingredients")
    route = 'addIngredients'
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

    print(data)

    try:
        res = requests.post(url + route, json=data)
        if res.status_code == 200:
            print("Request successful. Response:")
            print(res.json())
        else:
            print(f"Request failed with status code: {res.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def inven_use_ingredient(args):
    print(args)
    route = 'removeIngredients'
    data = {
        "name": args[1],
        "count": args[0]
    }
    print(data)
    try:
        res = requests.put(url + route, json=data)
        if res.status_code == 200:
            print("Request successful. Response:")
            print(res.json())
        else:
            print(f"Request failed with status code: {res.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
