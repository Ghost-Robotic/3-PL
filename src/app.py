import customtkinter as ctk
from tkinter import ttk
from os import system, name
from login import Login 
from dashboard import Dashboard


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        # configure window
        self.title("3-PL")
        system(self.after(1, self.wm_state ,('zoomed')) if name == 'nt' else self.attributes('-zoomed', True))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # create container that all content will be placed in
        container = ctk.CTkFrame(self, bg_color="#2b2b2b")
        container.grid(row = 0, column = 0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        
        self.frames = {}
                   
        for page in (Login, Dashboard):
            frame = page(container, self)
            self.frames[page] = frame 
            frame.grid(row = 0, column = 0)
          
           
        self.display_page(Login)   
           
        #login = Login(container, self)
        #login.pack(expand=True, anchor="center")
        #login.place(in_=container, anchor = "c", relx=.5, rely=.5)
        #login.tkraise()
        
    def display_page(self, frame):
        page = self.frames[frame]
        page.tkraise()
        
        

app = App()
app.mainloop()