import customtkinter as ctk

# main page that allows users to access sub-pages that contain main app functions

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#2b2b2b")