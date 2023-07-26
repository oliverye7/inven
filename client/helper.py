import requests
from datetime import datetime

url = "http://localhost:4000/"


def inven_add_ingredient(args):
    print("add ingredients")
    print(args)
    route = 'addIngredients'
    data = {"ingredients": [
        {
            "name": args[1],
            "count": args[0],
            "date": str(datetime.today().date()),
        }
    ]}

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
    pass


def inven_use_ingredient():
    pass
