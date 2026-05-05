import customtkinter as ctk
from PIL import Image, ImageTk
import style
import random
# initial landing page where users are directed to login
class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_background) 
        self.images = ["assets/c-1L-dark2.png", "assets/c1-indx.png", "assets/h2d.png", "assets/ht90-dark.png", 
                       "assets/P1S.png", "assets/xl.png", "assets/xl2.png", "assets/xl5-transp.png"]
        
        def show_error():
            self.error_label.grid()
            
        def hide_error():
            self.error_label.grid_remove()
            
        def help():
            if self.help_label.winfo_viewable():
                self.help_label.grid_remove()
            else:
                self.help_label.grid()   
                
            
        container = ctk.CTkFrame(self, fg_color=style.dark_background)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        img_container = ctk.CTkFrame(container)
        img_container.grid(row=0, column=0, sticky="nsew")
        img_container.columnconfigure(0, weight=1)
        img_container.rowconfigure(0, weight=1)
        img = ImageTk.PhotoImage((Image.open(self.random_img())).resize((700,700), Image.LANCZOS))
        self.img_label = ctk.CTkButton(img_container, image=img, command=self.change_img, text="", hover=False, fg_color=style.dark_background)
        self.img_label.grid(row=0, column=0)
        
        # 
        bg_frame = ctk.CTkFrame(container, fg_color=style.grey, corner_radius=30)
        bg_frame.grid(row=0, column=1, ipadx=30, ipady=30, sticky="w")
        bg_frame.rowconfigure(0, weight=1)
        bg_frame.columnconfigure(0, weight=1)
        bg_frame.rowconfigure(0, weight=1)
        bg_frame.rowconfigure(1, weight=1)
        
        # logo above login box
        dark_logo = Image.open("assets/3-PL-700x400.png")
        self.logo = ctk.CTkImage(dark_image=dark_logo, light_image=dark_logo, size=(int(dark_logo.width/4),int(dark_logo.height/4)))      
        logo_label = ctk.CTkLabel(bg_frame, image=self.logo, text="")
        logo_label.grid(row=0, column=0, pady=(0,15), sticky="s")
        
        # container inside login box that holds content, used to prevent widgets overlapping corners of login box
        login_cont = ctk.CTkFrame(bg_frame, fg_color=style.grey)
        login_cont.grid(row=1, column=0, sticky="n")
        login_cont.rowconfigure(0, weight=1)
        login_cont.columnconfigure(0, weight=1)

        # welcome text
        welcome_label = ctk.CTkLabel(login_cont, text="Sign in", font=("Segoe UI Black",30), text_color="#ffffff")
        info_label = ctk.CTkLabel(login_cont, text="Enter your organisation's login details below", font=("Segoe UI",20, "bold"), wraplength=300)
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")
        #info_label.grid(row=1, column=0, columnspan=2)

        # username entry
        user_label = ctk.CTkLabel(login_cont, text="Username:", font=("Segoe UI Black",18))
        user_label.grid(row=2, column = 0, padx=5, pady=(10,2), sticky="w")
        self.username = ctk.CTkEntry(login_cont, width=300, height=25, placeholder_text="ID number", font=("Segoe UI Black",18))
        self.username.grid(row=3, column=0, padx=5, pady=(2,10), sticky="w")
        self.after(300, lambda : self.username.focus())
        
        # password entry
        pass_label = ctk.CTkLabel(login_cont, text="Password:", font=("Segoe UI Black",18))
        pass_label.grid(row=4, column = 0, padx=5, pady=(10,2), sticky="w")
        self.password = ctk.CTkEntry(login_cont, width=300, height=25, show="•", placeholder_text="Password", font=("Segoe UI Black",18))
        self.password.grid(row=5, column=0, padx=5, pady=(2, 10), sticky="w")
        
        # error message
        self.error_label = ctk.CTkLabel(login_cont, text="*Invalid username or password", font=(style.bold_font, 16), text_color="#ff0000")
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(0, 5))
        self.error_label.grid_remove()
        
        command = lambda : show_error()
        command2 = lambda : hide_error()
        
        # submit button
        self.login_button =ctk.CTkButton(login_cont, command=command, width=100, height=40, text="Login", font=("Segoe UI Black", 25), fg_color="#00a2ff")
        self.login_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # help button
        help_command = lambda : help()
        help_button = ctk.CTkButton(login_cont, command=help_command, 
                                    width=30, height=30, corner_radius=15, 
                                    text="?", font=("Segoe UI Black", 20), text_color="black", anchor="center",
                                    fg_color="#ffffff", hover_color="#d4d4d4")
        help_button.grid(row=7, column=1, sticky="e")
        
        # help message
        self.help_label = ctk.CTkLabel(login_cont, text="All login information is managed by your organisation's admin, \nplease see them for any assistance required",
                                  font=(style.normal_font, 16), text_color="#ececec", wraplength=300)
        self.help_label.grid(row=8, column=0, columnspan=2)
        self.help_label.grid_remove()
    
    def random_img(self):
        return random.choice(self.images)
    
    def change_img(self):
        print("yas")
        img = ImageTk.PhotoImage((Image.open(self.random_img())).resize((700,700), Image.LANCZOS))
        self.img_label.configure(image=img)