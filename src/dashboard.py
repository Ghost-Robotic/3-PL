import sys
sys.path.append("../3_PL")
import customtkinter as ctk
from PIL import Image, ImageTk
import src.style as style
from src.pages.home import Home
from src.pages.add import Add
from src.pages.log import Log
from src.pages.account import AccountPage
from src.pages.printers import PrintersPage
from src.pages.filament import FilamentPage
from src.helpers.loading import Loading
from src.database import PrinterFilaments, Users, Logs, PrinterModels, Printers, Filaments
# main page that allows users to access sub-pages that contain main app functions

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_background)
        
        # logout_button = ctk.CTkButton(self, command=(lambda : self.logout()), width=100, height=40, text="Logout", font=("Segoe UI Black", 25),
        #                               fg_color="#00a2ff", hover_color="#0087d4")
        # logout_button.pack(side="top",anchor='e',padx=3,pady=3)
        
        # navigation bar with buttons for different tabs
        nav_container= ctk.CTkFrame(self, fg_color=style.dark_background, corner_radius=30, bg_color=style.dark_background)
        # nav_container.grid(row=0, column=0, padx=0, pady=(0,0))
        nav_container.pack(side="top", pady=(30,0))
        
        #===========================================
        #logo = ImageTk.PhotoImage((Image.open("assets/3-PL-700x400.png")).resize((140,80), Image.LANCZOS))
        logo = ctk.CTkImage(dark_image=Image.open("assets/3-PL-700x400.png"),size=(140,80))
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
        # self.add_log_button = ctk.CTkButton(nav_container, command=(lambda : self.set_page("add")),
        #                             text="+", font=("Segoe UI Black", 50),
        #                             fg_color=style.dark_background, hover_color=style.dark_foreground, corner_radius=0)
        # self.add_log_button.pack(side='left', fill="y", expand=True)
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
        
        # container where each page will be displayed
        self.page_container = ctk.CTkFrame(self, fg_color=style.dark_background)
        self.page_container.pack(side="top", fill="both", expand=True)
        self.page_container.rowconfigure(0,weight=1)
        self.page_container.columnconfigure(0,weight=1)
        
        self.box = ctk.CTkFrame(self.page_container, corner_radius=30, fg_color=style.dark_foreground)
        self.box.grid(row=0,column=0,sticky="nsew",padx=(40,40), pady=(0,40))
        #self.box.pack(side="top", padx=(40,40), pady=(0,40), fill="both", expand=True)
        self.box.rowconfigure(0, weight=1)
        self.box.columnconfigure(0, weight=1)   
                
        self.pages = {}      
        # for page in (Home, Log, PrintersPage, FilamentPage, AccountPage):
        #     frame = page(self.box, self.controller)
        #     self.pages[page] = frame 
        #     frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)       
        #     frame.rowconfigure(0, weight=1)
        #     frame.columnconfigure(0, weight=1) 
        
        # initialise home page       
        self.current_page="home"
        self.set_page("home") 
        self.home_button.configure(fg_color=style.dark_foreground)
        
    def page_constructor(self, page): 
        """ initialise given page

        Args:
            page (class): tkinter frame
        """
        frame = page(self.box,self.controller, self)
        self.pages[page] = frame
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)       
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1) 
        
    def loading_frame(self):
        """loading animation when each page is first initialised"""
        frame = Loading(self.page_container,self.controller)
        frame.grid(row=0, column=0, sticky="nsew",padx=40,pady=(0,40))
        frame.grid_single()
        
    def display_page(self, frame):
        page = self.pages[frame]
        page.tkraise()
        
    def logout(self):
        self.controller.logout()
        
    def set_page(self, page):
        """ display given page, initialise page if it does not exist

        Args:
            page (str): name of page
        """
        #self.loading_frame()
        match page:
            case "home":
                try:
                    self.display_page(Home)
                    self.reset_tab(self.current_page)
                    self.current_page = "home"
                    self.home_button.configure(fg_color=style.dark_foreground)
                except:
                    self.reset_tab(self.current_page)
                    self.home_button.configure(fg_color=style.dark_foreground)
                    self.page_constructor(Home)
                    self.current_page = "home"
            # case "add":
            #     self.display_page(Add)
            #     self.reset_tab(self.current_page)
            #     self.current_page = "add"
            #     self.add_log_button.configure(fg_color=style.dark_foreground)
            case "log":
                try:
                    self.display_page(Log)
                    self.reset_tab(self.current_page)
                    self.current_page = "log"
                    self.log_button.configure(fg_color=style.dark_foreground)
                except:
                    self.reset_tab(self.current_page)
                    self.log_button.configure(fg_color=style.dark_foreground)                    
                    self.current_page = "log"                    
                    self.loading_frame()
                    self.page_constructor(Log)
            case "printers":
                try:
                    self.display_page(PrintersPage)
                    self.reset_tab(self.current_page)
                    self.current_page = "printers"
                    self.printers_button.configure(fg_color=style.dark_foreground)
                except:
                    self.reset_tab(self.current_page)
                    self.printers_button.configure(fg_color=style.dark_foreground)
                    self.loading_frame()
                    self.page_constructor(PrintersPage)
                    self.current_page = "printers"
            case "filaments":
                try:
                    self.display_page(FilamentPage)
                    self.reset_tab(self.current_page)
                    self.current_page = "filaments"
                    self.filaments_button.configure(fg_color=style.dark_foreground)
                except:
                    self.reset_tab(self.current_page)
                    self.filaments_button.configure(fg_color=style.dark_foreground)
                    self.loading_frame()
                    self.page_constructor(FilamentPage)
                    self.current_page = "filaments"
            case "account":
                try:
                    self.display_page(AccountPage)
                    self.reset_tab(self.current_page)
                    self.current_page = "account"
                    self.account_button.configure(fg_color=style.dark_foreground)
                except:
                    self.reset_tab(self.current_page)
                    self.account_button.configure(fg_color=style.dark_foreground)
                    self.loading_frame()
                    self.page_constructor(AccountPage)
                    self.current_page = "account"
                
    def reset_tab(self, tab):
        """ resets button colour of given page

        Args:
            tab (str): name of page
        """
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
                
if __name__ == "__main__":
    class Test(ctk.CTk):
        def __init__(self, *args, **kwargs):
            self.database = r"database/log.db"
            self.access = True
            self.current_user = 123456
            self.auth_level = 5
            ctk.CTk.__init__(self, *args, **kwargs)
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            
            self.accounts = Users(self.database)
            self.logs = Logs(self.database)
            self.printer_models = PrinterModels(self.database)
            self.printers = Printers(self.database)
            self.filaments = Filaments(self.database)
            self.printer_filament = PrinterFilaments(self.database)
            
            
            dashboard = Dashboard(self,self)
            dashboard.grid(row=0, column=0, sticky="nsew")       
            dashboard.rowconfigure(0, weight=1)
            dashboard.columnconfigure(0, weight=1)
            
            self.after(1, lambda : self.state('zoomed'))
            
    app = Test()
    app.mainloop()
                