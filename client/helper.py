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
            print(f"Request failed with status code: {res.status_code}")
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
                # print(res.json())
        else:
            print(f"Request failed with status code: {res.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
