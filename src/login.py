import customtkinter as ctk
from PIL import Image, ImageTk
import src.style as style
import random
import src.helpers.hash_utils as hsh
from src.helpers.loading import Loading
# initial landing page where users are directed to login
class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        #controller.bind("<Configure>", controller.on_resize)
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_background) 
        self.images = ["assets/c-1L-dark2.png", "assets/c1-indx.png", "assets/h2d.png", "assets/ht90-dark.png", 
                       "assets/P1S.png", "assets/xl.png", "assets/xl2.png", "assets/xl5-transp.png",r"assets/f4l.png",r"assets/fuse.png"]
                
            
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=4)
        container.grid_rowconfigure(1, weight=5)
        
        img_container = ctk.CTkFrame(container, fg_color=style.dark_background)
        img_container.grid(row=0, column=0, sticky="nsew", rowspan=2)
        img_container.columnconfigure(0, weight=1)
        img_container.rowconfigure(0, weight=1)
        #img = ImageTk.PhotoImage((Image.open(self.random_img())).resize((700,700), Image.LANCZOS))
        img = ctk.CTkImage(dark_image=Image.open(self.random_img()),size=(700,700))
        
        self.img_label = ctk.CTkButton(img_container, image=img, command=self.change_img, text="", hover=False, fg_color=style.dark_background)
        self.img_label.grid(row=0, column=0)
        self.img_cycle = self.after(5000, self.change_img)
        
        # floating widget for login form
        login_widget = ctk.CTkFrame(container, fg_color=style.grey, corner_radius=30)
        login_widget.grid(row=1, column=1, ipadx=30, ipady=30, sticky="n")
        login_widget.rowconfigure(0, weight=1)
        login_widget.columnconfigure(0, weight=1)
        login_widget.rowconfigure(0, weight=1)
        login_widget.rowconfigure(1, weight=1)
        
        # logo above login box
        dark_logo = Image.open("assets/3-PL-700x400.png")
        self.logo = ctk.CTkImage(dark_image=dark_logo, light_image=dark_logo, size=(int(dark_logo.width/4),int(dark_logo.height/4)))      
        logo_label = ctk.CTkLabel(container, image=self.logo, text="")
        logo_label.grid(row=0, column=1, pady=(0,15), sticky="s")
        
        # container inside login_widget that holds content, used to prevent widgets overlapping corners of login box
        login_cont = ctk.CTkFrame(login_widget, fg_color=style.grey)
        login_cont.grid(row=1, column=0, sticky="n", padx=(5,0))
        login_cont.rowconfigure(0, weight=1)
        login_cont.columnconfigure(0, weight=1)

        # welcome text
        welcome_label = ctk.CTkLabel(login_cont, text="Sign in", font=("Segoe UI Black",30), text_color="#ffffff")
        info_label = ctk.CTkLabel(login_cont, text="Enter your organisation's login details below", font=("Segoe UI",20, "bold"), wraplength=300)
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")
        #info_label.grid(row=1, column=0, columnspan=2)

        # username entry
        validate_id = self.register(self.validate_id)
        
        user_label = ctk.CTkLabel(login_cont, text="ID Number:", font=("Segoe UI Black",18))
        user_label.grid(row=2, column = 0, padx=5, pady=(10,2), sticky="w")
        self.username = ctk.CTkEntry(login_cont, width=300, height=25, placeholder_text="ID number", font=(style.normal_font,18,"bold"),
                                     validate="key", validatecommand=(validate_id, "%P"))
        self.username.grid(row=3, column=0, padx=5, pady=(2,10), sticky="w")
        self.after(300, lambda : self.username.focus())
        self.username.bind("<Return>", lambda event : self.submit())
        
        # password entry
        pass_label = ctk.CTkLabel(login_cont, text="Password:", font=("Segoe UI Black",18))
        pass_label.grid(row=4, column = 0, padx=5, pady=(10,2), sticky="w")
        self.password = ctk.CTkEntry(login_cont, width=300, height=25, show="●", placeholder_text="Password", font=(style.normal_font,18,"bold"))
        self.password.grid(row=5, column=0, padx=5, pady=(2, 10), sticky="w")
        self.password.bind("<Return>", lambda event : self.submit())
        
        # error message
        self.error_label = ctk.CTkLabel(login_cont, text="*Invalid username or password", font=(style.bold_font, 16), text_color="#ff0000")
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(0, 5))
        self.error_label.grid_remove()
        

        # submit button
        self.login_button =ctk.CTkButton(login_cont, command=(lambda : self.submit()), width=100, height=40, text="Login", font=("Segoe UI Black", 25)
                                         , fg_color="#00a2ff", hover_color="#0087d4")
        self.login_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # help button
        help_button = ctk.CTkButton(login_cont, command=(lambda : self.help()), 
                                    width=30, height=30, corner_radius=15, 
                                    text="?", font=("Segoe UI Black", 20), text_color="black", anchor="center",
                                    fg_color="#ffffff", hover_color="#d4d4d4")
        help_button.grid(row=7, column=1, sticky="e")
        
        # help message
        self.help_label = ctk.CTkLabel(login_cont, text="Login details are managed by your organisation's admin. Please see them for assistance",
                                  font=(style.normal_font, 16), text_color="#ececec", wraplength=300)
        self.help_label.grid(row=8, column=0, columnspan=2)
        self.help_label.grid_remove()
        
        
    def show_error(self):
        """grid error label"""
        self.error_label.grid()
        
    def hide_error(self):
        """hide error lavel"""
        self.error_label.grid_remove()
        
    def help(self):
        """toggle help label"""
        if self.help_label.winfo_viewable():
            self.help_label.grid_remove()
        else:
            self.help_label.grid()
            
    def clear_username(self):
        """clear username entry field"""
        self.username.delete(0, ctk.END)
        
    def clear_password(self):
        """clear passoword entry field"""
        self.password.delete(0, ctk.END)
                       
    def random_img(self):
        return random.choice(self.images)
    
    def change_img(self):
        self.after_cancel(self.img_cycle)
        #img = ImageTk.PhotoImage((Image.open(self.random_img())).resize((700,700), Image.LANCZOS))
        img = ctk.CTkImage(dark_image=Image.open(self.random_img()),size=(700,700))
        self.img_label.configure(image=img)
        self.img_cycle = self.after(5000, self.change_img)
        
    def validate_id(self, id):
        if id == "ID number":
            return True
        return id.isdigit() or id==""
        
    def submit(self):
        """login if username and password are valid"""
        if self.username.get() != "" and self.password.get() != "":
            try:
                # gets corresponding hashed password and salt for given user_id
                matched_password, salt = self.controller.accounts.fetch_password(self.username.get())
                # hashes given password
                hashed_password = hsh.hash(password=self.password.get(), salt=salt)
                # check if given password matches stored password
                if matched_password == hashed_password:
                    frame = Loading(self.controller,self.controller)
                    frame.grid(row=0, column=0, sticky="nsew")
                    frame.grid_triple() 
                    
                    self.controller.access = True
                    self.controller.current_user = self.username.get()
                    self.controller.login()
                    print("match")
                    self.username.focus()
                    self.clear_username()
                    self.clear_password()
                    self.hide_error()
                    
                else:
                    raise Exception("Incorrect Password")
            except Exception as e:
                print(e)
                self.clear_password()
                self.show_error()
        else:
            print("no input detected")