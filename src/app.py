import customtkinter as ctk
from tkinter import ttk
from os import system, name
from login import Login 


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        
        #configuration
        self.title("3-PL")
        system(self.after(1, self.wm_state ,('zoomed')) if name == 'nt' else self.attributes('-zoomed', True))
        
        container = ctk.CTkFrame(self, bg_color="#2b2b2b")
        container.pack(side = "top", fill = "both", expand = True)
        
           
        login = Login(container, self)
        login.place(in_=container, anchor = "c", relx=.5, rely=.5)
        login.tkraise()
        
        #Theme 
        #self.configure(bg="#1c2526")
        

app = App()
app.mainloop()