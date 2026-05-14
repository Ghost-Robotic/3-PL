import customtkinter as ctk
from os import system, name
from src.login import Login 
from src.dashboard import Dashboard
from src.database import Users
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        self.access = False
        self.current_user = None
        ctk.CTk.__init__(self, *args, **kwargs)
        #self.bind("<Configure>", self.on_resize)
        # configure window
        self.title("3-PL")
        #logo = Image.open(r"assets\logov4.png")
        #icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        #logo.save('logov4.ico', format='ICO', sizes=icon_sizes)
        self.iconbitmap(r"assets\logov4.ico")
        #system(self.after(1, self.wm_state ,('zoomed')) if name == 'nt' else self.attributes('-zoomed', True))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(576, 324)
        self.wm_aspect(16,9,16,9)
        
        # create container that all content will be placed in        
        container = ctk.CTkFrame(self, bg_color="#2b2b2b")
        container.grid(row = 0, column = 0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # bg_img = Image.open("assets\\bg.png")
        # self.bg = ctk.CTkImage(dark_image=bg_img, size=(self.winfo_screenwidth(),self.winfo_screenheight()))      
        # bg_label = ctk.CTkLabel(container, image=self.bg, text="")
        # bg_label.grid(row=0, column=0)
        

        self.frames = {}
                   
        for page in (Login, Dashboard):
            frame = page(container, self)
            self.frames[page] = frame 
            frame.grid(row=0, column=0, sticky="nsew")       
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
          
           
        #self.display_page(Login)  
        #self.display_page(Dashboard)
        self.display_page(list(self.frames)[0])
           
        self.setup_database()
    
    def setup_database(self):
        self.accounts = Users(r"src\database\log.db")
        
    def display_page(self, frame=None, index=None):
        page = self.frames[frame]
        page.tkraise()                        
        
    def start(self): 
        self.after(1, lambda : self.state('zoomed'))
        self.mainloop()
        
    def login(self):
        if self.access == True and len(self.current_user) == 6:
            self.display_page(Dashboard)
        
    def on_resize(self, event):
        #pass
        print(f"{event.width}x{event.height}")