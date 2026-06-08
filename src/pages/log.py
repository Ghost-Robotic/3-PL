import customtkinter as ctk
import src.style as style
from .add import Add

class Log(ctk.CTkFrame):
    def __init__(self, parent, controller, parent_controller):
        self.controller = controller
        self.parent_controller = parent_controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=(5,25))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=20)

        
        topbar = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        topbar.grid(row=0,column=0, sticky='nwe', pady=(10,0))
        topbar.columnconfigure(0, weight=1)
        
        options = []
        if self.controller.auth_level != None:
            if self.controller.auth_level >= 3:
                options = [" Add "," View "]
            elif self.controller.auth_level >= 2:
                options = [" Add "]
            else:
                options = [" No Access "]
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=options, 
                                            font=(style.normal_font, 22), text_color="white",
                                            selected_color=style.main_blue, selected_hover_color=style.hover_blue,
                                            border_width=0, corner_radius=10,
                                            command=self.switch_subpage)
        option_button.grid(row=0,column=0, sticky="w",padx=25)        
        if " No Access " not in options:

            option_button.set(" Add ")
        
        line = ctk.CTkFrame(topbar, height=5, fg_color="#585858")
        line.grid(row=1,column=0, sticky="we", padx=10, pady=(10,0))

        self.content_box = ctk.CTkFrame(container,fg_color=style.dark_foreground)
        self.content_box.grid(row=1, column=0, sticky="nsew")
        self.content_box.rowconfigure(0, weight=1)
        self.content_box.columnconfigure(0, weight=1)
        
#=================================================================================
        # initialise view subpage
        self.view_box = ctk.CTkFrame(self.content_box,fg_color=style.dark_foreground)
        self.view_box.grid(row=0, column=0, sticky="nsew", ipadx=10, ipady=10)
        self.view_box.rowconfigure(0, weight=1)
        self.view_box.rowconfigure(1, weight=30)
        self.view_box.columnconfigure(0, weight=1)
        self.view_box.grid_remove()
    
        log_table = self.controller.logs.fetch_table()        
        
        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=37,
                                              scrollbar_button_color=style.dark_foreground, scrollbar_button_hover_color=style.dark_foreground)
        header_frame.grid(row=0, column=0, sticky="nswe", padx=10,pady=0)
        header_frame._scrollbar.configure(height=0)
        table_header = ["ID", "User","Name", "Duration", "Weight (g)", "Printer", "Filament", "Time", "Date"]
        self.weights = [1,3,3,2,2,3,3,2,2]
        for i in range(len(table_header)):
            header_frame.columnconfigure(i, weight=self.weights[i], uniform=0)
            frame = ctk.CTkFrame(header_frame, border_width=3, border_color=style.main_blue, corner_radius=8)
            frame.grid(row=0,column=i, ipadx=7, ipady=8, sticky="nsew",padx=0)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)       
            label = ctk.CTkLabel(frame, text=table_header[i], font=(style.normal_font, 20, "bold"))
            label.grid(row=0,column=0) 
            
        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in self.weights:
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in log_table:
            column_counter = 0
            for item in row:
                frame = ctk.CTkFrame(self.table_frame, corner_radius=0)
                frame.grid(row=row_counter,column=column_counter, ipadx=7, ipady=8, sticky="nsew",padx=0)
                if (row_counter%2) == 1:
                    frame.configure(fg_color=style.dark_background)
                else:
                    frame.configure(fg_color=style.dark_foreground)
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
                label = ctk.CTkLabel(frame, text=item, font=(style.normal_font, 17))
                label.grid(row=0,column=0)
                if column_counter == 0: label.configure(font=(style.normal_font, 17,'bold'))
                column_counter += 1
            row_counter += 1
        
        
#=================================================================================
        # initialise add subpage
        if " No Access " not in options:
            self.add = Add(self.content_box, self.controller, self)
            self.add.grid(row=0, column=0, sticky="nsew")
            self.add.rowconfigure(0, weight=1)
            self.add.columnconfigure(0, weight=1)
            self.grid_add()

#=================================================================================
    def switch_subpage(self,page):
        match page:
            case " Add ":
                self.remove_view()
                self.grid_add()
            case " View ":
                self.remove_add()
                self.grid_view()

    # display subpage to add log
    def grid_add(self):
        self.add.grid()
    
    # hide subpage to add log
    def remove_add(self):
        self.add.grid_remove()
    
    # display subpage to view logs        
    def grid_view(self):
        self.view_box.grid()
        #self.update_view()
        
    # hide subpage to view logs
    def remove_view(self):
        self.view_box.grid_remove()        
        
    def update_view(self):
        """refresh view table"""
        self.table_frame.destroy()
        
        log_table = self.controller.logs.fetch_table()
        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in self.weights:
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in log_table:
            column_counter = 0
            for item in row:
                frame = ctk.CTkFrame(self.table_frame, corner_radius=0)
                frame.grid(row=row_counter,column=column_counter, ipadx=7, ipady=8, sticky="nsew",padx=0)
                if (row_counter%2) == 1:
                    frame.configure(fg_color=style.dark_background)
                else:
                    frame.configure(fg_color=style.dark_foreground)
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
                label = ctk.CTkLabel(frame, text=item, font=(style.normal_font, 17))
                label.grid(row=0,column=0)
                if column_counter == 0: label.configure(font=(style.normal_font, 17,'bold'))
                column_counter += 1
            row_counter += 1
    
    def validate_num(self, num):
        return num.isdigit() or num == ""
    
    def default_zero(self, var):
        if var.get() == "":
            var.set(0)