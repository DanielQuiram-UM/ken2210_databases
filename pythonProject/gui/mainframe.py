from datetime import timedelta, datetime
from tkinter import Image, TclError

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage

from pythonProject.config import DELIVERY_TIME_IN_MINUTES, ORDER_COMPLETION_TIME
from pythonProject.currentOrder import CurrentOrder
from pythonProject.currentCustomer import CurrentCustomer
from pythonProject.database import session
from pythonProject.main_functions import calculate_pizza_price, add_pizza_to_current_order, place_current_order, \
    remove_pizza_from_current_order, create_new_order, cancel_order, get_customer_from_order
from pythonProject.models import Pizza, Ingredient, Order, Deliverer, Delivery, ExtraItem


#to remind ourselves: self refers to working in the current GUI frame

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.current_page = "Pizzas"

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

        # Add a Refresh Button with the refresh icon
        refresh_icon_data = Image.open("../icons/refresh_icon.png")
        refresh_icon = CTkImage(dark_image=refresh_icon_data, light_image=refresh_icon_data, size=(30, 30))
        refresh_button = CTkButton(
            master=sidebar_frame,
            text="",
            image=refresh_icon,
            command=self.refresh_current_frame,  # Command linked to the refresh function
            text_color="#fff",
            fg_color="#1A936F",
            hover_color="#207244"
        )
        refresh_button.pack(pady=10, padx=10, fill="x")

        # Navigation Buttons on the Sidebar
        navigation_buttons = [
            ("Pizzas", lambda: self.show_page("Pizzas")),
            ("Extra Items", lambda: self.show_page("Extra Items")),
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

        restaurant_monitoring_buttons = [
            ("Current Deliveries", lambda: self.show_page("Deliveries")),
            ("Deliverer Status", lambda: self.show_page("Deliverers")),
            ("Earnings Report", lambda: self.show_page("Earnings"))
        ]

        for text, command in restaurant_monitoring_buttons:
            button = CTkButton(master=sidebar_frame, text=text, command=command, font=("Arial", 16), text_color="#fff",
                               fg_color="#1A936F", hover_color="#207244")
            button.pack(pady=10, padx=10, fill="x")

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
            "Extra Items": self.create_extra_items_page,
            "Current Order": self.create_current_order_page,
            "Account": self.create_account_page,
            "My Orders": self.create_orders_page,
            "Ingredients": self.create_ingredients_page,
            "Deliveries": self.create_deliveries_page,
            "Deliverers": self.create_deliverers_page,
            "Earnings": self.create_earnings_page
        }

        # Display the default page
        self.show_page("Pizzas")

    def show_page(self, page_name):
        """Switch to the selected page within the main view."""
        self.current_page = page_name
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

        # Schedule the layout of pizza details to allow for complete rendering
        self.main_view.after(200, self.layout_pizza_details, pizzas, current_order, scrollable_frame)

    def layout_pizza_details(self, pizzas, current_order, scrollable_frame):
        """Layout pizza details after the main view has been rendered."""
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
            pizza_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", corner_radius=8)
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

            # Display ingredients in a label that can be wrapped
            ingredients_text = ", ".join([ingredient.ingredient_name for ingredient in pizza.ingredients])
            ingredients_label = CTkLabel(master=details_frame, text=f"Ingredients: {ingredients_text}",
                                         font=("Arial", 14), text_color="#555",
                                         wraplength=600)  # Adjust wraplength based on design
            ingredients_label.pack(anchor="w", side="left", padx=(20, 0), fill="x")

            # Create a control frame for the buttons and ensure it's positioned correctly
            control_frame = CTkFrame(master=pizza_frame, fg_color="#eaeaea")
            control_frame.pack(anchor="e", side="bottom", padx=20, pady=(5, 10))  # Always pack at the bottom

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
                command=lambda pizza_id=pizza.pizza_id: self.remove_pizza_from_current_order(pizza_id)
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
                command=lambda pizza_id=pizza.pizza_id: self.add_pizza_to_current_order(pizza_id)
            )
            increase_button.pack(side="left", padx=(5, 0))

    def add_pizza_to_current_order(self,pizza_id):
        add_pizza_to_current_order(pizza_id)
        self.show_page("Current Order")

    def remove_pizza_from_current_order(self,pizza_id):
        remove_pizza_from_current_order(pizza_id)
        self.show_page("Current Order")

    def create_account_page(self):
        """Create the Account page view."""

        # Retrieve the current customer instance
        current_customer = CurrentCustomer().customer

        # Create the main account page structure
        CTkLabel(master=self.main_view, text="Account Page", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)

        # Check if a customer is set in the singleton and display their details
        if current_customer:
            # Display account details
            CTkLabel(master=self.main_view, text=f"First Name: {current_customer.customer_first_name}",
                     font=("Arial", 15)).pack(pady=5)
            CTkLabel(master=self.main_view, text=f"Last Name: {current_customer.customer_last_name}",
                     font=("Arial", 15)).pack(pady=5)
            CTkLabel(master=self.main_view, text=f"Email: {current_customer.customer_email}", font=("Arial", 15)).pack(
                pady=5)
            CTkLabel(master=self.main_view, text=f"Phone Number: {current_customer.phone_number}",
                     font=("Arial", 15)).pack(pady=5)
            CTkLabel(master=self.main_view, text=f"Gender: {current_customer.gender}", font=("Arial", 15)).pack(pady=5)
            CTkLabel(master=self.main_view, text=f"Date of Birth: {current_customer.date_of_birth}",
                     font=("Arial", 15)).pack(pady=5)
            CTkLabel(master=self.main_view,
                     text=f"Discount Available: {'Yes' if current_customer.discount_available else 'No'}",
                     font=("Arial", 15)).pack(pady=5)
        else:
            # No customer set, show a placeholder message
            CTkLabel(master=self.main_view, text="No customer information available.", font=("Arial", 15)).pack(pady=10)

    def create_current_order_page(self):
        """Create the Current Order page view."""
        # Clear existing widgets in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        CTkLabel(master=self.main_view, text="Current Order", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)

        # Access the current order from the CurrentOrder singleton
        current_order = CurrentOrder().order

        # Create a container frame for the scrollable area and the button
        container_frame = CTkFrame(master=self.main_view)
        container_frame.pack(pady=10, padx=10, fill="both", expand=True)

        if current_order and current_order.pizza_orders:  # Assuming pizza_orders is a relationship attribute in Order

            # Create a scrollable frame for displaying ordered pizzas
            scrollable_frame = ctk.CTkScrollableFrame(master=container_frame, fg_color="#f5f5f5", width=660)
            scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

            # Set the maximum height dynamically based on the container frame's height
            self.update_scrollable_frame_height(scrollable_frame)

            # Loop through each pizza in the current order
            for pizza_order in current_order.pizza_orders:
                pizza = session.query(Pizza).filter_by(pizza_id=pizza_order.pizza_id).first()  # Fetch the Pizza object

                if pizza:
                    # Create a frame for each pizza order
                    pizza_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=60, corner_radius=8)
                    pizza_frame.pack(pady=5, padx=10, fill="x")

                    # Create labels for the pizza name
                    pizza_name_label = CTkLabel(master=pizza_frame, text=pizza.pizza_name, font=("Arial", 16),
                                                text_color="#000")
                    pizza_name_label.pack(anchor="w", padx=(20, 0))

                    # Create a frame to hold the quantity label and control buttons
                    quantity_control_frame = CTkFrame(master=pizza_frame, fg_color="#eaeaea")
                    quantity_control_frame.pack(anchor="e", padx=(0, 20))

                    # Display the current quantity of the pizza
                    quantity_label = CTkLabel(master=quantity_control_frame,
                                              text=f"Quantity: {pizza_order.pizza_amount}",
                                              font=("Arial", 14), text_color="#555")
                    quantity_label.pack(side="left")

                    # Create a frame for the control buttons
                    control_frame = CTkFrame(master=quantity_control_frame, fg_color="#eaeaea")
                    control_frame.pack(side="left", padx=(10, 0))

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
                        command=lambda pizza_id=pizza.pizza_id: self.remove_pizza_from_current_order(pizza_id)
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
                        command=lambda pizza_id=pizza.pizza_id: self.add_pizza_to_current_order(pizza_id)
                    )
                    increase_button.pack(side="left", padx=(5, 0))

            # Show the "Place Order" button if the order is not yet placed
            place_order_button = CTkButton(
                master=container_frame, text="Place Order", font=("Arial", 16, "bold"), fg_color="#1A936F",
                text_color="#FFF",
                width=200, height=40, command=lambda: self.place_order_and_reload()
            )
            place_order_button.pack(pady=20)

        else:
            # If there are no pizzas in the current order
            CTkLabel(master=container_frame, text="Add items to place your order.", font=("Arial", 14),
                     text_color="#555").pack(pady=20)

    def update_scrollable_frame_height(self, scrollable_frame):
        """Update the height of the scrollable frame based on the container frame's height."""
        # Check if the scrollable_frame and its master exist
        if scrollable_frame and scrollable_frame.master:
            try:
                # Get the height of the container frame
                container_height = scrollable_frame.master.winfo_height()
                max_height = container_height * 0.8  # Set to 80% of the container frame height
                scrollable_frame.configure(height=max_height)

            except TclError as e:
                print(f"Error updating scrollable frame height: {e}")

            # Optionally, bind the resize event to update the height dynamically
            self.main_view.bind("<Configure>", lambda e: self.update_scrollable_frame_height(scrollable_frame))

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
            minutes_since_order = time_since_order.total_seconds() / 60

            # adding one minute to make it more realistic
            remaining_minutes = ORDER_COMPLETION_TIME - minutes_since_order + 1

            # Create a frame for each order
            order_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=140, corner_radius=8)
            order_frame.pack(pady=5, padx=10, fill="x")

            # Display the order date and ID at the top
            CTkLabel(master=order_frame, text=f"Order Date: {order.order_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                     font=("Arial", 16, "bold"), text_color="#2A8C55").pack(pady=(10, 5), anchor="w", padx=(20, 0))
            CTkLabel(master=order_frame, text=f"Status: {order.order_status}", font=("Arial", 14),
                     text_color="#555").pack(pady=(0, 10), anchor="w", padx=(20, 0))
            if(order.order_status != "completed"):
                CTkLabel(master=order_frame,
                         text=f"Estimated Delivery Time: ~{int(remaining_minutes)} minutes remaining",
                         font=("Arial", 14), text_color="#555").pack(pady=(0, 15), anchor="w", padx=(20, 0))

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
        cancel_order(order_id)
        self.show_page("My Orders")  # Refreshes the orders page to reflect changes

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

    def create_deliveries_page(self):
        """Create the Orders and Active Deliveries page view."""
        # Clear existing widgets in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Orders and Active Deliveries", font=("Arial Black", 25),
                 text_color="#2A8C55").pack(pady=20)

        # Create a scrollable frame for listing all orders and deliveries
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Query for orders with status 'in process'
        orders = session.query(Order).filter_by(order_status='in process').order_by(Order.order_timestamp.asc()).all()

        # Display Orders to be delivered
        if orders:
            CTkLabel(master=scrollable_frame, text="Orders to be Delivered:", font=("Arial", 18, "bold"),
                     text_color="#333").pack(pady=10, anchor="w", padx=(20, 0))

            for order in orders:
                # Create a frame for each order
                order_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=140, corner_radius=8)
                order_frame.pack(pady=5, padx=10, fill="x")

                # Retrieve the customer information using the get_customer_from_order function
                customer = get_customer_from_order(order)

                # Calculate time since order was placed
                time_since_order = datetime.now() - order.order_timestamp
                minutes_since_order = time_since_order.total_seconds() // 60

                # Create a display message for how long ago the order was placed
                if minutes_since_order > 120:
                    time_message = ">2 hours ago"
                else:
                    time_message = f"{int(minutes_since_order)} minutes ago"

                # Display the customer name, postal address, and order date at the top
                CTkLabel(master=order_frame,
                         text=f"Customer: {customer.customer_first_name} {customer.customer_last_name} - Address: {customer.address.postal_code}",
                         font=("Arial", 16, "bold"), text_color="#2A8C55").pack(pady=(10, 5), anchor="w", padx=(20, 0))
                CTkLabel(master=order_frame,
                         text=f"Order Date: {order.order_timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({time_message})",
                         font=("Arial", 14), text_color="#555").pack(pady=(0, 10), anchor="w", padx=(20, 0))

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

        else:
            # If no orders are in process
            CTkLabel(master=scrollable_frame, text="No orders to be delivered at the moment.", font=("Arial", 16),
                     text_color="#555").pack(pady=20)

        # Query for active deliveries (orders with status 'being delivered') initiated within the last X minutes
        delivery_completion_time = datetime.now() - timedelta(minutes=DELIVERY_TIME_IN_MINUTES)

        deliveries = session.query(Delivery).filter(Delivery.initiation_time >= delivery_completion_time).all()

        if deliveries:
            CTkLabel(master=scrollable_frame, text="Active Deliveries:", font=("Arial", 18, "bold"),
                     text_color="#333").pack(pady=20, anchor="w", padx=(20, 0))

            for delivery in deliveries:
                delivery_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=160, corner_radius=8)
                delivery_frame.pack(pady=5, padx=10, fill="x")

                # Retrieve the deliverer information
                deliverer = delivery.deliverer
                delivery_time = datetime.now() - delivery.initiation_time
                minutes_since_start = delivery_time.total_seconds() // 60

                # Retrieve the orders in the delivery
                delivery_orders = session.query(Order).filter_by(delivery_id=delivery.delivery_id).all()

                # Display the deliverer and time since delivery started
                CTkLabel(master=delivery_frame,
                         text=f"Deliverer: {deliverer.deliverer_first_name} {deliverer.deliverer_last_name} - Started {int(minutes_since_start)} minutes ago",
                         font=("Arial", 16, "bold"), text_color="#2A8C55").pack(pady=(10, 5), anchor="w", padx=(20, 0))

                # Display each order associated with the delivery
                for order in delivery_orders:
                    # Retrieve customer details
                    customer = get_customer_from_order(order)
                    CTkLabel(master=delivery_frame,
                             text=f"Order for {customer.customer_first_name} {customer.customer_last_name} - {customer.address.postal_code}",
                             font=("Arial", 14), text_color="#333").pack(pady=(2, 2), anchor="w", padx=(20, 0))

        else:
            # If no deliveries are active
            CTkLabel(master=scrollable_frame, text="No active deliveries at the moment.", font=("Arial", 16),
                     text_color="#555").pack(pady=20)

    def create_deliverers_page(self):
        """Create the Deliverers page view."""
        # Clear existing widgets in the main view
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Deliverers List", font=("Arial Black", 25), text_color="#2A8C55").pack(
            pady=20)

        # Query for all deliverer instances in the database
        deliverers = session.query(Deliverer).all()

        if not deliverers:
            # If no deliverers exist in the database
            CTkLabel(master=self.main_view, text="No deliverers found.", font=("Arial", 16), text_color="#555").pack(
                pady=20)
            return

        # Create a scrollable frame for listing all deliverers
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Display each deliverer in the scrollable frame
        for deliverer in deliverers:
            # Create a frame for each deliverer
            deliverer_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", height=50, corner_radius=8)
            deliverer_frame.pack(pady=5, padx=10, fill="x")

            # Create sub-frames for layout control (name on left, postal code/status on right)
            info_frame = CTkFrame(master=deliverer_frame, fg_color="#eaeaea")
            info_frame.pack(fill="both", expand=True, padx=20, pady=10)

            # Display the deliverer's full name on the left
            CTkLabel(master=info_frame,
                     text=f"{deliverer.deliverer_first_name} {deliverer.deliverer_last_name}",
                     font=("Arial", 16, "bold"), text_color="black").pack(side="left", anchor="w")

            # Check if the deliverer is currently assigned to a delivery
            if not deliverer.postal_code:
                # Display 'Available' in green text if no postal code is assigned
                CTkLabel(master=info_frame,
                         text="Available",
                         font=("Arial", 16), text_color="#2A8C55").pack(side="right", anchor="e")
            else:
                # Display the postal code in black text if assigned
                CTkLabel(master=info_frame,
                         text=f"Postal Code: {deliverer.postal_code}",
                         font=("Arial", 16), text_color="black").pack(side="right", anchor="e")

                # Check if the deliverer is on an active delivery
                active_delivery = session.query(Delivery).filter_by(deliverer_id=deliverer.deliverer_id).first()
                if active_delivery:
                    # Calculate the time since the delivery was initiated
                    time_since_delivery = datetime.now() - active_delivery.initiation_time
                    minutes_since_delivery = time_since_delivery.total_seconds() // 60

                    # Calculate remaining time for the delivery (30 minutes total)
                    remaining_time = DELIVERY_TIME_IN_MINUTES - minutes_since_delivery

                    if remaining_time > 0:
                        # Display remaining time
                        CTkLabel(master=info_frame,
                                 text=f"Away for: {int(remaining_time)} minutes",
                                 font=("Arial", 16), text_color="#FF4500").pack(side="right", anchor="e")
                    else:
                        # If time is up, show delivery complete message
                        CTkLabel(master=info_frame,
                                 text="Delivery Complete",
                                 font=("Arial", 16), text_color="#2A8C55").pack(side="right", anchor="e")

    def create_earnings_page(self):
        pass

    def logout(self):
        self.parent.show_frame("LoginFrame")

    def refresh_current_frame(self):
        """Refresh the current frame by committing the session and reloading the page."""
        session.commit()  # Commit any pending transactions to the database
        self.show_page(self.current_page)

#TODO: display dietary status underneath each pizza --> Daniel

    def create_extra_items_page(self):
        """Create the Extra Items page view."""
        # Retrieve all extra item objects from the database using the session.
        extra_items = session.query(ExtraItem).all()

        # Retrieve the current order instance
        current_order = CurrentOrder().order

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Our Extra Items", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)

        # Create a container frame for displaying the extra item details in a grid format
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Schedule the layout of extra item details to allow for complete rendering
        self.main_view.after(200, self.layout_extra_item_details, extra_items, current_order, scrollable_frame)

    def layout_extra_item_details(self, extra_items, current_order, scrollable_frame):
        """Layout extra item details after the main view has been rendered."""
        # Loop through each extra item and display its name, dietary status and the amount controls
        for item in extra_items:
            # Show the total price of the extra item
            item_price = item.cost

            #Show the dietary status of the extra item
            dietary_status = item.dietary_status
            #TODO: make sure it shows up in the GUI!
            # Check the current amount of this extra item in the order, if it exists
            item_amount = 0
            if current_order and current_order.extra_item_orders:
                for extra_item_order in current_order.extra_item_orders:
                    if extra_item_order.item_id == item.item_id:
                        item_amount = extra_item_order.item_amount
                        break

            # Create a frame for each pizza
            extra_item_frame = CTkFrame(master=scrollable_frame, fg_color="#eaeaea", corner_radius=8)
            extra_item_frame.pack(pady=5, padx=10, fill="x")

            # Create a frame to hold the extra item name and price in the same row
            name_price_frame = CTkFrame(master=extra_item_frame, fg_color="#eaeaea")
            name_price_frame.pack(fill="x", pady=(10, 0))

            # Add the extra item name label on the left within name_price_frame
            extra_item_name_label = CTkLabel(master=name_price_frame, text=item.item_name,
                                            font=("Arial", 16, "bold"),
                                            text_color="#000")
            extra_item_name_label.pack(anchor="w", side="left", padx=(20, 0))

            # Add the extra item price label on the right within name_price_frame
            price_label = CTkLabel(master=name_price_frame, text=f"{item_price:.2f}€",
                                    font=("Arial", 16, "bold"),
                                    text_color="#000")
            price_label.pack(anchor="e", side="right", padx=(10, 20))

            # Create a new frame to hold the amount controls
            details_frame = CTkFrame(master=extra_item_frame, fg_color="#eaeaea")
            details_frame.pack(fill="x", pady=(5, 10))

            # Create a control frame for the buttons and ensure it's positioned correctly
            control_frame = CTkFrame(master=extra_item_frame, fg_color="#eaeaea")
            control_frame.pack(anchor="e", side="bottom", padx=20,
                                 pady=(5, 10))  # Always pack at the bottom

            # Add "-" (=minus) button to decrease the extra item amount in the order
            decrease_button = CTkButton(
                master=control_frame,
                text="-",
                font=("Arial", 14),
                fg_color="#1A936F",
                text_color="#fff",
                hover_color="#207244",
                width=30,
                height=30,
                command=lambda item_id=item.item_id: self.remove_extra_item_from_current_order(item_id)
                )
            decrease_button.pack(side="left", padx=(0, 5))

            # Add "+" button to increase the extra item amount in the order
            increase_button = CTkButton(
                master=control_frame,
                text="+",
                font=("Arial", 14),
                fg_color="#1A936F",
                text_color="#fff",
                hover_color="#207244",
                width=30,
                height=30,
                command=lambda item_id=item.item_id: self.add_extra_item_to_current_order(item_id)
                )
            increase_button.pack(side="left", padx=(5, 0))

#TODO: continue shopping button after adding a pizza / extra item --> Merel

#TODO: add estimated delivery time to order confirmation --> Daniel

#TODO: tracking the status of the delivery

#TODO: earnings page solely visible for the boss of the pizza place

#TODO: monitoring: provide a real-time display for the restaurant staff, showing a list of pizzas that have been ordered but not yet dispatched for delivery --> Daniel