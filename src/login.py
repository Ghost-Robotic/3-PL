import customtkinter as ctk
from PIL import Image
import style

# initial landing page where users are directed to login
class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#2b2b2b") 
        
        def show_error():
            self.error_label.grid()
            
        def hide_error():
            self.error_label.grid_remove()
            
        def help():
            if self.help_label.winfo_viewable():
                self.help_label.grid_remove()
            else:
                self.help_label.grid()       
        
        # logo above login box
        dark_logo = Image.open("assets\\3-PL.png")
        self.logo = ctk.CTkImage(dark_image=dark_logo, size=(dark_logo.width/3,dark_logo.height/3))      
        logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        logo_label.grid(row=0, column=0)
        
        
        # login Box: cosmetic container that holds login widgets
        bg_frame = ctk.CTkFrame(self, fg_color="#05ac71", corner_radius=40, border_width=7, border_color="#262626", bg_color="#2b2b2b")
        bg_frame.grid(row=1, column=0, ipadx=30, ipady=30)
        bg_frame.rowconfigure(0, weight=1)
        bg_frame.columnconfigure(0, weight=1)
        #bg_frame.grid_propagate(False)
        
        # container inside login box that holds content, used to prevent widgets overlapping corners of login box
        login_cont = ctk.CTkFrame(bg_frame, width=300, fg_color="#05ac71", corner_radius=-1)
        login_cont.grid(row=0, column=0)
        login_cont.rowconfigure(0, weight=1)
        login_cont.columnconfigure(0, weight=1)
        # login_cont.place(in_=bg_frame, anchor = "n", relx=.5, rely=.1)
        # login_cont.grid_propagate(False)
        
        # welcome text
        welcome_label = ctk.CTkLabel(login_cont, text="Welcome", font=("Segoe UI Black",30), text_color="#31acf3")
        info_label = ctk.CTkLabel(login_cont, text="Enter your organisation's login details below", font=("Segoe UI",20, "bold"), wraplength=300)
        welcome_label.grid(row=0, column=0, columnspan=2)
        info_label.grid(row=1, column=0, columnspan=2)

        # username entry
        user_label = ctk.CTkLabel(login_cont, text="Username:", font=("Segoe UI Black",25))
        user_label.grid(row=2, column = 0, padx=5, pady=10)
        self.username = ctk.CTkEntry(login_cont, width=180, height=25, placeholder_text="ID number", font=("Segoe UI Black",18))
        self.username.grid(row=2, column=1, padx=5, pady=23)
        self.after(1, self.username.focus())
        
        # password entry
        pass_label = ctk.CTkLabel(login_cont, text="Password:", font=("Segoe UI Black",25))
        pass_label.grid(row=3, column = 0, padx=5, pady=10)
        self.password = ctk.CTkEntry(login_cont, width=180, height=25, show="•", placeholder_text="Password", font=("Segoe UI Black",18))
        self.password.grid(row=3, column=1, padx=5, pady=(23, 10))
        
        # error message
        self.error_label = ctk.CTkLabel(login_cont, text="*Invalid username or password", font=(style.bold_font, 16), text_color="#ff0000")
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(0, 5))
        self.error_label.grid_remove()
        
        command = lambda : show_error()
        command2 = lambda : hide_error()
        
        # submit button
        self.login_button =ctk.CTkButton(login_cont, command=command, width=100, height=40, text="Login", font=("Segoe UI Black", 25), fg_color="#00a2ff")
        self.login_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # help button
        help_command = lambda : help()
        help_button = ctk.CTkButton(login_cont, command=help_command, 
                                    width=30, height=30, corner_radius=15, 
                                    text="?", font=("Segoe UI Black", 20), text_color="black", 
                                    fg_color="#ffffff", hover_color="#d4d4d4")
        help_button.grid(row=5, column=1, sticky="e")
        
        # help message
        self.help_label = ctk.CTkLabel(login_cont, text="All login information is managed by your organisation's admin, \nplease see them for any assistance required",
                                  font=(style.normal_font, 16), text_color="#ececec", wraplength=300)
        self.help_label.grid(row=6, column=0, columnspan=2)
        self.help_label.grid_remove()
    
   