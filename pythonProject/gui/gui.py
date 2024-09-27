import customtkinter as ctk
from pythonProject.gui.loginframe import LoginFrame
from pythonProject.gui.registrationframe import RegistrationFrame
from pythonProject.gui.mainframe import MainFrame

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
            frame.grid(row=0, column=0, sticky="nsew")  # Use grid for layout control

        # Configure grid weights to allow frames to expand appropriately
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

    app = Application()
    app.mainloop()
