# This program uses object-oriented programming to create a shoe inventory.
# For each shoe in the inventory, the following information is available:
    # Country, code, product name, cost, quantity, value
# The user is able to do the following: 
    # Search products by code;
    # Determine the product with the lowest quantity and restock it;
    # Determine the product with the highest quantity;
    # Calculate the total value of each stock item


from tabulate import tabulate 

# Welcome message:
print("\nWelcome to the online shoe inventory!")
# Standard error message:
no_shoes = "\nNo shoes found in the inventory. Enter 're' to read all shoes in the inventory before trying again.\n"

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Shoe(country={self.country}, code={self.code}, product={self.product}, cost={self.cost}, quantity={self.quantity})"

#=============Shoe list===========
"""The list will be used to store a list of objects of shoes."""
shoe_list = []

#==========Functions outside the class==============
def read_shoes_data():
    """Reads the shoe data from the inventory.txt file and stores it in shoe_list."""
    
    try:
        with open("inventory.txt", "r") as inventory_file:
            next(inventory_file) # skip first line
            for line in inventory_file: 
                data = line.strip().split(",")
                shoe = Shoe(data[0], data[1], data[2], float(data[3]), int(data[4]))  
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("\nThe file was not found.\n")
    print("\nShoes successfully read from the file!\n")
    return shoe_list
    

def capture_shoes():
    """Captures new shoe data from the user and stores it in shoe_list."""
    
    country = input("Enter the shoe's country of origin: ")
    code = input("Enter the shoe code: ")
    product = input("Enter the product name: ")
    while True:
        try:
            cost = float(input("Enter the cost per unit: "))
            break
        except ValueError:
            print("Please enter a valid cost (e.g. 123.45)")
    while True:
        try:
            quantity = int(input("Enter the quantity available: "))
            break
        except ValueError:
            print("Please enter a valid quantity (e.g. 10)")
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)
    print(f"{product} ({code}) from {country} has been added to the inventory.")


def view_all():
    """Iterates over the list of shoes in the inventory and prints the details."""
    
    if len(shoe_list) == 0:
        print(no_shoes)
        return
    header = ["Code", "Product", "Country", "Quantity", "Cost per Unit"]
    rows = []
    for shoe in shoe_list:
        rows.append([shoe.code, shoe.product, shoe.country, shoe.quantity, shoe.cost])
    print(tabulate(rows, headers=header, tablefmt="fancy_grid"))


def re_stock():
    """Finds the shoes with the lowest quantity and asks the user if they want to re-stock them."""
    
    if len(shoe_list) == 0:
        print(no_shoes)
        return

    # Sort shoes by quantity
    shoe_list.sort(key=lambda x: x.quantity)
    while True:
        # Group shoes with the same quantity
        groups = [[shoe for shoe in shoe_list if shoe.quantity == shoe_list[0].quantity]]
        for shoe in groups[0]:
            print(f"\n{shoe.product} ({shoe.code}) may need to be restocked. There are only {shoe.quantity} pairs in stock.")
            restock = input("Would you like to restock this shoe? (y/n) ").lower()
            if restock == "y":
                qty = int(input(f"\nHow many pairs of {shoe.product} would you like to add? "))
                if qty <= 0:
                    print("\nInvalid input. Try again.\n")
                    return
                shoe.quantity += qty
                print(f"\n{qty} pairs of {shoe.product} ({shoe.code}) have been added to the inventory.\n")
                break
            elif restock == "n":
                continue
        else:
            # Move on to the next group
            groups.pop(0)
            if len(groups) == 0:
                print(f"\nAll low-stock shoes have been checked.\n")
                return


def search_shoe():
    """Searches for a shoe from the list using the shoe code and prints it if found."""

    if len(shoe_list) == 0:
        print(no_shoes)
        return
    code = input("\nEnter the code of the shoe you are searching for: ")
    for shoe in shoe_list:
        if shoe.code == code:
            print(f"""
    Name: {shoe.product}
    Country: {shoe.country}
    Quantity: {shoe.quantity}
    Price: {shoe.cost}
            """)
            return
    print(f"\nNo shoe with code {code} found in the inventory.\n")


def value_per_item():
    """Calculates the total value for each shoe using the formula cost * quantity."""
    
    if len(shoe_list) == 0:
        print(no_shoes)
        return
    header = ["Code", "Product", "Quantity", "Cost per Unit", "Total Value"]
    rows = []
    for shoe in shoe_list:
        rows.append([shoe.code, shoe.product, shoe.quantity, shoe.cost, shoe.cost * shoe.quantity])
    print(tabulate(rows, headers=header, tablefmt="fancy_grid"))


def highest_qty():
    """Finds the shoe with the highest quantity and prints it."""

    max_qty = -1
    max_shoe = None
    for shoe in shoe_list:
        if shoe.get_quantity() > max_qty:
            max_qty = shoe.get_quantity()
            max_shoe = shoe
    if max_shoe:
        print(f"\nThe shoe with the highest quantity on sale is: {max_shoe.product} ({max_shoe.code}). There are {max_shoe.quantity} pairs in stock.\n")
    else:
        print(no_shoes)


#==========Main Menu=============
"""This menu executes each function defined above."""

while True: 
    shoe_menu = input("""What would you like to do?

re - read shoes
cs - capture shoes
va - view all shoes
rs - re-stock
sh - search shoe
vl - value per item
hq - highest quantity
ex - exit program

Input your choice: """)

    if shoe_menu == "re":
        read_shoes_data()
    
    elif shoe_menu == "cs":
        capture_shoes()
    
    elif shoe_menu == "va":
        view_all()
    
    elif shoe_menu == "rs":
        re_stock()
    
    elif shoe_menu == "sh":
        search_shoe()
    
    elif shoe_menu == "vl":
        value_per_item()
    
    elif shoe_menu == "hq":
        highest_qty()
    
    elif shoe_menu == "ex":
        print("\nClosing inventory.\n")
        break

    else:
        print("\nInvalid input. Please try again.\n")