"""
    Main logic for interacting with the database
"""
import decimal
import random
from datetime import datetime, timedelta
import bcrypt

from pythonProject.config import ORDER_CANCELLATION_TIMEFRAME, DELIVERY_TIME_IN_MINUTES
from pythonProject.currentCustomer import CurrentCustomer
from pythonProject.currentOrder import CurrentOrder
from pythonProject.models import Pizza, Ingredient, ExtraItem, Customer, Order, Delivery, Deliverer, PizzaOrder, \
    ExtraItemOrder, Customer_Address, DiscountCode
from pythonProject.database import session

''' FOOD FUNCTIONS'''

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


# Helper function to check if an ingredient already exists.
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
    existing_item = session.query(ExtraItem).filter_by(item_name=extra_item["item_name"]).first()
    if existing_item:
        return existing_item
    else:
        new_item = ExtraItem(item_name=extra_item["item_name"], cost=extra_item["cost"], dietary_status=extra_item["dietary_status"])
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


''' CUSTOMER & ORDER DELIVERY INFO'''

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


# Function to create a new order
def create_new_order():
    current_order_singleton = CurrentOrder()
    current_customer_singleton = CurrentCustomer()

    current_customer = current_customer_singleton.customer

    new_order = Order(
        customer_id=current_customer.customer_id,
        order_status="new")
    current_order_singleton.set_order(new_order)

    return CurrentOrder().order


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

def get_or_create_discount_code(discount_code_string):
    new_discount_code = DiscountCode(
        discount_string=discount_code_string
    )
    session.add(new_discount_code)
    session.commit()
    return  new_discount_code

''' PLACING & PROCESSING THE ORDER FUNCTIONS'''

# Method to place the current order instance
def place_current_order():
    current_order = CurrentOrder().order
    current_customer = CurrentCustomer().customer
    if current_order is None:
        print("Could not find the current order to be placed")
    else:
        CurrentOrder().update_status("placed")
        CurrentOrder().update_timestamp()

    if current_customer and current_customer.pizza_count >= 10:
        current_customer.pizza_count -= 10

    session.commit()
# Method to find the customer that belongs to the current order
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


# Method to add an extra item to the current order of a customer
def add_extra_item_to_order(item_id):
        current_order_singleton = CurrentOrder()
        current_order = current_order_singleton.order

        if current_order is None:
            current_order = create_new_order()
        # Check if the extra_item is already in the order
        existing_extra_item_order = session.query(ExtraItemOrder).filter(
            ExtraItemOrder.order_id == current_order.order_id,
            ExtraItemOrder.item_id == item_id
        ).first()

        if existing_extra_item_order:
            # If the extra item is already in the order, increase the amount
            existing_extra_item_order.item_amount += 1
        else:
            # Create a new ExtraItemOrder entry
            new_extra_item_order = ExtraItemOrder(order_id=current_order.order_id, item_id=item_id, item_amount=1)
            session.add(new_extra_item_order)

        # Commit the session to save changes
        session.commit()

# Method to remove a pizza from the current order if need be
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


# Method to remove an extra item from the current order if need be
def remove_extra_item_from_current_order(item_id):
    current_order_singleton = CurrentOrder()

    # Get the current order
    current_order = current_order_singleton.order

    # If no current order exists, exit the method as there's nothing to remove
    if not current_order:
        return

    # Check if the pizza is already in the order
    existing_extra_item_order = session.query(ExtraItemOrder).filter(
        ExtraItemOrder.order_id == current_order.order_id,
        ExtraItemOrder.item_id == item_id
    ).first()

    if existing_extra_item_order:
        # If the extra item amount is greater than 1, reduce the amount by 1
        if existing_extra_item_order.item_amount > 1:
            existing_extra_item_order.item_amount -= 1
        else:
            # If the amount is 1, remove the extra item order from the session
            session.delete(existing_extra_item_order)

        # Commit the session to save changes
        session.commit()


# Method to cancel the order with the given order ID and refresh the page.
def cancel_order(order_id):
    order_to_cancel = session.query(Order).filter_by(order_id=order_id).first()
    if order_to_cancel:
        session.delete(order_to_cancel)
        session.commit()  # Save the changes to the database


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

# Method to assign a postal code to a deliverer
def assign_deliverer(postal_code, session):

    deliverer = session.query(Deliverer).filter_by(postal_code=None).first()
    if deliverer:
        deliverer.postal_code = postal_code
        session.commit()
        return deliverer
    return None

def process_orders(session):
    now = datetime.now()
    print("Checking for 'placed orders")
    placed_orders = session.query(Order).filter_by(order_status='placed').filter(Order.order_timestamp <= now - timedelta(minutes=ORDER_CANCELLATION_TIMEFRAME)).all()
    for order in placed_orders:
        order.order_status = 'in process'
        session.commit()

def deliver_orders(session):
    """Process orders that are in 'in process' status and assign them to deliveries."""

    print("Checking for 'in process' orders...")
    orders = session.query(Order).filter_by(order_status='in process').all()
    if not orders:
        print("No orders to process.")
        return

    # Group orders by postal code
    postal_code_groups = {}
    for order in orders:
        customer_address = session.query(Customer_Address).join(Customer).filter(
            Customer.customer_id == order.customer_id).first()
        if customer_address:
            postal_code = customer_address.postal_code
            if postal_code not in postal_code_groups:
                postal_code_groups[postal_code] = []
            postal_code_groups[postal_code].append(order)

    for postal_code, orders in postal_code_groups.items():
        deliverer = assign_deliverer(postal_code, session)
        if deliverer is None:
            print(f"No available deliverer for postal code {postal_code}.")
            print(f"Employing another guy")
            employ_another_guy(session)
            return

        new_delivery = Delivery(
            deliverer_id=deliverer.deliverer_id,
            initiation_time=datetime.now()
        )
        session.add(new_delivery)
        session.commit()

        for order in orders:
            order.delivery_id = new_delivery.delivery_id
            order.order_status = 'being delivered'
            session.commit()

        print(f"Assigned {len(orders)} order(s) to deliverer {deliverer.deliverer_first_name} {deliverer.deliverer_last_name} for postal code {postal_code}.")

def monitor_deliveries(session):
    print("Checking for completed deliveries...")
    now = datetime.now()
    completed_deliveries = session.query(Delivery)\
        .filter(Delivery.initiation_time <= now - timedelta(minutes=DELIVERY_TIME_IN_MINUTES)).all()

    if not completed_deliveries:
        print("No deliveries to complete.")
        return

    for delivery in completed_deliveries:
        orders = session.query(Order).filter_by(delivery_id=delivery.delivery_id).all()
        for order in orders:
            order.order_status = 'completed'

            # Retrieve the customer associated with this order
            customer = session.query(Customer).filter_by(customer_id=order.customer_id).first()

            if customer:
                print("increase the pizza count for customer")
                # Calculate the total amount of pizzas in this order
                pizza_count_in_order = get_pizza_amount_in_order(order)

                # Increment the customer's pizza count
                customer.pizza_count += pizza_count_in_order
                session.commit()
            else:
                print("couldn't find customer")

        delivery.deliverer.postal_code = None
        session.commit()

        session.delete(delivery)
        session.commit()

        print(f"Marked delivery {delivery.delivery_id} as completed and set {len(orders)} order(s) to 'completed' status. Delivery instance deleted.")

def employ_another_guy(session):
    """Employ another deliverer with a unique name not already in the database."""
    first_names = ["Chris", "Sam", "Alex", "Jordan", "Taylor", "Casey", "Jamie", "Robin", "Morgan", "Charlie"]
    last_names = ["Pepperoni", "Mozzarella", "Gorgonzola", "Olive", "Pesto", "Basilico", "Alfredo", "Parmesan",
                  "Garlic", "Margherita"]

    # Get existing deliverers from the database
    existing_deliverers = session.query(Deliverer).all()
    existing_names = {(deliverer.deliverer_first_name, deliverer.deliverer_last_name) for deliverer in
                      existing_deliverers}

    # Attempt to find a new unique name
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        # Generate a random name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = (first_name, last_name)

        # Check if this name is unique
        if full_name not in existing_names:
            # Add the new deliverer to the database
            new_deliverer = {"deliverer_first_name": first_name, "deliverer_last_name": last_name}
            get_or_create_deliverer(new_deliverer)
            print(f"New deliverer employed: {first_name} {last_name}")
            return  # Exit the function once a unique name is found and added
        attempts += 1

    # If no unique name was found after the maximum attempts
    print("Could not find a unique name for a new deliverer.")

def get_order(order_id):
    existing_order = session.query(Order).filter_by(order_id=order_id).first()
    if existing_order:
        return existing_order
    else:
        return "Order not found!"

# TODO: Create a new delivery
def create_delivery():
    pass


# TODO: Method to add an order to a delivery
def add_order_to_delivery(order):
    pass


# TODO: Method to remove an order from a delivery
def remove_order_from_delivery(order):
    pass

# Helper function to ensure the deliverers are not added to the database multiple times.
def find_deliverer(deliverer_id):
    existing_deliverer = session.query(Deliverer).filter_by(deliverer_id=deliverer_id).first()
    if existing_deliverer:
        return existing_deliverer
    else:
        return "Deliverer is not found!"


''' CALCULATION & DISCOUNT FUNCTIONS '''

# Function that calculates the price of a regular pizza
def calculate_pizza_price(pizza):
    # SQL query: finds the relevant ingredient cost for our 'ingredient' that belongs to our 'pizza'
    # and sums all these costs
    return sum(ingredient.ingredient_cost for ingredient in pizza.ingredients) * decimal.Decimal(1.49)

def get_dietary_status(pizza):

    dietary_status = "vegan"

    # Iterate through each ingredient to adjust the status
    for ingredient in pizza.ingredients:
        if ingredient.dietary_status == "non-vegetarian":
            return "non-vegetarian"
        elif ingredient.dietary_status == "vegetarian":
            dietary_status = "vegetarian"
    return dietary_status

# TODO: Method to calculate the earnings

def calculate_earnings(selected_month, selected_region, selected_gender, selected_age):
    """Calculate the total earnings and count the orders based on the filter criteria."""
    from datetime import datetime
    from sqlalchemy import func

    # Base query to filter orders and calculate earnings
    query = session.query(Order).filter_by(order_status='completed')

    query = query.join(Customer, Order.customer_id == Customer.customer_id).join(
        Customer_Address, Customer.customer_id == Customer_Address.customer_id)

    # Apply filters if specified
    if selected_month and selected_month != "All Time":
        month_index = datetime.strptime(selected_month, "%B").month  # Convert month name to index (1-12)
        query = query.filter(func.extract('month', Order.order_timestamp) == month_index)

    if selected_region:
        query = query.filter(
            (Customer_Address.postal_code.ilike(f"%{selected_region}%")) |
            (Customer_Address.city.ilike(f"%{selected_region}%"))
        )

    if selected_gender and selected_gender != "All":
        query = query.filter(Customer.gender == selected_gender)

    if selected_age:
        try:
            # Extract lower and upper age bounds
            lower_age, upper_age = map(int, selected_age.split('-'))
            # Calculate birthdate range based on current date
            current_year = datetime.now().year
            birth_year_start = current_year - upper_age
            birth_year_end = current_year - lower_age
            query = query.filter(
                func.extract('year', Customer.date_of_birth).between(birth_year_start, birth_year_end))
        except ValueError:
            print("Invalid age range format provided.")

    # Execute the query to get the filtered orders
    filtered_orders = query.all()

    # Calculate total earnings and the number of orders
    total_earnings = 0
    order_count = len(filtered_orders)
    for order in filtered_orders:
        total_earnings += calculate_order_price(order)

    return total_earnings, order_count

# TODO: Method to calculate the price of an entire order

def calculate_order_price(order):
    """Calculate the total price of a given order."""
    total_price = 0.00  # Initialize total price as a float

    # Calculate the total price for each pizza in the order
    pizzas_in_order = session.query(PizzaOrder).filter_by(order_id=order.order_id).all()
    cheapest_pizza_price = 0
    cheapest_extra_item_price = 0

    # Calculate the total price for each pizza in the order
    for pizza_order in pizzas_in_order:
        # Get the pizza details from the Pizza table
        pizza = session.query(Pizza).filter_by(pizza_id=pizza_order.pizza_id).first()
        if pizza:
            # Calculate the cost of this specific pizza and multiply by the quantity
            pizza_price = float(calculate_pizza_price(pizza))  # Ensure this is a float
            total_price += float(pizza_price * pizza_order.pizza_amount)  # Convert pizza_order.pizza_amount to float

            # Check if this pizza is the cheapest one
            if cheapest_pizza_price == 0 or pizza_price < cheapest_pizza_price:
                cheapest_pizza_price = pizza_price

    # Calculate the total price for each extra item in the order
    extra_items_in_order = session.query(ExtraItemOrder).filter_by(order_id=order.order_id).all()

    for extra_item_order in extra_items_in_order:
        # Get the extra item details from the ExtraItem table
        extra_item = session.query(ExtraItem).filter_by(item_id=extra_item_order.item_id).first()
        if extra_item:
            # Add the cost of the extra item multiplied by its quantity
            total_price += float(extra_item.cost * extra_item_order.item_amount)  # Ensure this is a float

            # Check if this extra item is the cheapest one
            if cheapest_extra_item_price == 0 or float(extra_item.cost) < cheapest_extra_item_price:
                cheapest_extra_item_price = float(extra_item.cost)

    # Exclude cheapest pizza and extra item if birthday products are free
    if order.free_birthday_products:
        total_price -= cheapest_pizza_price  # Exclude cheapest pizza
        if cheapest_extra_item_price <= 4:
            total_price -= cheapest_extra_item_price  # Exclude cheapest extra item

    # Apply discount if applicable
    if order.discount_applied:
        total_price *= 0.90  # Apply a 10% discount

    # Ensure the total price does not go below zero
    total_price = max(total_price, 0.0)

    return total_price

# Method to get the total amount of pizzas in an order
def get_pizza_amount_in_order(order):
    pizza_orders = session.query(PizzaOrder).filter_by(order_id=order.order_id).all()

    # Sum up the quantity of each pizza in the order
    total_pizzas = sum(pizza_order.pizza_amount for pizza_order in pizza_orders)

    return total_pizzas

def remove_discount():
    current_order_singleton = CurrentOrder()
    current_order = current_order_singleton.order

    if not current_order:
        return
    current_order.discount_applied = False
    session.commit()
# Method to apply a discount without a discount code
def apply_pizza_discount():
    current_order_singleton = CurrentOrder()
    current_order = current_order_singleton.order

    if not current_order:
        return
    current_order.discount_applied = True
    session.commit()

# Method to apply a discount by providing a valid discount code
def apply_discount_code(discount_code_entry):
    discount_code = session.query(DiscountCode).filter_by(discount_string=discount_code_entry).first()
    if discount_code:
        current_order_singleton = CurrentOrder()
        current_order = current_order_singleton.order

        if not current_order:
            return
        current_order.discount_applied = True
        session.commit()

def apply_birthday_discount():
    """Apply a birthday discount to the current order if today is the customer's birthday."""
    # Get the current customer instance
    current_customer_singleton = CurrentCustomer()
    current_customer = current_customer_singleton.customer

    if current_customer:
        # Get the current date
        today = datetime.now().date()
        # Extract the date of birth of the current customer
        date_of_birth = current_customer.date_of_birth

        # Check if today matches the customer's birthday (ignoring the year)
        if today.month == date_of_birth.month and today.day == date_of_birth.day:
            # Access the current order instance
            current_order_singleton = CurrentOrder()
            current_order = current_order_singleton.order

            if current_order:
                # Apply the birthday discount
                current_order.free_birthday_products = True

                # Commit the changes to the database
                session.commit()



# TODO: Method to calculate when someone has a right to the 10% discount (so after 10 pizzas ordered)

# TODO: Method to offer someone a free pizza + drink on their bday

# TODO: Method to apply discount codes / birthday discounts / 10 pizza reward discounts
