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
        self.configure(width=800, height=600)

        header_frame = ctk.CTkFrame(self, fg_color="#1A936F", width=800, height=200)
        header_frame.pack(side=tkinter.TOP, fill=tkinter.X)

        label_header = ctk.CTkLabel(header_frame, text="Pizza Delivery System", text_color="white",
                                    font=("Arial", 36, "bold"))
        label_header.pack(side=tkinter.TOP, pady=50)

        form_frame = ctk.CTkFrame(self, fg_color="#f5f5f5", width=600)
        form_frame.pack(side=tkinter.TOP, pady=(20, 10), padx=20)
        form_frame.pack_propagate(False)

        labels = [
            "First Name", "Last Name", "Email", "Password", "Gender",
            "Date of Birth", "Phone Number", "Street", "City", "Country", "Postal Code"
        ]

        self.entry_fields = {}
        self.gender_var = ctk.StringVar(value="")

        for i, label_text in enumerate(labels):
            # Create and place label
            label = ctk.CTkLabel(form_frame, text=f"{label_text} *", font=("Arial", 14))
            label.grid(row=i, column=0, padx=10, pady=5)  # Align labels to the right

            # Create and place entry fields or dropdowns
            if label_text == "Gender":
                gender_dropdown = ctk.CTkOptionMenu(form_frame, variable=self.gender_var,
                                                    values=["Male", "Female", "Other"])
                gender_dropdown.grid(row=i, column=1, padx=10, pady=5)  # Expand dropdown
                continue

            if label_text == "Date of Birth":
                date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
                date_entry.grid(row=i, column=1, padx=10, pady=5)  # Expand date entry
                self.entry_fields["date_of_birth"] = date_entry
                continue

            entry = ctk.CTkEntry(form_frame)
            if label_text == "Password":
                entry.configure(show="*")
            self.entry_fields[label_text.replace(" ", "_").lower()] = entry
            entry.grid(row=i, column=1, padx=10, pady=5)  # Expand entry fields

        # Submit button
        button_submit = ctk.CTkButton(form_frame, text="Submit", command=self.submit_registration_form,
                                      fg_color="#1A936F", width=250)
        button_submit.grid(row=len(labels), column=0, columnspan=2, pady=(20, 5))  # Span both columns

        # Back to Login button
        button_back = ctk.CTkButton(form_frame, text="Back to Login", command=self.display_login_form,
                                    fg_color="#1A936F", width=250)
        button_back.grid(row=len(labels) + 1, column=0, columnspan=2, pady=(0, 20))  # Span both columns

        # Configure grid weights for better resizing
        form_frame.columnconfigure(0, weight=1)  # Allow column 0 to expand
        form_frame.columnconfigure(1, weight=2)  # Allow column 1 to expand more than column 0

        # Center the whole form vertically
        form_frame.rowconfigure(len(labels), weight=1)  # Allow the space before the buttons to expand
        form_frame.rowconfigure(len(labels) + 1, weight=1)  # Allow the space after the buttons to expand

    def submit_registration_form(self):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'gender', 'date_of_birth', 'phone_number',
                           'street', 'city', 'country', 'postal_code']
        for field in required_fields:
            if field == 'gender':
                if not self.gender_var.get():
                    messagebox.showerror("Registration Error", "Gender is required.")
                    return
            else:
                if not self.entry_fields.get(field, None) or self.entry_fields[field].get() == "":
                    messagebox.showerror("Registration Error", f"{field.replace('_', ' ').title()} is required.")
                    return

        first_name = self.entry_fields['first_name'].get()
        last_name = self.entry_fields['last_name'].get()
        email = self.entry_fields['email'].get()
        password = self.entry_fields['password'].get()
        gender = self.gender_var.get()
        dob = datetime.strptime(self.entry_fields['date_of_birth'].get(),
                                "%Y-%m-%d").date() if 'date_of_birth' in self.entry_fields else None
        phone = self.entry_fields['phone_number'].get()
        street = self.entry_fields['street'].get()
        city = self.entry_fields['city'].get()
        country = self.entry_fields['country'].get()
        postal_code = self.entry_fields['postal_code'].get()

        self.register_customer(first_name, last_name, email, password, gender, dob, phone, street, city, country,
                               postal_code)
        messagebox.showinfo("Registration", "Registration Successful!")
        self.display_login_form()

#TODO: we already have this function in the main_functions file so remove it in one place?
    def register_customer(self, first_name, last_name, email, password, gender, dob, phone, street, city, country,
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
