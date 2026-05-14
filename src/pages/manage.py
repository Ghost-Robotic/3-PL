import customtkinter as ctk
import src.style as style

class Manage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="pink")