from datetime import datetime

from pythonProject.models import Order
from pythonProject.database import session
from pythonProject.currentCustomer import CurrentCustomer  # Assuming this class is defined similarly to CurrentOrder

class CurrentOrder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentOrder, cls).__new__(cls)
            cls._instance.order = None
            cls._instance._initialize_order()
        return cls._instance

    def _initialize_order(self):
        """Check if there's an existing 'new' order for the current customer and set it as the current order."""
        current_customer_singleton = CurrentCustomer()
        current_customer = current_customer_singleton.customer

        if current_customer:
            # Query the database to find a "new" order for this customer
            existing_order = session.query(Order).filter_by(
                customer_id=current_customer.customer_id,
                order_status="new"
            ).first()

            if existing_order:
                self.order = existing_order
                print(f"Existing order found and set: Order ID {existing_order.order_id}")
            else:
                print("No existing order found for this customer. Ready to create a new one if needed.")
        else:
            print("No customer is set in the CurrentCustomer singleton.")

    @property
    def total_pizzas(self):
        """Calculate the total number of pizzas in the current order."""
        if self.order and self.order.pizza_orders:
            return sum(pizza_order.pizza_amount for pizza_order in self.order.pizza_orders)
        return 0

    def check_pizza_amount(self, pizza_id):
        """Check the amount of a specific pizza in the current order."""
        if self.order and self.order.pizza_orders:
            for pizza_order in self.order.pizza_orders:
                if pizza_order.pizza_id == pizza_id:
                    return pizza_order.pizza_amount
            return 0  # Pizza ID not found in the order
        else:
            print("No order is set or no pizzas are in the current order.")
            return 0

    def set_order(self, order):
        """Set the current order"""
        self.order = order
        session.add(self.order)
        session.commit()
        print("Set a new order in the singleton.")

    def update_status(self, new_status):
        """Update the status of the current order"""
        if self.order:
            self.order.order_status = new_status
            session.commit()
            print(f"Order status updated to: {new_status}")
        else:
            print("No order is set in the CurrentOrder singleton.")

    def update_timestamp(self):
        """Update the timestamp of the current order to the current time."""
        if self.order:
            self.order.order_timestamp = datetime.now()
            session.commit()
            print(f"Order timestamp updated to: {self.order.order_timestamp}")
        else:
            print("No order is set in the CurrentOrder singleton.")

    def commit_order(self):
        """Commit the current order to the database"""
        session.add(self.order)
        session.commit()

    def clear(self):
        """Clear the current order"""
        self.order = None
