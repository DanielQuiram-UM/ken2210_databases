"""
    Main logic for interacting with the database
"""
import decimal
from pickletools import decimalnl_long

import bcrypt
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from pythonProject.currentCustomer import CurrentCustomer
from pythonProject.currentOrder import CurrentOrder
from pythonProject.models import Pizza, Ingredient, ExtraItem, Customer, Order, Delivery, Deliverer, PizzaOrder, \
    ExtraItemOrder
from pythonProject.database import session

''' FOOD STUFF'''


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


# Helper function to check if ingredient already exists.
def get_or_create_ingredient(ingredient):
    existing_ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient["ingredient_name"]).first()
    if existing_ingredient:
        return existing_ingredient
    else:
        new_ingredient = Ingredient(ingredient_name=ingredient["ingredient_name"],
                                    ingredient_cost=ingredient["ingredient_cost"],
                                    dietary_status=ingredient["dietary_status"])
        session.add(new_ingredient)
        session.commit()
        return new_ingredient


def get_or_create_deliverer(deliverer):
    # Check if a deliverer with the same first name and last name already exists
    existing_deliverer = session.query(Deliverer).filter_by(
        deliverer_first_name=deliverer["deliverer_first_name"],
        deliverer_last_name=deliverer["deliverer_last_name"]
    ).first()

    if existing_deliverer:
        return existing_deliverer
    else:
        # Create a new deliverer if not found
        new_deliverer = Deliverer(
            deliverer_first_name=deliverer["deliverer_first_name"],
            deliverer_last_name=deliverer["deliverer_last_name"]
        )
        session.add(new_deliverer)
        session.commit()
        return new_deliverer


# Function that represents the junction table pizza ingredients
def match_ingredients_to_pizza(pizza_name, ingredient_names):
    pizza = get_or_create_pizza(pizza_name)
    for ingredient_name in ingredient_names:
        ingredient = session.query(Ingredient).filter_by(ingredient_name=ingredient_name).first()
        if ingredient and ingredient not in pizza.ingredients:
            pizza.ingredients.append(ingredient)
    session.commit()


# Helper function to check if the pizza suborder already exists
def get_or_create_pizza_suborder(order_id):
    existing_pizza_suborder = session.query(PizzaOrder).filter_by(order_id=order_id).first()
    if existing_pizza_suborder:
        return existing_pizza_suborder
    else:
        new_pizza_suborder = PizzaOrder(order_id=order_id)
        session.add(new_pizza_suborder)
        session.commit()
        return new_pizza_suborder


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


# Helper function to check if item_suborder already exists
def get_or_create_item_suborder(order_id):
    existing_item_suborder = session.query(ExtraItemOrder).filter_by(order_id=order_id).first()
    if existing_item_suborder:
        return existing_item_suborder
    else:
        new_item_suborder = ExtraItemOrder(order_id=order_id)
        session.add(new_item_suborder)
        session.commit()
        return new_item_suborder


''' CUSTOMER & DELIVERY INFO'''


# Helper function to check if a customer already exists
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


# Helper function to check if the delivery already exists
def find_or_create_delivery(delivery_id):
    existing_delivery = session.query(Delivery).filter_by(delivery_id=delivery_id).first()
    if existing_delivery:
        return existing_delivery
    else:
        new_delivery = Delivery(delivery_id=delivery_id)
        session.add(new_delivery)
        session.commit()
        return new_delivery


# Helper function to ensure the deliverers are not added to the database multiple times.
def find_or_add_deliverer(deliverer_id):
    existing_deliverer = session.query(Deliverer).filter_by(deliverer_id=deliverer_id).first()
    if existing_deliverer:
        return existing_deliverer
    # So this else is not possible right? Unless new people are hired i guess
    else:
        new_deliverer = Deliverer(deliverer_id=deliverer_id)
        session.add(new_deliverer)
        session.commit()
        return new_deliverer


# To end the session
session.close()


# Defining common methods. These ones have to be implemented at some point

# Function that calculates the price of a regular pizza
def calculate_pizza_price(pizza):
    # SQL query: finds the relevant ingredient cost for our 'ingredient' that belongs to our 'pizza'
    # and sums all these costs
    return sum(ingredient.ingredient_cost for ingredient in pizza.ingredients) * decimal.Decimal(1.49)


# TODO: Method to calculate the price of an entire order

# Function to create a new order
def create_new_order():
    current_order_singleton = CurrentOrder()
    current_customer_singleton = CurrentCustomer()

    current_customer = current_customer_singleton.customer

    new_order = Order(
        customer_id=current_customer.customer_id,  # Assuming you have a customer_id field in the Order model
        order_status="new")
    current_order_singleton.set_order(new_order)  # Update the singleton with the new order

    return CurrentOrder().order


# Method to place the current order instance to be proceeded
def place_current_order():
    current_order = CurrentOrder().order
    if current_order is None:
        print("Could not find the current order to be placed")
    else:
        CurrentOrder().update_status("placed")
        CurrentOrder().update_timestamp()


def get_customer_from_order(order):
    return session.query(Customer).filter(Customer.customer_id == order.customer_id).first()


# Method to add a pizza to the current order of a customer
def add_pizza_to_current_order(pizza_id):
    current_order_singleton = CurrentOrder()
    current_order = current_order_singleton.order

    if current_order is None:
        current_order = create_new_order()
    # Check if the pizza is already in the order
    existing_pizza_order = session.query(PizzaOrder).filter(
        PizzaOrder.order_id == current_order.order_id,
        PizzaOrder.pizza_id == pizza_id
    ).first()

    if existing_pizza_order:
        # If the pizza is already in the order, increase the amount
        existing_pizza_order.pizza_amount += 1
    else:
        # Create a new PizzaOrder entry
        new_pizza_order = PizzaOrder(order_id=current_order.order_id, pizza_id=pizza_id, pizza_amount=1)
        session.add(new_pizza_order)

    # Commit the session to save changes
    session.commit()


# TODO: Method to add a product to an order
def add_extra_item_to_order(product, order):
    pass


def remove_pizza_from_current_order(pizza_id):
    current_order_singleton = CurrentOrder()

    # Get the current order
    current_order = current_order_singleton.order

    # If no current order exists, exit the method as there's nothing to remove
    if not current_order:
        return

    # Check if the pizza is already in the order
    existing_pizza_order = session.query(PizzaOrder).filter(
        PizzaOrder.order_id == current_order.order_id,
        PizzaOrder.pizza_id == pizza_id
    ).first()

    if existing_pizza_order:
        # If the pizza amount is greater than 1, reduce the amount by 1
        if existing_pizza_order.pizza_amount > 1:
            existing_pizza_order.pizza_amount -= 1
        else:
            # If the amount is 1, remove the pizza order from the session
            session.delete(existing_pizza_order)

        # Commit the session to save changes
        session.commit()


# TODO: Method to remove a product from an order
def remove_extra_item_from_current_order(product, order):
    pass


# Cancels the order with the given order ID and refreshes the page."""
def cancel_order(order_id):
    order_to_cancel = session.query(Order).filter_by(order_id=order_id).first()
    if order_to_cancel:
        session.delete(order_to_cancel)
        session.commit()  # Save the changes to the database


# TODO: Create a new delivery
def create_delivery():
    pass


# TODO: Method to add an order to a delivery
def add_order_to_delivery(order):
    pass


# TODO: Method to remove an order from a delivery
def remove_order_from_delivery(order):
    pass


''' CUSTOMER & DELIVERY FUNCTIONS'''


# Function to register a new customer
def register_customer(first_name, last_name, email, password, gender, dob, phone, street, city, country,
                      postal_code):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_customer = Customer(
        customer_first_name=first_name,
        customer_last_name=last_name,
        customer_email=email,
        password=hashed_password.decode('utf-8'),
        gender=gender,
        date_of_birth=dob,
        phone_number=phone,
        street=street,
        city=city,
        country=country,
        postal_code=postal_code
    )
    session.add(new_customer)
    session.commit()


# TODO: Method to remove a customer. Do we need this?
def remove_customer(customer):
    pass


# TODO: for delivery purposes
def get_customer_id():
    pass

# TODO: Method to calculate when someone has a right to the 10% discount (so after 10 pizzas ordered)

# TODO: Method to offer someone a free pizza + drink on their bday

# TODO: Method to apply discount codes / birthday discounts / 10 pizza reward discounts
