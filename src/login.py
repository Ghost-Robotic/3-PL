import customtkinter as ctk
from PIL import Image


class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#2b2b2b")
        
        #Title
        # title = ctk.CTkFrame(self, bg_color="transparent")
        # title.grid(row=0, column=0)
        # three = ctk.CTkLabel(title, text="3", font=("Segoe UI Black",30), text_color="#00a2ff", bg_color="#2b2b2b", padx=5, pady=5)
        # three.grid(row=0, column=0)
        # pl = ctk.CTkLabel(title, text="-PL", font=("Segoe UI Black",30), text_color="#ffffff", bg_color="#2b2b2b", padx=5, pady=5)
        # pl.grid(row=0, column=1)
        
        
        dark_logo = Image.open("assets\\3-PL.png")
        self.logo = ctk.CTkImage(dark_image=dark_logo, size=(dark_logo.width/3,dark_logo.height/3))      
        logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        logo_label.grid(row=0, column=0)
        
        #Login Box
        bg_frame = ctk.CTkFrame(self, width=400, height=400, fg_color="#35c191", corner_radius=40, border_width=7, border_color="#262626", bg_color="#2b2b2b")
        bg_frame.grid(row=1, column=0)
        bg_frame.grid_propagate(False)
        
        login_cont = ctk.CTkFrame(self, width=300, height=300, fg_color="#35c191", corner_radius=-1)
        login_cont.place(in_=bg_frame, anchor = "c", relx=.5, rely=.5)
        login_cont.grid_propagate(False)

        user_label = ctk.CTkLabel(login_cont, text="Username:", font=("Segoe UI Black",20))
        user_label.grid(row=0, column = 0, padx=5, pady=10)
        username = ctk.CTkEntry(login_cont, width=180, height=25)
        username.grid(row=0, column=1, padx=5, pady=23)
        
        pass_label = ctk.CTkLabel(login_cont, text="Password:", font=("Segoe UI Black",20))
        pass_label.grid(row=1, column = 0, padx=5, pady=10)
        password = ctk.CTkEntry(login_cont, width=180, height=25, show="•")
        password.grid(row=1, column=1, padx=5, pady=23)