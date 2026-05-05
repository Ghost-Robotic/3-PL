import customtkinter as ctk
from os import system, name
from login import Login 
from dashboard import Dashboard



class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.bind("<Configure>", self.on_resize)
        # configure window
        self.title("3-PL")
        system(self.after(1, self.wm_state ,('zoomed')) if name == 'nt' else self.attributes('-zoomed', True))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(576, 324)
        
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
          
           
        self.display_page(Login)  
        #self.display_page(Dashboard)  
           
        #login = Login(container, self)
        #login.pack(expand=True, anchor="center")
        #login.place(in_=container, anchor = "c", relx=.5, rely=.5)
        #login.tkraise()
        
    def display_page(self, frame):
        page = self.frames[frame]
        page.tkraise()
        
    def start(self):    
        self.mainloop()
        
    def on_resize(self, event):
        pass
        #print(f"{event.width}x{event.height}")