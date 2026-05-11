import customtkinter as ctk
from PIL import Image, ImageTk
import style
from pages.home import Home
from pages.add import Add
from pages.log import Log
from pages.manage import Manage
# main page that allows users to access sub-pages that contain main app functions

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color="#2b2b2b")
        
        # navigation bar
        nav_container= ctk.CTkFrame(self, fg_color=style.dark_background, corner_radius=30, bg_color=style.dark_background)
        # nav_container.grid(row=0, column=0, padx=0, pady=(0,0))
        nav_container.pack(side="top", pady=(30,0))
        
        
        logo = ImageTk.PhotoImage((Image.open("assets\\3-PL-700x400.png")).resize((140,80), Image.LANCZOS))
        logo_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("home")), 
                                    image=logo, anchor="center", text="", 
                                    corner_radius=0, fg_color=style.dark_background,
                                    hover=False, width=160, height=100)
        logo_button.pack(side='left', pady=(0,0))     
        
        self.home_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("home")),
                                    text="Home", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.home_button.pack(side='left', fill="y", expand=True)
        
        self.add_log_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("add")),
                                    text="+", font=("Segoe UI Black", 50),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.add_log_button.pack(side='left', fill="y", expand=True)
        
        self.log_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("log")),
                                    text="Log", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.log_button.pack(side='left', fill="y", expand=True)
        
        self.manage_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("manage")),
                                    text="Manage", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.manage_button.pack(side='left', fill="y", expand=True)
        
        # page
        page_container = ctk.CTkFrame(self)
        page_container.pack(side="top", fill="both", expand=True)
        
        box = ctk.CTkFrame(page_container, corner_radius=30, fg_color=style.dark_foreground)
        box.pack(side="top", padx=(40,40), pady=(0,40), fill="both", expand=True)
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)   
                
        self.pages = {}      
        for page in (Home, Add, Log, Manage):
            frame = page(box, self)
            self.pages[page] = frame 
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)       
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1) 
               
        self.current_page="home"
        self.set_page("home")    
        
        
    def display_page(self, frame):
        page = self.pages[frame]
        page.tkraise()
        
    def set_page(self, page):
        match page:
            case "home":
                self.display_page(Home)
                self.reset_tab(self.current_page)
                self.current_page = "home"
                self.home_button.configure(fg_color=style.dark_foreground)
            case "add":
                self.display_page(Add)
                self.reset_tab(self.current_page)
                self.current_page = "add"
                self.add_log_button.configure(fg_color=style.dark_foreground)
            case "log":
                self.display_page(Log)
                self.reset_tab(self.current_page)
                self.current_page = "log"
                self.log_button.configure(fg_color=style.dark_foreground)
            case "manage":
                self.display_page(Manage)
                self.reset_tab(self.current_page)
                self.current_page = "manage"
                self.manage_button.configure(fg_color=style.dark_foreground)
                
    def reset_tab(self, tab):
        match tab:
            case "home":
                self.home_button.configure(fg_color=style.dark_background)
            case "add":
                self.add_log_button.configure(fg_color=style.dark_background)
            case "log":
                self.log_button.configure(fg_color=style.dark_background)
            case "manage":
                self.manage_button.configure(fg_color=style.dark_background)
                