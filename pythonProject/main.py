"""
    Main logic for interacting with the database
"""
from sqlalchemy import text
from models import Pizza, Ingredient
from database import session, init_db

# Initialize the database (drop and create tables)
init_db()

# Helper function to check if pizza already exists
def get_or_create_pizza(pizza_name):
    existing_pizza = session.query(Pizza).filter_by(pizza_name=pizza_name).first()
    if existing_pizza:
        return existing_pizza
    else:
        new_pizza = Pizza(pizza_name=pizza_name)
        session.add(new_pizza)
        session.commit()
        return new_pizza


# Helper function to check if ingredient already exists
def get_or_create_ingredient(ingredient):
    existing_ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient.ingredient_name).first()
    if existing_ingredient:
        return existing_ingredient
    else:
        new_ingredient = Ingredient(ingredient_name=ingredient.ingredient_name,
                                    ingredient_cost=ingredient.ingredient_cost,
                                    dietary_status=ingredient.dietary_status)
        session.add(new_ingredient)
        session.commit()
        return new_ingredient

# Filling the pizza table
pizzas = ["Margherita", "Marinara", "Ortolana", "Diavola", "Napolitana",
          "Calzone", "Hawaii", "Quattro Formaggi", "Vegana", "Capricciosa"]

for pizza_name in pizzas:
    get_or_create_pizza(pizza_name)

Tomato_Sauce = Ingredient(ingredient_name="Tomato_Sauce", ingredient_cost=2.00, dietary_status="vegan")
Mozzarella = Ingredient(ingredient_name="Mozzarella")
Zucchini = Ingredient(ingredient_name="Zucchini")
Eggplant = Ingredient(ingredient_name="Eggplant")
Tomatoes = Ingredient(ingredient_name="Tomatoes")
Spinach = Ingredient(ingredient_name="Spinach")
Gorgonzola = Ingredient(ingredient_name="Gorgonzola")
Parmesan = Ingredient(ingredient_name="Parmesan")
Fontina = Ingredient(ingredient_name="Fontina")
Paprika = Ingredient(ingredient_name="Paprika")
Onion = Ingredient(ingredient_name="Onion")
Salami = Ingredient(ingredient_name="Salami")
Rocket_Salad = Ingredient(ingredient_name="Rocket_Salad")

get_or_create_ingredient(Tomato_Sauce)

# Test the connection and query the database
try:
    with session.bind.connect() as connection:
        # Simple query to test the connection
        result = connection.execute(text("SELECT 1"))

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()

# Defining common methods. These ones have to be implemented at some point

# TODO: Method to calculate the price of one pizza
def calculate_pizza_price(pizza):
    pass


# TODO: Method to calculate the price of an entire order
def calculate_order_price(order):
    pass


# TODO: Method to create a new customer
def create_customer(customer):
    pass


# TODO: Method to remove a customer
def remove_customer(customer):
    pass


# TODO: Create a new order
def create_order(customer_id):
    pass


# TODO: Method to add product to an order
def add_product_to_order(product, order):
    pass


# TODO: Method to remove a product from an order
def remove_product_from_order(product, order):
    pass


# TODO: Create a new delivery
def create_delivery():
    pass


# TODO: Method to add an order to a delivery
def add_order_to_delivery(order):
    pass


# TODO: Method to remove an order from a delivery
def remove_order_from_delivery(order):
    pass


# TODO: Method to add an order to a delivery
def add_order_to_delivery(pizza):
    pass


# TODO: ...
