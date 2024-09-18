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

ingredients = [
    {"ingredient_name": "Tomato Sauce", "ingredient_cost": 2.00, "dietary_status": "vegan"},
    {"ingredient_name": "Mozzarella", "ingredient_cost": 3.00, "dietary_status": "vegetarian"},
    {"ingredient_name": "Zucchini", "ingredient_cost": 1.50, "dietary_status": "vegan"},
    {"ingredient_name": "Eggplant", "ingredient_cost": 1.70, "dietary_status": "vegan"},
    {"ingredient_name": "Gorgonzola", "ingredient_cost": 2.50, "dietary_status": "vegetarian"},
    {"ingredient_name": "Parmesan", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
    {"ingredient_name": "Fontina", "ingredient_cost": 2.20, "dietary_status": "vegetarian"},
    {"ingredient_name": "Paprika", "ingredient_cost": 1.10, "dietary_status": "vegan"},
    {"ingredient_name": "Onion", "ingredient_cost": 0.80, "dietary_status": "vegan"},
    {"ingredient_name": "Salami", "ingredient_cost": 3.50, "dietary_status": "non-vegetarian"},
    {"ingredient_name": "Rocket Salad", "ingredient_cost": 1.80, "dietary_status": "vegan"},
    {"ingredient_name": "Garlic", "ingredient_cost": 0.50, "dietary_status": "vegan"},
    {"ingredient_name": "Anchovies", "ingredient_cost": 3.00, "dietary_status": "non-vegetarian"},
    {"ingredient_name": "Capers", "ingredient_cost": 1.00, "dietary_status": "vegan"},
    {"ingredient_name": "Ham", "ingredient_cost": 3.20, "dietary_status": "non-vegetarian"},
    {"ingredient_name": "Mushrooms", "ingredient_cost": 1.50, "dietary_status": "vegan"},
    {"ingredient_name": "Pineapple", "ingredient_cost": 1.80, "dietary_status": "vegan"},
    {"ingredient_name": "Artichokes", "ingredient_cost": 2.30, "dietary_status": "vegan"}
]

for ingredient_data in ingredients:
    ingredient = Ingredient(
        ingredient_name=ingredient_data['ingredient_name'],
        ingredient_cost=ingredient_data['ingredient_cost'],
        dietary_status=ingredient_data['dietary_status']
    )
    get_or_create_ingredient(ingredient)

pizza_ingredient_map = {
    "Margherita": ["Tomato Sauce", "Mozzarella"],
    "Marinara": ["Tomato Sauce", "Garlic", "Onion"],
    "Ortolana": ["Tomato Sauce", "Zucchini", "Eggplant", "Paprika"],
    "Diavola": ["Tomato Sauce", "Mozzarella", "Salami"],
    "Napolitana": ["Tomato Sauce", "Mozzarella", "Anchovies", "Capers"],
    "Calzone": ["Mozzarella", "Ham", "Mushrooms", "Tomato Sauce"],
    "Hawaii": ["Tomato Sauce", "Mozzarella", "Ham", "Pineapple"],
    "Quattro Formaggi": ["Mozzarella", "Gorgonzola", "Parmesan", "Fontina"],
    "Vegana": ["Tomato Sauce", "Zucchini", "Paprika", "Mushrooms", "Rocket Salad"],
    "Capricciosa": ["Tomato Sauce", "Mozzarella", "Ham", "Mushrooms", "Artichokes"]
}

def add_ingredients_to_pizza(pizza_name, ingredient_names):
    pizza = get_or_create_pizza(pizza_name)
    for ingredient_name in ingredient_names:
        ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_name).first()
        if ingredient and ingredient not in pizza.ingredients:
            pizza.ingredients.append(ingredient)
    session.commit()

for pizza_name, ingredient_names in pizza_ingredient_map.items():
    add_ingredients_to_pizza(pizza_name, ingredient_names)

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
