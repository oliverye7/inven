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

    parser.add_argument("-p", "--pantry", action='store_true',
                        help="view current pantry")

    parser.add_argument("-P", "--aggregatePantry", action='store_true',
                        help="view current pantry with aggregated values")

    args = parser.parse_args()

    if hasattr(args, 'func') and callable(args.func):
        args.func(args)
    else:
        main(args)
