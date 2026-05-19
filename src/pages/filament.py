import customtkinter as ctk
import src.style as style
import src.database as db

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
        content_box.rowconfigure(0, weight=1)
        content_box.columnconfigure(0, weight=1)
        
#=================================================================================
        # initialise view subpage
        self.view_box = ctk.CTkFrame(content_box,fg_color=style.dark_foreground)
        self.view_box.grid(row=0, column=0, sticky="nsew", ipadx=10, ipady=10)
        self.view_box.rowconfigure(0, weight=1)
        self.view_box.rowconfigure(1, weight=10)
        self.view_box.columnconfigure(0, weight=1)
        self.view_box.grid_remove()
        filaments = db.filaments.fetch_all()
        
        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=45)
        header_frame.grid(row=0, column=0, sticky="swe", padx=20)
        header_frame._scrollbar.configure(height=45)
        table_header = ["ID", "Name", "Spool Weight", "No."]
        for i in range(len(table_header)):
            header_frame.columnconfigure(i, weight=1, uniform=0)
            frame = ctk.CTkFrame(header_frame, border_width=3, border_color=style.main_blue, corner_radius=8)
            frame.grid(row=0,column=i, ipadx=7, ipady=8, sticky="nsew",padx=0)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)       
            label = ctk.CTkLabel(frame, text=table_header[i], font=(style.normal_font, 20, "bold"))
            label.grid(row=0,column=0) 
        
        table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        for i in range(4):
            table_frame.columnconfigure(i, weight=1, uniform=0) 
        row_counter = 0
        for row in filaments:
            column_counter = 0
            for item in row:
                frame = ctk.CTkFrame(table_frame, border_width=3, corner_radius=0)
                frame.grid(row=row_counter,column=column_counter, ipadx=7, ipady=8, sticky="nsew",padx=0)
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
                label = ctk.CTkLabel(frame, text=item, font=(style.normal_font, 15))
                label.grid(row=0,column=0)
                if column_counter == 0: label.configure(font=(style.normal_font, 15,'bold'))
                column_counter += 1
            row_counter += 1
        
#=================================================================================
        #initialise add subpage
        self.add_box = ctk.CTkFrame(content_box,fg_color=style.dark_foreground)
        self.add_box.grid(row=0, column=0, sticky="nsew")
        self.add_box.grid_remove()
        
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