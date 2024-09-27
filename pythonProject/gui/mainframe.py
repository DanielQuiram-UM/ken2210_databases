from tkinter import Image

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage

from pythonProject.database import session
from pythonProject.main_functions import calculate_pizza_price
from pythonProject.models import Pizza, Ingredient


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

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(10, 0), anchor="center")


        # Navigation Buttons on the Sidebar
        navigation_buttons = [
            ("Pizzas", lambda: self.show_page("Pizzas")),
            ("Ingredients", lambda: self.show_page("Ingredients")),
            ("My Orders", lambda: self.show_page("My Orders")),
            ("Account", lambda: self.show_page("Account")),
            ("Logout", lambda: self.logout()),


        ]

        # Create each button in the sidebar
        for text, command in navigation_buttons:
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

        # Create a title label for the page
        CTkLabel(master=self.main_view, text="Our Pizzas", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)

        # Create a container frame for displaying the pizza details in a grid format
        scrollable_frame = ctk.CTkScrollableFrame(master=self.main_view, fg_color="#f5f5f5", width=660, height=520)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Loop through each pizza and display its name, ingredients, and a "Add to Order" button
        for pizza in pizzas:
            # Calculate the total price of the pizza based on its ingredients
            total_price = calculate_pizza_price(pizza)

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

            # Create a new frame to hold ingredients and the "Add to Order" button in the same row
            details_frame = CTkFrame(master=pizza_frame, fg_color="#eaeaea")
            details_frame.pack(fill="x", pady=(5, 10))

            # Display ingredients on the left inside details_frame
            ingredients_text = ", ".join([ingredient.ingredient_name for ingredient in pizza.ingredients])
            ingredients_label = CTkLabel(master=details_frame, text=f"Ingredients: {ingredients_text}",
                                         font=("Arial", 14), text_color="#555")
            ingredients_label.pack(anchor="w", side="left", padx=(20, 0))

            # Add the "Add to Order" button on the right inside details_frame
            add_button = CTkButton(
                master=details_frame,
                text="Add to Order",
                font=("Arial", 14),
                fg_color="#1A936F",
                text_color="#fff",
                hover_color="#207244"
            )
            add_button.pack(anchor="e", side="right", padx=20)

    def create_account_page(self):
        """Create the Account page view."""
        CTkLabel(master=self.main_view, text="Account Page", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)
        CTkLabel(master=self.main_view, text="User account details and settings go here.", font=("Arial", 15)).pack()

    def create_orders_page(self):
        """Create the My Orders page view."""
        CTkLabel(master=self.main_view, text="My Orders Page", font=("Arial Black", 25), text_color="#2A8C55").pack(pady=20)
        CTkLabel(master=self.main_view, text="Order history and status go here.", font=("Arial", 15)).pack()

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