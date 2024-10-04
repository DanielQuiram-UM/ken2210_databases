import time
import customtkinter as ctk
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pythonProject.config import DATABASE_URL
from pythonProject.gui.loginframe import LoginFrame
from pythonProject.gui.registrationframe import RegistrationFrame
from pythonProject.gui.mainframe import MainFrame

# Establish the database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pizza Delivery System")
        self.geometry("800x600")

        # Initialize frames
        self.frames = {
            "LoginFrame": LoginFrame(parent=self),
            "RegistrationFrame": RegistrationFrame(parent=self),
            "MainFrame": MainFrame(parent=self)
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Show the login frame initially
        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        """Bring the specified frame to the front using the frame name."""
        frame = self.frames[frame_name]
        frame.tkraise()  # Bring the frame to the front

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Start the GUI application
    app = Application()
    app.mainloop()
