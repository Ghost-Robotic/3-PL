import customtkinter as ctk
import src.style as style
import random
from PIL import Image

class Home(ctk.CTkFrame):
    def __init__(self, parent, controller, parent_controller):
        self.controller = controller
        self.model_imgs = [r"assets\modelpics\plate_1.png", r"assets\modelpics\plate_2.png", r"assets\modelpics\plate_3.png", r"assets\modelpics\plate_4.png", 
                          r"assets\modelpics\plate_5.png", r"assets\modelpics\plate_6.png", r"assets\modelpics\plate_7.png", ]
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=(5,25))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
        # container with cycling images
        img_container = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        img_container.grid(row=0, column=0, sticky="nsew", rowspan=2)
        img_container.columnconfigure(0, weight=1)
        img_container.rowconfigure(0, weight=1)
        
        img = ctk.CTkImage(dark_image=Image.open(self.random_img()),size=(600,600))
        
        self.img_label = ctk.CTkButton(img_container, image=img, command=self.change_img, text="", hover=False, fg_color=style.dark_foreground)
        self.img_label.grid(row=0, column=0)
        self.img_cycle = self.after(5000, self.change_img)
        
        # buttons on left of screen
        nav_tabs = {"log" : "Add New Print Job",
                    "printers" : "View Available Printers",
                    "filaments" : "View Available Filament",
                    "account" : "View Profile"}
        
        self.nav_buttons_cont = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        self.nav_buttons_cont.grid(row=0,column=0,sticky="w",padx=(10,0))
        image = ctk.CTkImage(dark_image=Image.open(r"assets\toolhead-transp.png"),size=(120,120))
        image_box = ctk.CTkButton(self.nav_buttons_cont, image=image,fg_color=style.dark_foreground,state="disabled",text="")
        image_box.pack(side="top",padx=(120,0))
        
        
        for tab in list(nav_tabs):
            button = ctk.CTkButton(self.nav_buttons_cont, text=nav_tabs[tab], command=lambda page=tab: parent_controller.set_page(page),
                                   border_color=style.main_blue,border_width=0,fg_color=style.dark_foreground,
                                   font=(style.normal_font,23,"bold"),text_color=style.main_blue, hover_color="#3A3A3A",
                                   width=280, height=50,anchor="w")
            button.pack(side='top', pady=8)
            
        # buttons on right of screen only available to admins
        self.admin_buttons_cont = ctk.CTkFrame(container)
        
    def random_img(self):
        return random.choice(self.model_imgs)
    
    def change_img(self):
        self.after_cancel(self.img_cycle)
        img = ctk.CTkImage(dark_image=Image.open(self.random_img()),size=(600,600))
        self.img_label.configure(image=img)
        self.img_cycle = self.after(5000, self.change_img)