import customtkinter as ctk
import src.style as style

class FilamentPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=(5,25))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=10)

        
        topbar = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        topbar.grid(row=0,column=0, sticky='we')
        topbar.columnconfigure(0, weight=1)
        
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=[" View "," Add "], 
                                               font=(style.normal_font, 22), text_color="white",
                                               selected_color=style.main_blue, selected_hover_color=style.hover_blue,
                                               border_width=0, corner_radius=10,
                                               command=self.switch_subpage)
        option_button.grid(row=0,column=0, sticky="w",padx=25)
        option_button.set(" View ")
        
        line = ctk.CTkFrame(topbar, height=5, fg_color="#585858")
        line.grid(row=1,column=0, sticky="we", padx=10, pady=(10,0))

        content_box = ctk.CTkFrame(container,fg_color=style.dark_foreground)
        content_box.grid(row=1, column=0, sticky="nsew")
        
#=================================================================================
        # initialise view subpage
        self.view_box = ctk.CTkFrame(container,fg_color=style.dark_foreground)
        self.view_box.grid(row=0, column=0, sticky="nsew")
        
#=================================================================================
        #initialise add subpage
        self.add_box = ctk.CTkFrame(container,fg_color=style.dark_foreground)
        self.add_box.grid(row=0, column=0, sticky="nsew")
        
        self.grid_view()
#=================================================================================
    def switch_subpage(self,page):
        match page:
            case " View ":
                self.remove_add()
                self.grid_view()
            case " Add ":
                self.remove_view()
                self.grid_add()
    
    # display subpage to view filaments        
    def grid_view(self):
        self.view_box.grid()
    
    # hide subpage to view filaments
    def remove_view(self):
        self.view_box.grid_remove()
    
    # display subpage to add filaments
    def grid_add(self):
        self.add_box.grid()
        
    # hide subpage to add filaments    
    def remove_add(self):
        self.add_box.grid_remove()