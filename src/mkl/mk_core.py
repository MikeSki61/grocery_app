
"""
mk_core.py
This file is the core file that provides the functions for the app.
It includes the ability to add, remove, edit, search and export the list.

Functions are:
-add_items(): Add items to the list.
-remove_items(): Removes items from the list.
-edit_items(): Edits any item within the list. Any value can be edited.
-export_items(): Able to export the list.
-search_items(): Able to search for items if there are duplicates using id number.

Author: Mike Kwiatkowsky
Version: 3.0.0
"""
import logging
import os
import re
import uuid

import mkl.constants as constants
import mkl.utils as utils
from mkl.grocery_item import GroceryItem

class GroceryList:
    
    def __init__(self):
        self.grocery_list_path = os.path.join(
            constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json"
        )
        
        self.grocery_list = []
        self.set_grocery_list()
    
    def add_item(self, name, store, cost, amount, priority, buy):
        """
        Add a new item to the list.

        Args:
            name (str): the name of the item
            store (str): the store where the item is bought
            cost (float): the cost of the item
            amount (int): the quantity of the item
            priority (int): the priority level for buying the item
            buy (bool): Whether the item should be bought
            id (int): Automatically generated
        """
        #  Generate a random UUID
        unique_id = int(uuid.uuid4())

        grocery_item = GroceryItem()
        grocery_item.name = name
        grocery_item.store = store
        grocery_item.cost = cost
        grocery_item.amount = amount
        grocery_item.priority = priority
        grocery_item.buy = buy
        grocery_item.id = unique_id

        self.grocery_list.append(grocery_item)
        self.save_data()
        logging.info(
            f"Added: {name} {store} {cost} {amount} {priority} {buy} {unique_id}"
        )



    def remove_item(self, name, id: int) -> None:
        
        """This is a function to remove items
            from the list as a string.

        Args:
            id (int): the assigned id for the item

        Returns:
            str: _return item as a string
        """
        
        index = self.get_index_from_id(id)
        self.grocery_list.pop(index)

        self.save_data()
        utils.show_warning(title="SUCCESS", msg=f"{name} was removed")



    def set_grocery_list(self):
        os.makedirs(constants.EXPORT_PATH, exist_ok=True)
        # file_path os.path.join(
        #     constants.EXPORT_PATH, f"{constants.GROCERY_LIST}.json")

        if os.path.exists(self.grocery_list_path):
            grocery_list = self.load_data()

        else:
            # Create and empty grocery list and save.
            print("No json path found, creating JSON path")
            grocery_list = []
            self.save_data()
            
        self.grocery_list = grocery_list

    def search_item_name(self, search_item):
        """
        Finds items in the grocery list whose name starts with the given search string.

        Args:
            search_item (str): The searcg string to match the start of the item names

        Returns:
            _type_: _description_
        """
        matching_items = []
        pattern = rf"^{search_item}"
        
        for item in self.grocery_list:
            if re.match(pattern, item.name, re.IGNORECASE):
                matching_items.append(item)
        return matching_items
    
    def sort_items(self, attribute, reverse=False):
        self.grocery_list = sorted(
            self.grocery_list,
            key=lambda item: getattr(item, attribute),
            reverse=reverse
        )

        utils.save_data(self.grocery_list_path, self.grocery_list)
        
    def get_index_from_id(self, id):
        """
        Get the index from the given id.

        Args:
            id (int): item number from the grocery list item

        Returns:
            int: The index of the grocery item in the grocery list 
        """
        index = 0

        for item in self.grocery_list:
            if item.id == id:
                return index
            else:
                index += 1

    def get_index_from_name(self, name: str):
    
        """_The get_index_from_name(name) function 
    will return the name of the item.

        Returns:
            _name_: _will return a string
        """
        index = 0
        self.grocery_list = self.get_grocery_list()

        for index, item in enumerate(self.grocery_list):
            if item.name == name:
                return index
        raise ValueError(f"Item with name '{name}' not found in grocery list. ")

    def edit_item(
        self,
        name: str,
        store: str | None = None, 
        cost: float | None = None, 
        amount: int | None = None, 
        priority: int | None = None,
        buy: str | bool= "skip", 
        id: int | None = None,
    ):
        """This is  function the allows the user to edit the items in a list.

        Args:
            name (str):The name of the item edit
            store (str | None)ed staore name. Defaults to none.
            cost (float | None):Updated cost. Defaults to None.
            amount (int | None): Updated amount. Defaults to None.
            priority (int | None): Updated priority. Defaults to None.
            buy (str | bool): Updated buy status. Defaults to "skip"
            id (str | None): Updated id.
        """
        
        index = self.get_index_from_id(id)
        current_item = self.grocery_list[index]

        if name:
            current_item.name = name
        
        if store:
            current_item.store = store
            
        if cost:
            current_item.cost = cost
            
        if amount:
            current_item.amount = amount
            
        if priority:
            current_item.priority = priority
        
        if buy == "skip":
            # keep existing value
            pass
        else:
            current_item.buy = buy

        if id:
            current_item.id = id

        self.save_data()

    def export_items(self):
        """_The export_items() function will export the items that may have
        been edited, removed or added to the list, 
        creating a new list called the buy_list.
        """
        buy_list = []
        for item in self.grocery_list:
            if item.buy:
                buy_list.append(item)
            
        if buy_list:
            self.list_items(buy_list)

            total_cost = self.calculate_total_cost(buy_list, round_cost=True)
            print(f"The total cost is ${total_cost}")
            print(utils.get_line_delimiter())

            exported_list_file = os.path.join(
                constants.EXPORT_PATH, constants.EXPORT_LIST
            )

            with open(exported_list_file, "w") as f:
                item_num = 1

                for item in buy_list:
                    item_string = (
                        f"item {item_num} "
                        f"|name: {item.name} "
                        f"|store: {item.store} "
                        f"|cost: {item.cost} "
                        f"|amount: {item.amount} "
                        f"|priority: {item.priority} "
                        f"|buy: {item.buy} "
                        )
                    
                    f.write(item_string + "\n")
                    item_num += 1

                f.write("\n")
                f.write(f"The total cost is ${total_cost}")
            
            return exported_list_file
                
    @staticmethod       
    def list_items(items)-> str:
        """The list_items() function will list / print the items.

        Returns:
            str: -items as a string
        """
        item_num = 1
        print("ITEMS: ")
        for item in items:
            item_string = (
                f"item {item_num}. "
                f"| name: {item.name} "
                f"| store: {item.store} "
                f"| cost: {item.cost} "
                f"| amount: {item.amount} "
                f"| priority: {item.priority} "
                f"| buy: {item.buy} "
            )
            print(item_string)  

    @staticmethod
    def calculate_total_cost( 
        grocery_list: list[object], 
        round_cost: bool = False,
        tax: float = 0.08,
        ):
        """_Parameters
        grocery_list (list[dict]): A list of dictionaries where each dictionary represents
        an item with keys 'amount' (int) and 'cost' (float).
        round_cost (bool): If True, rounds the total cost to the nearest integer. Default is False.
        tax (float): The tax rate to apply to the total cost. Default is the global TAX constant.

        Returns:
            _float: The total cost after applying tax and optional rounding.
        """
        total_cost = 0

        for item in grocery_list:
            cost = item.amount * item.cost
            total_cost += cost

        if round_cost:
            total_cost = round(total_cost, 2)
            
        if tax:
            total_cost += total_cost * tax

        return total_cost
    
    def save_data(self):
        export_list = []

        for item in self.grocery_list:
            export_list.append(vars(item))

        utils.save_data(self.grocery_list_path, export_list)

    def load_data(self):
        grocery_list = []
        json_data = utils.load_data(self.grocery_list_path)

        for item in json_data:
            grocery_item = GroceryItem()
            for key, value in item.items():

                # Ensure attribute exists
                if hasattr(grocery_item, key):
                    setattr(grocery_item, key, value)

            grocery_list.append(grocery_item)

        return grocery_list
    

