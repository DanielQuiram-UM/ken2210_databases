import customtkinter as ctk
import tkinter
from tkinter import messagebox
import bcrypt

from pythonProject.currentCustomer import CurrentCustomer
from pythonProject.models import Customer
from pythonProject.database import session


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.configure(width=800, height=600)

        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color="#1A936F", width=800, height=200)
        header_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        # Header label
        label_header = ctk.CTkLabel(header_frame, text="Pizza Delivery System", text_color="white", font=("Arial", 36, "bold"))
        label_header.pack(side=tkinter.TOP, pady=50)

        # Create a container frame for inputs and buttons
        form_frame = ctk.CTkFrame(self, width=400, height=300, fg_color="#f5f5f5")
        form_frame.pack(side=tkinter.TOP, pady=50)  # Add some padding to space from header

        # Email label and entry field
        label_email = ctk.CTkLabel(form_frame, text="Email", font=("Arial", 14))
        label_email.pack(anchor="w", padx=20, pady=(20, 5))

        self.entry_email = ctk.CTkEntry(form_frame, placeholder_text="Enter email...", width=250)
        self.entry_email.pack(padx=20, pady=5)

        # Password label and entry field
        label_password = ctk.CTkLabel(form_frame, text="Password", font=("Arial", 14))
        label_password.pack(anchor="w", padx=20, pady=(20, 5))

        self.entry_password = ctk.CTkEntry(form_frame, show="*", placeholder_text="Enter password...", width=250)
        self.entry_password.pack(padx=20, pady=5)

        # Login button
        button_login = ctk.CTkButton(form_frame, text="Login", command=self.login_customer, fg_color="#1A936F", width=250)
        button_login.pack(pady=(20, 10), padx=20)

        # Register button
        button_register = ctk.CTkButton(form_frame, text="Register", command=self.display_registration_form, fg_color="#1A936F", width=250)
        button_register.pack(pady=(10, 20), padx=20)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def login_customer(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        customer = session.query(Customer).filter_by(customer_email=email).first()
        if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf-8')):
            current_customer = CurrentCustomer()
            current_customer.set_customer(customer)
            self.parent.show_frame("MainFrame")
        else:
            messagebox.showerror("Login", "Incorrect email or password.")


    def display_registration_form(self):
        self.parent.show_frame("RegistrationFrame")
