"""
    Main logic for interacting with the database
"""
from sqlalchemy import text
from models import Pizza, Ingredient, ExtraItem, Customer, Order, Delivery, Deliverer
from database import session, init_db

# Initialize the database (drop and create tables)
init_db()

# Filling in the pizza table
pizzas = ["Margherita", "Marinara", "Ortolana", "Diavola", "Napolitana",
          "Calzone", "Hawaii", "Quattro Formaggi", "Vegana", "Capricciosa"]

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

#Create for loop to ensure that all pizzas in the list are checked
for pizza_name in pizzas:
    get_or_create_pizza(pizza_name)

#Filling in the ingredients table
# TODO: check total costs now since i added pizza dough & check whether we want the drinks as ingredients

ingredients = [
    {"ingredient_name": "Pizza Dough", "ingredient_cost": 2.00, "dietary_status": "vegetarian"},
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
    {"ingredient_name": "Artichokes", "ingredient_cost": 2.30, "dietary_status": "vegan"},
    {"ingredient_name": "Coca Cola", "ingredient_cost": 3.00, "dietary_status": "vegan"},
    {"ingredient_name": "Ice Tea", "ingredient_cost": 3.00, "dietary_status": "vegan"},
    {"ingredient_name": "White Wine", "ingredient_cost": 3.50, "dietary_status": "vegan"},
    {"ingredient_name": "Red Wine", "ingredient_cost": 3.50, "dietary_status": "vegan"},
    {"ingredient_name": "Homemade Lemonade", "ingredient_cost": 3.50, "dietary_status": "vegan"},
    {"ingredient_name": "Nutella", "ingredient_cost": 2.50, "dietary_status": "vegetarian"},
    {"ingredient_name": "Cacoa powder", "ingredient_cost": 1.50, "dietary_status": "vegan"},
    {"ingredient_name": "Ladyfinger cookies", "ingredient_cost": 1.00, "dietary_status": "vegetarian"},
    {"ingredient_name": "Eggs", "ingredient_cost": 1.00, "dietary_status": "vegetarian"},
    {"ingredient_name": "Sugar", "ingredient_cost": 0.50, "dietary_status": "vegan"},
    {"ingredient_name": "Mascarpone", "ingredient_cost": 1.50, "dietary_status": "vegetarian"}
]

# Helper function to check if ingredient already exists
def get_or_create_ingredient(ingredient_input):
    existing_ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_input.ingredient_name).first()
    if existing_ingredient:
        return existing_ingredient
    else:
        new_ingredient = Ingredient(ingredient_name=ingredient_input.ingredient_name,
                                    ingredient_cost=ingredient_input.ingredient_cost,
                                    dietary_status=ingredient_input.dietary_status)
        session.add(new_ingredient)
        session.commit()
        return new_ingredient

#For loop to check that all ingredients in the list are added/in the db
for ingredient_input in ingredients:
    ingredient = Ingredient(
        ingredient_name=ingredient_input['ingredient_name'],
        ingredient_cost=ingredient_input['ingredient_cost'],
        dietary_status=ingredient_input['dietary_status']
    )
    get_or_create_ingredient(ingredient)

#Mapping the relations between the pizzas and their corresponding ingredients
pizza_ingredient_map = {
    "Margherita": ["Pizza Dough", "Tomato Sauce", "Mozzarella"],
    "Marinara": ["Pizza Dough", "Tomato Sauce", "Garlic", "Onion"],
    "Ortolana": ["Pizza Dough", "Tomato Sauce", "Zucchini", "Eggplant", "Paprika"],
    "Diavola": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Salami"],
    "Napolitana": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Anchovies", "Capers"],
    "Calzone": ["Pizza Dough", "Mozzarella", "Ham", "Mushrooms", "Tomato Sauce"],
    "Hawaii": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Ham", "Pineapple"],
    "Quattro Formaggi": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Gorgonzola", "Parmesan", "Fontina"],
    "Vegana": ["Pizza Dough", "Tomato Sauce", "Zucchini", "Paprika", "Mushrooms", "Rocket Salad"],
    "Capricciosa": ["Pizza Dough", "Tomato Sauce", "Mozzarella", "Ham", "Mushrooms", "Artichokes"]
}

#Function for customers that want to add ingredients to their pizza
# TODO: Function to remove ingredients from a pizza

#Function that represents the junction table pizza ingredients
def add_ingredients_to_pizza(pizza_name, ingredient_names):
    pizza = get_or_create_pizza(pizza_name)
    for ingredient_name in ingredient_names:
        ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_name).first()
        print(ingredient)
        if ingredient and ingredient not in pizza.ingredients:  #read if there's an ingredient and that pizza is not in the pizza ingredients
            print(" added")
            pizza.ingredients.append(ingredient)
    session.commit()

for pizza_name, ingredient_names in pizza_ingredient_map.items():
    add_ingredients_to_pizza(pizza_name, ingredient_names)

# TODO: rewrite the code add_ingredients_to_pizz to form the pizza_order table

#Filling in the extra items table
extra_items = ["Coca Cola", "Ice Tea", "White Wine", "Red Wine", "Homemade Lemonade", "Tiramisu", "Nutella Pizza"]

# TODO: Still needs to be used
extra_item_ingredient_map = {
    "Nutella Pizza": ["Pizza Dough", "Nutella"],
    "Tiramisu": ["Sugar", "Eggs", "Mascarpone", "Cacoa Powder"],
    "Coca Cola": ["Coca Cola"],
    "Ice Tea": ["Ice Tea"],
    "Red Wine": ["Red Wine"],
    "White Wine": ["White Wine"],
    "Homemade Lemonade": ["Homemade Lemonade"]
}

# Helper function to check if extra item already exists
def get_or_create_extra_item(extra_item):
    existing_item = session.query(ExtraItem).filter_by(item_name=extra_item).first()
    if existing_item:
        return existing_item
    else:
        new_item = ExtraItem(item_name=extra_item)
        session.add(new_item)
        session.commit()
        return new_item

# TODO: rewrite this code to form the item_ingreidents table IF tom wants us to keep the junction table
'''def add_ingredients_to_item(pizza_name, ingredient_names):
    pizza = get_or_create_pizza(pizza_name)
    for ingredient_name in ingredient_names:
        ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_name).first()
        print(ingredient)
        if ingredient and ingredient not in pizza.ingredients:  #read if there's an ingredient and that pizza is not in the pizza ingredients
            print(" added")
            pizza.ingredients.append(ingredient)
    session.commit()

for pizza_name, ingredient_names in pizza_ingredient_map.items():
    add_ingredients_to_pizza(pizza_name, ingredient_names)'''

# TODO: rewrite the code above to form the item_order table

# Helper function to check if customer already exists
def find_or_create_customer(customer_email):
    existing_customer = session.query(Customer).filter_by(customer_email=customer_email).first()
    if existing_customer:
        return existing_customer
    else:
        new_customer = Customer(customer_email=customer_email)
        session.add(new_customer)
        session.commit()
        return new_customer

# Helper function to check if the order already exists
def find_or_create_order(order_id):
    existing_order = session.query(Order).filter_by(order_id=order_id).first()
    if existing_order:
        return existing_order
    else:
        new_order = Order(order_id=order_id)
        session.add(new_order)
        session.commit()
        return new_order

# Helper function to check if the delivery is already existing
def find_or_create_delivery(delivery_id):
    existing_delivery = session.query(Delivery).filter_by(delivery_id=delivery_id).first()
    if existing_delivery:
        return existing_delivery
    else:
        new_delivery = Delivery(delivery_id=delivery_id)
        session.add(new_delivery)
        session.commit()
        return new_delivery

# Helper function to ensure the deliverers are not added to the db multiple times
def find_or_add_deliverer(deliverer_id):
    existing_deliverer = session.query(Deliverer).filter_by(deliverer_id=deliverer_id).first()
    if existing_deliverer:
        return existing_deliverer
    #So this else is not possible right? Unless new people are hired i guess
    else:
        new_deliverer = Deliverer(deliverer_id=deliverer_id)
        session.add(new_deliverer)
        session.commit()
        return new_deliverer

#To end the session
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


# TODO:  Method to cancel order within 5 min


# TODO: Method to calculate when someone has a right to a discount


# TODO: Method to apply discount code
