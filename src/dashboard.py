import customtkinter as ctk
from PIL import Image, ImageTk
import src.style as style
from src.pages.home import Home
from src.pages.add import Add
from src.pages.log import Log
from src.pages.account import AccountPage
from src.pages.printers import PrintersPage
from src.pages.filament import FilamentPage
# main page that allows users to access sub-pages that contain main app functions

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_background)
        
        logout_button = ctk.CTkButton(self, command=(lambda : self.logout()), width=100, height=40, text="Logout", font=("Segoe UI Black", 25),
                                      fg_color="#00a2ff", hover_color="#0087d4")
        logout_button.pack(side="top",anchor='e',padx=3,pady=3)
        
        # navigation bar
        nav_container= ctk.CTkFrame(self, fg_color=style.dark_background, corner_radius=30, bg_color=style.dark_background)
        # nav_container.grid(row=0, column=0, padx=0, pady=(0,0))
        nav_container.pack(side="top", pady=(0,0))
        
        #===========================================
        logo = ImageTk.PhotoImage((Image.open("assets\\3-PL-700x400.png")).resize((140,80), Image.LANCZOS))
        logo_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("home")), 
                                    image=logo, anchor="center", text="", 
                                    corner_radius=0, fg_color=style.dark_background,
                                    hover=False, width=160, height=100)
        logo_button.pack(side='left', pady=(0,0))     
        #===========================================
        self.home_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("home")),
                                    text="Home", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.home_button.pack(side='left', fill="y", expand=True)
        #===========================================
        self.add_log_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("add")),
                                    text="+", font=("Segoe UI Black", 50),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.add_log_button.pack(side='left', fill="y", expand=True)
        #===========================================
        self.log_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("log")),
                                    text="Log", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.log_button.pack(side='left', fill="y", expand=True)
        #===========================================
        self.printers_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("printers")),
                                    text="Printers", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.printers_button.pack(side='left', fill="y", expand=True)
        #===========================================
        self.filaments_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("filaments")),
                                    text="Filaments", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.filaments_button.pack(side='left', fill="y", expand=True)
        #===========================================        
        self.account_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("account")),
                                    text="Account", font=("Segoe UI Black", 22),
                                    fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        self.account_button.pack(side='left', fill="y", expand=True)
        
        # page
        page_container = ctk.CTkFrame(self, fg_color=style.dark_background)
        page_container.pack(side="top", fill="both", expand=True)
        
        box = ctk.CTkFrame(page_container, corner_radius=30, fg_color=style.dark_foreground)
        box.pack(side="top", padx=(40,40), pady=(0,40), fill="both", expand=True)
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)   
                
        self.pages = {}      
        for page in (Home, Add, Log, PrintersPage, FilamentPage, AccountPage):
            frame = page(box, controller)
            self.pages[page] = frame 
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)       
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1) 
               
        self.current_page="home"
        self.set_page("home")    
        
        
    def display_page(self, frame):
        page = self.pages[frame]
        page.tkraise()
        
    def logout(self):
        self.controller.logout()
        
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
            case "printers":
                self.display_page(PrintersPage)
                self.reset_tab(self.current_page)
                self.current_page = "printers"
                self.printers_button.configure(fg_color=style.dark_foreground)
            case "filaments":
                self.display_page(FilamentPage)
                self.reset_tab(self.current_page)
                self.current_page = "filaments"
                self.filaments_button.configure(fg_color=style.dark_foreground)
            case "account":
                self.display_page(AccountPage)
                self.reset_tab(self.current_page)
                self.current_page = "account"
                self.account_button.configure(fg_color=style.dark_foreground)
                
    def reset_tab(self, tab):
        match tab:
            case "home":
                self.home_button.configure(fg_color=style.dark_background)
            case "add":
                self.add_log_button.configure(fg_color=style.dark_background)
            case "log":
                self.log_button.configure(fg_color=style.dark_background)
            case "printers":
                self.printers_button.configure(fg_color=style.dark_background)
            case "filaments":
                self.filaments_button.configure(fg_color=style.dark_background)
            case "account":
                self.account_button.configure(fg_color=style.dark_background)
                