# import sys
#
# if __name__ == "__main__":
#    # Join all the command line arguments (excluding the script name)
#    cmd = sys.argv[1:]
#    print(cmd)
#
#    if (cmd[0] == 'add'):
#    elif (cmd[0] == 'use'):
#        route = 'removeIngredients'
#        data = {}
#

import argparse
import helper


def main(args):
    # Your main script logic here
    print(args)
    if (args.addIngredient):
        helper.inven_add_ingredient(args.addIngredient)
    elif (args.useIngredient):
        helper.inven_use_ingredient(args.useIngredient)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Basic Argument Parsing Script")

    # Add arguments
    parser.add_argument("-ai", "--addIngredient", type=str, nargs='+',
                        help="add ingredient to pantry")

    parser.add_argument("-ui", "--useIngredient", type=str, nargs='+',
                        help="use a single ingredient")

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args)
