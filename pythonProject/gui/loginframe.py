import customtkinter as ctk
import tkinter
from tkinter import messagebox
import bcrypt
from pythonProject.models import Customer
from pythonProject.database import session


# Frame for the login page
class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.configure(width=800, height=600)

        # Create a label for the header
        label_header = ctk.CTkLabel(self, text="Pizza Delivery System", text_color="Blue", font=("Arial", 24))
        label_header.grid(row=0, column=0, pady=(20, 10))

        # Create login form elements
        label_email = ctk.CTkLabel(self, text="Email")
        label_email.grid(row=1, column=0, pady=5)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Enter email...")
        self.entry_email.grid(row=2, column=0, pady=5)

        label_password = ctk.CTkLabel(self, text="Password")
        label_password.grid(row=3, column=0, pady=5)

        self.entry_password = ctk.CTkEntry(self, show="*", placeholder_text="Enter password...")
        self.entry_password.grid(row=4, column=0, pady=5)

        # Login button
        button_login = ctk.CTkButton(self, text="Login", command=self.login_customer)
        button_login.grid(row=5, column=0, pady=10)

        button_register = ctk.CTkButton(self, text="Register", command=self.display_registration_form)
        button_register.grid(row=6, column=0, pady=10)

        # Center the frame elements within the parent frame
        self.grid_rowconfigure(0, weight=1)  # Header
        self.grid_rowconfigure(6, weight=1)  # Buttons
        self.grid_columnconfigure(0, weight=1)  # Center column

    def login_customer(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        customer = session.query(Customer).filter_by(customer_email=email).first()
        if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf-8')):
            self.parent.show_frame("MainFrame")
        else:
            messagebox.showerror("Login", "Incorrect email or password.")

    def display_registration_form(self):
        self.parent.show_frame("RegistrationFrame")
