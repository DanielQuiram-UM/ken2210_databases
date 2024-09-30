import tkinter
from tkinter import messagebox
import bcrypt
import customtkinter as ctk
from tkcalendar import DateEntry

from pythonProject.models import Customer, Customer_Address
from pythonProject.database import session
from datetime import datetime


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_registration_form()

        self.configure(width=800, height=600)

    from tkcalendar import DateEntry

    def create_registration_form(self):
        # Create a header label
        label_header = ctk.CTkLabel(self, text="Register as new account", text_color="Blue", font=("Arial", 24))
        label_header.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Define the labels for the form
        labels = [
            "First Name", "Last Name", "Email", "Password", "Gender",
            "Date of Birth", "Phone Number", "Street", "City", "Country", "Postal Code"
        ]

        # Store entry fields in a dictionary for easy access
        self.entry_fields = {}

        # Create labels and entry fields dynamically
        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text)
            label.grid(row=i + 1, column=0, pady=5, sticky="w")

            if label_text == "Gender":
                self.gender_var = ctk.StringVar()
                gender_dropdown = ctk.CTkOptionMenu(self, variable=self.gender_var, values=["Male", "Female", "Other"])
                gender_dropdown.grid(row=i + 1, column=1, padx=10, pady=5)
                continue

            if label_text == "Date of Birth":
                # Use DateEntry for Date of Birth
                date_entry = DateEntry(self, date_pattern='y-mm-dd')  # You can customize the date format
                date_entry.grid(row=i + 1, column=1, padx=10, pady=5)
                self.entry_fields["date_of_birth"] = date_entry
                continue

            entry = ctk.CTkEntry(self)
            if label_text == "Password":
                entry.configure(show="*")
            self.entry_fields[label_text.replace(" ", "_").lower()] = entry

            entry.grid(row=i + 1, column=1, padx=10, pady=5)

        # Register button to submit the form
        button_submit = ctk.CTkButton(self, text="Submit", command=self.submit_registration_form)
        button_submit.grid(row=len(labels) + 1, column=0, columnspan=2, pady=(10, 5))

        # Button to go back to the login form
        button_back = ctk.CTkButton(self, text="Back to Login", command=self.display_login_form)
        button_back.grid(row=len(labels) + 2, column=0, columnspan=2, pady=5)

        # Center the frame in the window
        self.grid_rowconfigure(len(labels) + 3, weight=1)  # Allow space at the bottom for centering

    def submit_registration_form(self):
        # Gather and process the registration data
        first_name = self.entry_fields['first_name'].get()
        last_name = self.entry_fields['last_name'].get()
        email = self.entry_fields['email'].get()
        password = self.entry_fields['password'].get()
        gender = self.gender_var.get()  # Get gender from the dropdown
        dob = datetime.strptime(self.entry_fields['date_of_birth'].get(),
                                "%Y-%m-%d").date() if 'date_of_birth' in self.entry_fields else None
        # Dummy until this is a field only with integers
        phone = self.entry_fields['phone_number'].get() if 'phone_number' in self.entry_fields else None
        street = self.entry_fields['street'].get() if 'street' in self.entry_fields else None
        city = self.entry_fields['city'].get() if 'city' in self.entry_fields else None
        country = self.entry_fields['country'].get() if 'country' in self.entry_fields else None
        postal_code = self.entry_fields['postal_code'].get() if 'postal_code' in self.entry_fields else None

        # Register new customer
        self.register_customer(first_name, last_name, email, password, gender, dob, phone, street, city, country, postal_code)
        messagebox.showinfo("Registration", "Registration Successful!")
        self.display_login_form()

    #TODO: Add Address accordingly
    def register_customer(self, first_name, last_name, email, password, gender, dob, phone, street, city, country, postal_code):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_customer = Customer(
            customer_first_name=first_name,
            customer_last_name=last_name,
            customer_email=email,
            password=hashed_password.decode('utf-8'),
            gender=gender,
            date_of_birth=dob,
            phone_number=phone,
        )
        new_address = Customer_Address(
            street=street,
            city=city,
            country=country,
            postal_code=postal_code
        )
        new_customer.address = new_address
        session.add(new_customer)
        session.commit()

    def display_login_form(self):
        self.parent.show_frame("LoginFrame")
