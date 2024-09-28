from datetime import timedelta, datetime
from tkinter import Image

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage

from pythonProject.currentOrder import CurrentOrder
from pythonProject.currentCustomer import CurrentCustomer
from pythonProject.database import session
from pythonProject.main_functions import calculate_pizza_price, add_pizza_to_current_order, place_current_order, \
    remove_pizza_from_current_order, create_new_order
from pythonProject.models import Pizza, Ingredient, Order


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.configure(width=800, height=600)

        # Sidebar Frame
        sidebar_frame = CTkFrame(master=self, fg_color="#1A936F", width=176, height=600, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("../icons/pizza_icon.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(100, 100))

        order_icon_data = Image.open("../icons/order_basket_icon.png")
        order_icon = CTkImage(dark_image=order_icon_data, light_image=order_icon_data, size=(30, 30))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(10, 0), anchor="center")

        # Navigation Buttons on the Sidebar
        navigation_buttons = [
            ("Pizzas", lambda: self.show_page("Pizzas")),
            ("Ingredients", lambda: self.show_page("Ingredients")),
        ]

        # Create each button in the sidebar for main navigation
        for text, command in navigation_buttons:
            button = CTkButton(master=sidebar_frame, text=text, command=command, font=("Arial", 16), text_color="#fff",
                               fg_color="#1A936F", hover_color="#207244")
            button.pack(pady=10, padx=10, fill="x")

        # Add the order icon button for Current Order
        order_button = CTkButton(master=sidebar_frame, text="", command=lambda: self.show_page("Current Order"),
                                 image=order_icon, text_color="#fff",
                                 fg_color="#1A936F", hover_color="#207244")
        order_button.pack(pady=10, padx=10, fill="x")  # This adds the order icon button

        spacer_frame = CTkFrame(master=sidebar_frame, fg_color="#1A936F", height=20)
        spacer_frame.pack(fill="both", expand=True)  # This will expand to fill the available space

        # Account Navigation Buttons at the bottom
        account_navigation_buttons = [
            ("My Orders", lambda: self.show_page("My Orders")),
            ("Account", lambda: self.show_page("Account")),
            ("Logout", lambda: self.logout())
        ]

        # Create each account button in the sidebar
        for text, command in account_navigation_buttons:
            button = CTkButton(master=sidebar_frame, text=text, command=command, font=("Arial", 16), text_color="#fff",
                               fg_color="#1A936F", hover_color="#207244")
            button.pack(pady=10, padx=10, fill="x")

        # Main View Frame
        self.main_view = CTkFrame(master=self, fg_color="#fff", width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left", fill="both", expand=True)

        # Initialize different pages in the main view
        self.pages = {
            "Pizzas": self.create_pizzas_page,
            "Current Order": self.create_current_order_page,
            "Account": self.create_account_page,
            "My Orders": self.create_orders_page,
            "Ingredients": self.create_ingredients_page
        }

        # Display the default page
        self.show_page("Pizzas")

    def show_page(self, page_name):
        """Switch to the selected page within the main view."""
        # Clear any existing content in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Create the page content using the corresponding method
        if page_name in self.pages:
            self.pages[page_name]()

    def create_pizzas_page(self):
        """Create the Pizzas page view."""
        # Retrieve all Pizza objects from the database using the session.
        pizzas = session.query(Pizza).all()

        # Retrieve the current order instance
        current_order = CurrentOrder().order

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Our Pizzas", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)

        # Create a container frame for displaying the pizza details in a grid format
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Loop through each pizza and display its name, ingredients, and the amount controls
        for pizza in pizzas:
            # Calculate the total price of the pizza based on its ingredients
            total_price = calculate_pizza_price(pizza)

            # Check the current amount of this pizza in the order, if it exists
            pizza_amount = 0
            if current_order and current_order.pizza_orders:
                for pizza_order in current_order.pizza_orders:
                    if pizza_order.pizza_id == pizza.pizza_id:
                        pizza_amount = pizza_order.pizza_amount
                        break

            # Create a frame for each pizza
            pizza_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=120, corner_radius=8)
            pizza_frame.pack(pady=5, padx=10, fill="x")

            # Create a frame to hold the pizza name and price in the same row
            name_price_frame = CTkFrame(master=pizza_frame, fg_color="#eaeaea")
            name_price_frame.pack(fill="x", pady=(10, 0))

            # Add the Pizza name label on the left within name_price_frame
            pizza_name_label = CTkLabel(master=name_price_frame, text=pizza.pizza_name, font=("Arial", 16, "bold"),
                                        text_color="#000")
            pizza_name_label.pack(anchor="w", side="left", padx=(20, 0))

            # Add the Pizza price label on the right within name_price_frame
            price_label = CTkLabel(master=name_price_frame, text=f"{total_price:.2f}€", font=("Arial", 16, "bold"),
                                   text_color="#000")
            price_label.pack(anchor="e", side="right", padx=(10, 20))

            # Create a new frame to hold ingredients and amount controls
            details_frame = CTkFrame(master=pizza_frame, fg_color="#eaeaea")
            details_frame.pack(fill="x", pady=(5, 10))

            # Display ingredients on the left inside details_frame
            ingredients_text = ", ".join([ingredient.ingredient_name for ingredient in pizza.ingredients])
            ingredients_label = CTkLabel(master=details_frame, text=f"Ingredients: {ingredients_text}",
                                         font=("Arial", 14), text_color="#555")
            ingredients_label.pack(anchor="w", side="left", padx=(20, 0))

            # Create a frame for the counter and control buttons on the right inside details_frame
            control_frame = CTkFrame(master=details_frame, fg_color="#eaeaea")
            control_frame.pack(anchor="e", side="right", padx=20)

            # Add "-" button to decrease the pizza amount in the order
            decrease_button = CTkButton(
                master=control_frame,
                text="-",
                font=("Arial", 14),
                fg_color="#1A936F",
                text_color="#fff",
                hover_color="#207244",
                width=30,
                height=30,
                command=lambda pizza_id=pizza.pizza_id: remove_pizza_from_current_order(pizza_id)
            )
            decrease_button.pack(side="left", padx=(0, 5))

            # Add "+" button to increase the pizza amount in the order
            increase_button = CTkButton(
                master=control_frame,
                text="+",
                font=("Arial", 14),
                fg_color="#1A936F",
                text_color="#fff",
                hover_color="#207244",
                width=30,
                height=30,
                command=lambda pizza_id=pizza.pizza_id: add_pizza_to_current_order(pizza_id)
            )
            increase_button.pack(side="left", padx=(5, 0))

    def create_account_page(self):
        """Create the Account page view."""
        CTkLabel(master=self.main_view, text="Account Page", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)
        CTkLabel(master=self.main_view, text="User account details and settings go here.", font=("Arial", 15)).pack()

    def create_current_order_page(self):
        """Create the Current Order page view."""
        # Clear existing widgets in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        CTkLabel(master=self.main_view, text="Current Order", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)

        # Access the current order from the CurrentOrder singleton
        current_order = CurrentOrder().order

        if current_order and current_order.pizza_orders:  # Assuming pizza_orders is a relationship attribute in Order
            # Create a title for the ordered pizzas
            CTkLabel(master=self.main_view, text="Ordered Pizzas:", font=("Arial", 18, "bold"), text_color="#000").pack(
                pady=(10, 5))

            # Create a scrollable frame for displaying ordered pizzas
            scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
            scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

            # Loop through each pizza in the current order
            for pizza_order in current_order.pizza_orders:
                pizza = session.query(Pizza).filter_by(pizza_id=pizza_order.pizza_id).first()  # Fetch the Pizza object

                if pizza:
                    # Create a frame for each pizza order
                    pizza_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=60, corner_radius=8)
                    pizza_frame.pack(pady=5, padx=10, fill="x")

                    # Create labels for the pizza name and quantity
                    pizza_name_label = CTkLabel(master=pizza_frame, text=pizza.pizza_name, font=("Arial", 16),
                                                text_color="#000")
                    pizza_name_label.pack(anchor="w", padx=(20, 0))

                    quantity_label = CTkLabel(master=pizza_frame, text=f"Quantity: {pizza_order.pizza_amount}",
                                              font=("Arial", 14), text_color="#555")
                    quantity_label.pack(anchor="e", padx=(0, 20))

            # Show the "Place Order" button if the order is not yet placed
            place_order_button = CTkButton(
                master=self.main_view, text="Place Order", font=("Arial", 16, "bold"), fg_color="#2A8C55",
                text_color="#FFF",
                width=200, height=40, command=lambda: self.place_order_and_reload()
            )
            place_order_button.pack(pady=20)

        else:
            # If there are no pizzas in the current order
            CTkLabel(master=self.main_view, text="Add items to place your order.", font=("Arial", 14),
                     text_color="#555").pack(pady=20)

    def place_order_and_reload(self):

        # Place the order
        place_current_order()

        # Flush the current order to be able to make a new one
        create_new_order()

        # Redirect to the orders to see the placed order
        self.show_page("My Orders")

    from datetime import datetime, timedelta

    def create_orders_page(self):
        """Create the My Orders page view."""
        # Clear existing widgets in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="My Orders", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)

        customer_id = CurrentCustomer().customer.customer_id
        orders = session.query(Order).filter_by(customer_id=customer_id).filter(Order.order_status != 'new').order_by(Order.order_timestamp.desc()).all()

        if not orders:
            # If no past orders are found
            CTkLabel(master=self.main_view, text="You have not placed any orders yet.", font=("Arial", 16),
                     text_color="#555").pack(pady=20)
            return

        # Create a scrollable frame for listing all past orders
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Display each order in the scrollable frame
        for order in orders:
            # Check the time difference between now and the order initiation time
            time_since_order = datetime.now() - order.order_timestamp

            # Update order status if more than five minutes have passed and status is still "Placed"
            if order.order_status == "placed" and time_since_order > timedelta(minutes=5):
                order.order_status = "in process"
                session.commit()  # Save changes to the database

            # Create a frame for each order
            order_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=140, corner_radius=8)
            order_frame.pack(pady=5, padx=10, fill="x")

            # Display the order date and ID at the top
            CTkLabel(master=order_frame, text=f"Order Date: {order.order_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                     font=("Arial", 16, "bold"), text_color="#2A8C55").pack(pady=(10, 5), anchor="w", padx=(20, 0))
            CTkLabel(master=order_frame, text=f"Status: {order.order_status}", font=("Arial", 14),
                     text_color="#555").pack(pady=(0, 10), anchor="w", padx=(20, 0))

            # Create a sub-frame for listing all pizzas in the order
            pizza_list_frame = CTkFrame(master=order_frame, fg_color="#f5f5f5", height=60, corner_radius=8)
            pizza_list_frame.pack(pady=5, padx=20, fill="x")

            # Loop through the pizzas in the order and list each one with its quantity
            for pizza_order in order.pizza_orders:
                pizza = session.query(Pizza).filter_by(pizza_id=pizza_order.pizza_id).first()
                if pizza:
                    pizza_details_label = CTkLabel(
                        master=pizza_list_frame,
                        text=f"{pizza.pizza_name} - Quantity: {pizza_order.pizza_amount}",
                        font=("Arial", 14),
                        text_color="#333"
                    )
                    pizza_details_label.pack(anchor="w", pady=(2, 2), padx=(10, 0))

            # Calculate the total price of the order
            total_price = sum(calculate_pizza_price(
                session.query(Pizza).filter_by(pizza_id=pizza_order.pizza_id).first()) * pizza_order.pizza_amount for
                              pizza_order in order.pizza_orders)

            # Display the total price for the order at the bottom of the order frame
            CTkLabel(master=order_frame, text=f"Total Price: {total_price:.2f}€", font=("Arial", 16, "bold"),
                     text_color="#000").pack(pady=(10, 10), anchor="e", padx=(0, 20))

            # Show the "Cancel Order" button if the order was placed within the last 5 minutes and is still "Placed"
            if order.order_status == "placed" and time_since_order <= timedelta(minutes=5):
                cancel_button = CTkButton(
                    master=order_frame, text="Cancel Order", font=("Arial", 14, "bold"),
                    fg_color="#D9534F", text_color="#FFF", width=150, height=30,
                    command=lambda order_id=order.order_id: self.cancel_order(order_id)
                )
                cancel_button.pack(pady=(5, 10), anchor="e", padx=(0, 20))

    def cancel_order(self, order_id):
        """Cancel the order with the given order ID and refresh the page."""
        order_to_cancel = session.query(Order).filter_by(order_id=order_id).first()
        if order_to_cancel:
            session.delete(order_to_cancel)
            session.commit()  # Save the changes to the database
        self.show_page("My Orders")  # Refresh the orders page to reflect changes

    def create_ingredients_page(self):
        """Create the Ingredients page view."""
        # Retrieve all Ingredient objects from the database using the session
        ingredients = session.query(Ingredient).all()

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Ingredients Page", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)

        # Create a scrollable frame for listing ingredients
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Loop through each ingredient and display its name, price, and dietary status
        for idx, ingredient in enumerate(ingredients):
            # Determine the dietary status emoji
            if ingredient.dietary_status == "vegan":
                status_text = "🥦 (vegan)"
            elif ingredient.dietary_status == "vegetarian":
                status_text = "🥕 (vegetarian)"
            else:
                status_text = ""

            # Create a frame for each ingredient
            ingredient_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=80, corner_radius=8)
            ingredient_frame.pack(pady=5, padx=10, fill="x")

            # Create a frame to hold the ingredient name and cost in the same row
            name_price_frame = CTkFrame(master=ingredient_frame, fg_color="#eaeaea")
            name_price_frame.pack(fill="x", pady=(10, 0))

            # Add the Ingredient name label with dietary emoji
            ingredient_name_label = CTkLabel(
                master=name_price_frame,
                text=f"{ingredient.ingredient_name} {status_text}",
                font=("Arial", 16, "bold"),
                text_color="#000"
            )
            ingredient_name_label.pack(anchor="w", side="left", padx=(20, 0))

    def logout(self):
        self.parent.show_frame("LoginFrame")
