import customtkinter as ctk
import os
import sys
from src.login import Login 
from src.dashboard import Dashboard
from src.database import Users, Logs, PrinterModels, Printers, Filaments
import src.database as db
from PIL import Image, ImageTk
import src.style as style
from src.helpers.loading import Loading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        self.database = r"database\log.db"
        
        self.access = False
        self.current_user = None
        self.auth_level = None
        ctk.CTk.__init__(self, *args, **kwargs)
        #self.bind("<Configure>", self.on_resize)
        # configure window
        self.title("3-PL")
        # logo = Image.open(r"assets\v2logo.png")
        # icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        # logo.save('v2logo.ico', format='ICO', sizes=icon_sizes)
        self.iconbitmap(r"assets\v2logo.ico")
        #system(self.after(1, self.wm_state ,('zoomed')) if name == 'nt' else self.attributes('-zoomed', True))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(576, 324)
        
        # create container that all content will be placed in        
        self.container = ctk.CTkFrame(self, bg_color=style.dark_background)
        self.container.grid(row = 0, column = 0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        
        frame = Loading(self,self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_triple()         

        self.frames = {}     
        for page in ((Login,)):
            frame = page(self.container, self)
            self.frames[page] = frame 
            frame.grid(row=0, column=0, sticky="nsew")       
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

        #self.display_page(Login)  
        #self.display_page(Dashboard)
        #self.display_page(list(self.frames)[0])
           
        
    def display_page(self, frame=None, index=None):
        page = self.frames[frame]
        page.tkraise()                        
        
    def start(self): 
        self.after(1, lambda : self.state('zoomed'))
        self.mainloop()
        
    def login(self):
        if self.access == True and len(self.current_user) == 6:

            self.auth_level = db.accounts.fetch_auth(self.current_user)
            for page in ((Dashboard,)):
                frame = page(self.container, self)
                self.frames[page] = frame 
                frame.grid(row=0, column=0, sticky="nsew")       
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
            self.display_page(Dashboard)
            
    def logout(self):
        frame = Loading(self,self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_triple() 
        self.access = False
        self.current_user = None
        self.auth_level = None
        self.frames[Dashboard].destroy()
        
    def on_resize(self, event):
        #pass
        print(f"{event.width}x{event.height}")