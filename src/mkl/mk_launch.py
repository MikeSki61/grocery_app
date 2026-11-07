#!/usr/bin/env python

import argparse
from PyQt5 import QtWidgets
import sys

from mkl import mk_core
from mkl import constants
from mkl import utils
from mkl.paths import ensure_dirs
from mkl.ui import mkl_ui, stylesheet

class Launch:
    def __init__(self):
        self.grocery_app = mk_core.GroceryList()

    def launch(self, mode="interactive") -> None:
        """
        Main loop to handle user commands for managing the grocry list.

        Commands:
        - add Add a new item to the grocry list.
        - remove Remove an item from the grocery list
        - edit Edit the details of any item in the grocery list
        - list  Display all items in the grocery list
        - export Export all items of the shopping list
        - search Search for any item in the grocery list
        - quit Exit the application
        """
        if mode == "interactive":
            self.run_interactive()
        elif mode == "cli":
            print("Use CLI mode from main()")
        elif mode == "ui":
            app = QtWidgets.QApplication(sys.argv)
            app.setStyleSheet(stylesheet.load_stylesheet())
            ui = mkl_ui.GroceryApp()
            ui.show()
            app.exec_()
        else:
            print(f"Unknown mode: {mode}")

    def run_interactive(self) -> None:
        print("")
        print(utils.get_line_delimiter())
        print("Welocome to your MK Grocery List Manager!")
        print(utils.get_line_delimiter())

        while True:
            command = input(
                "Enter a command(add, remove, edit, list, export, search, quit):"
            ).lower

            if command == "add":
                # Add an item to the grocery list.
                self.handle_add_command()
                
            elif command == "remove":
                # Remove an item from the grocery list.
                    self.handle_remove_command()

            elif command == "edit":
                # Edit an item in the grocery list.
                self.handle_edit_command()

            elif command == "list":
                self.handle_list_command()

            elif command == "export":
                self.grocery_app.export_items()

            elif command == "search":
                self.handle_search_command()

            elif command == "quit":
                break
            else:
                print("Invalid command. Please try again.")

    # Command handlers====================

    def handle_add_command(self, args=None):
        if args:
            name = args.name
            store = args.store
            cost = args.cost
            amount = args.amount
            priority = args.priority

            buy = args.buy.lower() in constants.BUY_TRUE
        else:
            name, store, cost, amount, priority, buy = self.get_inputs()

        self.grocery_app.add_item(
            name=name, store=store, cost=cost, amount=amount, priority=priority, buy=buy
        )

        print(f"{name} was added to the grocery list")
        print(utils.get_line_delimiter())

    def handle_remove_command(self, args: argparse.Namespace | None = None) -> None:
        """
        Remove an item by name prefix.

        If multiple items match, prompt the user to choose which one.
        """
        if args and getattr(args, "name", None):
            name = " ".join(args.name).strip() if isinstance(
                args.name, list) else str(args.name).strip()
        else:
            name = input("\nEnter the item name to remove: ").strip()

        print("")
        matches = self.grocery_app.search_item_name(name)

        if not matches:
            print(f"I'm sorry, I could not find a match for '{name}'.")
            return

        if len(matches) > 1:
            for match_num, match in enumerate(matches, start=1):
                print(
                    f"{match_num}. "
                    f"| Name: {match.name} "
                    f"| Store: {match.store} "
                    f"| Cost: {match.cost} "
                    f"| Amount: {match.amount} "
                    f"| Priority: {match.priority} "
                    f"| Buy: {match.buy}"
                )

            item_num = input(
                "\nPlease select the number you would like to remove: ").strip()
            match_item = matches[int(item_num) - 1]

            self.grocery_app.remove_item(name, id=match_item.id)
            print("\nSelected item has been removed.")
            return

        match_item = matches[0]
        self.grocery_app.remove_item(name, id=match_item.id)
        print("That item has been removed.\n")

    def handle_edit_command(self):  # This is the command to be used to edit
        item = input("Which item would you like to edit? ")
        matches = self.grocery_app.search_item_name(item)

        if not matches:
            print(f"There are no items with the name {item}")

        elif len(matches) > 1:
            match_num = 1
            for match in matches:
                match_string = (
                    f"item {match_num} "
                    f"| name: {match["name"]} "
                    f"| store: {match["store"]} "
                    f"| cost: {match["cost"]} "
                    f"| amount: {match["amount"]} "
                    f"| priority: {match["priority"]} "
                    f"| buy: {match["buy"]}"
                )
                print(match_string)
                match_num += 1

            item_num = input("Which item do you want to edit?")
            match_item = matches[int(item_num) - 1]
            name, store, cost, amount, priority, buy = self.get_inputs()
            self.grocery_app.edit_item(
                name, store, cost, amount, priority, buy, match_item.id
            )
        else:
            match_item = matches[0]
            name, store, cost, amount, priority, buy = self.get_inputs()
            self.grocery_app.edit_item(
                name, store, cost, amount, priority, buy, match_item.id
            )

    def handle_list_command(self) -> None:
        self.grocery_app.list_items(self.grocery_app.grocery_list)

    def handle_search_command(self):
        """
        Handles the logic triggered by the search command in command line mode.
        Search a keyword and print the matches
        """
        # Get user imput for the search keyword
        search_keyword = input(
            "What is the name of the item you would like to search? "
        )
        print(utils.get_line_delimiter())

        print("Searching for matching items...")

        matches = self.grocery_app.search_item_name(search_keyword)

        if matches:

            print("Theese items match your search. ")
            self.grocery_app.list_items(matches)

        else:
            print("No items match the provided search item")

    def get_inputs(self):
        """The following functions are for the inputs
            to collect information for the list.
        export

                Returns:
                    string:  item to be added as a string
        """

        name = self.get_name_input()
        print(utils.get_line_delimiter())

        store = self.get_store_input()
        print(utils.get_line_delimiter())

        cost = self.get_cost_input()
        print(utils.get_line_delimiter())

        amount = self.get_amount_input()
        print(utils.get_line_delimiter())

        priority = self.get_priority_input()
        print(utils.get_line_delimiter())

        buy = self.get_buy_input()
        print(utils.get_line_delimiter())

        return name, store, cost, amount, priority, buy

    @staticmethod
    def get_name_input():
        """
        Get the user input for the name attribute.

        Returns:
            name(str) The name of the item

        """
        print("Enter a name for the item. (ex. ice cream)")
        # Get the name input
        name = input("Item name: ").strip()

        if not name:
            name = constants.NAME_DEFAULT

        return name

    @staticmethod
    def get_store_input():
        print("Enter the name of the store for the item. (ex. Walmart)")

        # Get the store input
        store = input("Store name (or 'skip' to leave blank): ").strip()

        # No store provided, set to default
        if not store:
            store = constants.STORE_DEFAULT

        return store

    @staticmethod
    def get_cost_input():
        print("Enter the cost of the item. (ex. 5.25)")

        while True:
            # Get the cost input
            cost = input("Item price: ").strip()

            # No cost input provided, set to default
            if not cost:
                cost = constants.COST_DEFAULT
                break

            try:
                # Convert the cost to a float
                cost = float(cost)
                break

            # Unable to convert the cost to a float
            except ValueError:
                print("Invalid input. Please enter a valid price.")

        return cost

    @staticmethod
    def get_amount_input():
        print("Enter the amount you need to get. (ex. 5)")
        while True:
            # Get the amount input
            amount = input("Item quantity: ").strip()
            # Amount not provided, set to default
            if not amount:
                amount = constants.AMOUNT_DEFAULT
                break

            try:
                # Convert the amount to an int
                amount = int(amount)
                # Amount must be at least 1
                if amount > 0:
                    break

                print("Quantity must be a positive number.")

            # Unable to convert amount to an int
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")

        return amount

    @staticmethod
    def get_priority_input():
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        print(f"Enter the priority for the item between " f"{p_min}-{p_max}. (ex. 2)")

        while True:
            # Get the priority input
            priority = input("Priority: ").strip()

            # No input provided, set to default
            if not priority:
                constants.PRIORITY_DEFAULT
                break

            try:
                # Convert the priority to an int
                priority = int(priority)

                # Check priority is within min to max
                if p_min <= priority <= p_max:
                    break

            # Failed to convert priority to an int
            except ValueError:
                print(
                    f"Invalid input. Please enter a number between "
                    f"{p_min} and {p_max}."
                )

        return priority

    @staticmethod
    def get_buy_input():
        print("Enter if this item should be purchased now. (ex. yes)")

        while True:
            # Get the buy input
            buy = input("Buy: ").strip().lower()

            # No buy input provided
            if not buy:
                buy = constants.BUY_DEFAULT
                break

            # Buy input is true
            if buy in constants.BUY_TRUE:
                buy = True
                break

            # Buy input is false
            elif buy in constants.BUY_FALSE:
                buy = False
                break

            # Buy input was not valid
            else:
                print("Invalid input. Please enter true|yes OR false|no")

        return buy

def main() ->None:
    # Make sure the app directory exists
    ensure_dirs()
    parser = argparse.ArgumentParser(description="MK Grocery List Manager")
    parser.add_argument(
        "--mode",
        choices=["cli", "ui", "interactive"],
        default="interactive",
        help="Choose how to run the app: cli, ui, or interactive (default).",
    )

    subparsers = parser.add_subparsers(dest="command")
    # Add parser args
    add_parser = subparsers.add_parser("add", help="Add a new item")
    add_parser.add_argument("--name", required=True, help="Item name")
    add_parser.add_argument("--store", default=constants.STORE_DEFAULT, help="Store name" )
    add_parser.add_argument("--cost", type=float, default=constants.COST_DEFAULT, help="Item cost" )
    add_parser.add_argument("--amount", type=int, default=constants.AMOUNT_DEFAULT, help="Quantity")
    add_parser.add_argument("--priority",type=int,default=constants.PRIORITY_DEFAULT,help="Priority (1-5)",)
    add_parser.add_argument("--buy", type=str, default=str(constants.BUY_DEFAULT), help="Buy now? (yes/no)")

    # Remove parser args
    remove_parser = subparsers.add_parser("remove", help="Remove an item")
    remove_parser.add_argument("--name", nargs="+", help="Item name (or prefix) to remove")

    # Edit parser agrs
    edit_parser = subparsers.add_parser("edit", help="Edit an item")
    edit_parser.add_argument("--name", nargs="+", help="Item name (or prefix) to edit")
    edit_parser.add_argument("--new-name", dest="new_name",default=None, help="New name for the item (optional)")
    edit_parser.add_argument("--store", default=None,help="New store name (optional)")
    edit_parser.add_argument("--cost", type=float,default=None, help="New cost (optional)")
    edit_parser.add_argument("--amount", type=int,default=None, help="New quantity (optional)")
    edit_parser.add_argument("--priority", type=int,default=None, help="New priority 1-5 (optional)")
    edit_parser.add_argument("--buy",default=None,choices=(*constants.BUY_TRUE, *constants.BUY_FALSE),
        help="Set buy flag (yes/no/true/false or y/n/1/0). Omit to keep current.",
    )
    edit_parser.add_argument("--id", type=int, default=None, help="Item id to disambiguate when multiple items match")

    subparsers.add_parser("list", help="List items")
    subparsers.add_parser("export", help="Export items")

    # Searcht parser args
    search_parser = subparsers.add_parser("search", help = "Search for items")
    search_parser.add_argument("query", nargs="+", help="Search prefix for item name.Use quotes for multi_word searches")

    args = parser.parse_args()
    app = Launch()

    if args.mode == "interactive":
        app.launch(mode="interactive")

    elif args.mode == "ui":
        app.launch(mode="ui")

    elif args.mode == "cli":
        if not args.command:
            print(
                "Please provide a command (like 'add', 'remove', 'edit', 'list', 'export', 'search')"
            )
            return

        match args.command:
            case "add":
                app.handle_add_command(args)
            case "remove":
                app.handle_remove_command()
            case "edit":
                app.handle_edit_command()
            case "list":
                app.grocery_app.list_items(app.grocery_app.grocery_list)
            case "export":
                app.grocery_app.export_items()
            case "search":
                app.handle_search_command()


# Call the function
if __name__ == "__main__":
    main()
