import customtkinter as ctk
import sys
sys.path.append("../3_PL")
import src.style as style

def show_success(parent, controller):
    success_cont = ctk.CTkFrame(parent, border_width=3, border_color=style.main_green,corner_radius=10, width=400, height=100)
    success_cont.grid(row=0, column=0)
    success_cont.rowconfigure(0,weight=1)
    success_cont.rowconfigure(1,weight=5)
    success_cont.columnconfigure(0,weight=1)
    
    topbar = ctk.CTkFrame(success_cont, fg_color="#242323", corner_radius=10)
    topbar.grid(row=0,column=0,sticky="new",padx=5,pady=5)
    success_label = ctk.CTkLabel(topbar, text="Successfully Saved ", font=(style.normal_font,25,"bold"), text_color=style.main_green, width=370, anchor="w")
    success_label.grid(row=0,column=0, padx=(10,0),pady=7, sticky="nw")
    
    close_button = ctk.CTkButton(topbar, text="X", font=(style.normal_font,20,"bold"), text_color="white",
                                    hover_color="red", fg_color="#242323",width=30,height=30,
                                    command=(lambda : success_cont.destroy()))
    close_button.grid(row=0,column=1, sticky="se", padx=7,pady=7)
    
    success_frame = ctk.CTkFrame(success_cont, fg_color=style.dark_background, width=500, height=100)
    success_frame.grid(row=1, column=0, sticky="nsew",padx=5,pady=5)
    success_frame.columnconfigure(0,weight=1)
    

    success = ctk.CTkLabel(success_frame, text="", font=(style.normal_font,20,"bold"), text_color="white")
    success.grid(row=0,column=0, padx=(15,0))
    
    okay_button = ctk.CTkButton(success_frame, text="Okay", font=(style.normal_font,22,"bold"),
                                    border_color=style.main_blue, border_width=2,hover_color=style.main_blue, fg_color=style.dark_background,width=50,
                                    command=(lambda : success_cont.destroy()))
    okay_button.grid(row=1,column=1, sticky="se", padx=10,pady=10)