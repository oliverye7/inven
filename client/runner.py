import argparse
import helper


def main(args):
    # Your main script logic here
    print(args)
    if (args.pantry):
        helper.inven_see_pantry()
    elif (args.aggregatePantry):
        helper.inven_see_aggregate_pantry()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Basic Argument Parsing Script")

    subparsers = parser.add_subparsers(title="subcommands", dest="action")

    add_parser = subparsers.add_parser("add", help="add ingredient to pantry")
    add_parser.add_argument("ingredient", type=str,
                            nargs='+', help="ingredient(s) to add")
    add_parser.set_defaults(func=helper.inven_add_ingredient)

    use_parser = subparsers.add_parser("use", help="use a single ingredient")
    use_parser.add_argument("quantity", type=int,
                            help="quantity of the ingredient to use")
    use_parser.add_argument("ingredient", type=str, help="ingredient to use")
    use_parser.set_defaults(func=helper.inven_use_ingredient)

    recipe_parser = subparsers.add_parser(
        "recipe", help="adds a recipe to the pantry memory")
    recipe_parser.add_argument(
        "recipe", type=str, help="name of recipe")
    recipe_parser.set_defaults(func=helper.inven_add_recipe)

    make_parser = subparsers.add_parser(
        "make", help="uses a recipe, if there are enough ingredients")
    make_parser.add_argument(
        "recipe", type=str, help="name of recipe")
    make_parser.set_defaults(func=helper.inven_use_recipe)

    update_parser = subparsers.add_parser(
        "update", help="updates a recipe in the db. if the recipe isn't already in the db, adds the recipe to the db")
    update_parser.add_argument(
        "recipe", type=str, help="name of recipe to be updated")
    update_parser.set_defaults(func=helper.inven_update_recipe)

    shopping_parser = subparsers.add_parser(
        "shopping", help="given a list of csv, generates a shopping list taking into acount existing ingredients in the pantry")
    shopping_parser.add_argument(
        "shoppingList", type=str, nargs="+", help="csv of recipe names")
    shopping_parser.set_defaults(func=helper.inven_shopping_list)

    parser.add_argument("-p", "--pantry", action='store_true',
                        help="view current pantry")

    parser.add_argument("-P", "--aggregatePantry", action='store_true',
                        help="view current pantry with aggregated values")

    args = parser.parse_args()

    if hasattr(args, 'func') and callable(args.func):
        args.func(args)
    else:
        main(args)
