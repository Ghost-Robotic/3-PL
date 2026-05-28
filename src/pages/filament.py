import customtkinter as ctk
import src.style as style
import src.database as db

class FilamentPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=(5,25))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=10)

        
        topbar = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        topbar.grid(row=0,column=0, sticky='nwe', pady=(10,0))
        topbar.columnconfigure(0, weight=1)
        
        options = []
        if self.controller.auth_level != None:
            if self.controller.auth_level == 5:
                options = [" View "," Add "]
            else:
                options = [" View "]
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=options, 
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
        self.view_box.rowconfigure(1, weight=30)
        self.view_box.columnconfigure(0, weight=1)
        self.view_box.grid_remove()
        filaments = db.filaments.fetch_all()
        
        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=37,
                                              scrollbar_button_color=style.dark_foreground, scrollbar_button_hover_color=style.dark_foreground)
        header_frame.grid(row=0, column=0, sticky="nswe", padx=10,pady=0)
        header_frame._scrollbar.configure(height=0)
        table_header = ["ID", "Name", "Spool Weight (g)", "No."]
        weights = [1,3,3,2]
        for i in range(len(table_header)):
            header_frame.columnconfigure(i, weight=weights[i], uniform=0)
            frame = ctk.CTkFrame(header_frame, border_width=3, border_color=style.main_blue, corner_radius=8)
            frame.grid(row=0,column=i, ipadx=7, ipady=8, sticky="ew",padx=0)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)       
            label = ctk.CTkLabel(frame, text=table_header[i], font=(style.normal_font, 20, "bold"))
            label.grid(row=0,column=0) 
        
        table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in (1,3,3,2):
            table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in filaments:
            column_counter = 0
            for item in row:
                frame = ctk.CTkFrame(table_frame, corner_radius=0)
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
        #initialise add subpage
        self.add_box = ctk.CTkFrame(content_box,fg_color=style.dark_foreground)
        self.add_box.grid(row=0, column=0, sticky="nsew")
        self.add_box.columnconfigure(0, weight=1)
        self.add_box.rowconfigure(0, weight=1)
        self.add_box.rowconfigure(1, weight=1)
        self.add_box.grid_remove()
        self.material_name = ctk.StringVar()
        self.weight = ctk.StringVar(value="0")
        self.amount = ctk.StringVar(value="0")
        val_num = self.register(self.validate_num)
        
        form_frame = ctk.CTkFrame(self.add_box, fg_color=style.dark_foreground)
        form_frame.grid(row=0,column=0, sticky="n")
        name_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        name_frame.grid(row=0,column=0, padx=40, pady=(30,12),sticky="nw")
        name_frame.columnconfigure(1, weight=1)
        name_label = ctk.CTkLabel(name_frame, text="Material Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.material_name,
                                   font=(style.normal_font, 25), text_color="#f5f5f5", width=300)
        self.name_entry.grid(row=0, column=1)
        
        weight_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        weight_frame.grid(row=1,column=0, padx=(60,0), pady=15, sticky="nw")
        weight_frame.columnconfigure(1, weight=1)
        weight_label = ctk.CTkLabel(weight_frame, text="Spool Weight:", font=(style.normal_font, 20, "bold"), text_color="white")
        weight_label.grid(row=0, column=0, padx=(0,20))
        self.weight_entry = ctk.CTkEntry(weight_frame, textvariable=self.weight,
                                   font=(style.normal_font, 20), text_color="#f5f5f5", width=80,
                                   validate="key", validatecommand=(val_num, "%P"))
        self.weight_entry.grid(row=0, column=1)
        self.weight_entry.bind("<FocusOut>", lambda e: self.default_zero(self.weight))
        self.weight_entry.bind("<Return>", lambda e: self.default_zero(self.weight))
        
        amount_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        amount_frame.grid(row=2,column=0, padx=(60,0), pady=15, sticky="nw")
        amount_frame.columnconfigure(1, weight=1)
        amount_label = ctk.CTkLabel(amount_frame, text="No. available spools:", font=(style.normal_font, 20, "bold"), text_color="white")
        amount_label.grid(row=0, column=0, padx=(0,20))
        self.amount_entry = ctk.CTkEntry(amount_frame, textvariable=self.amount,
                                   font=(style.normal_font, 20), text_color="#f5f5f5", width=60,
                                   validate="key", validatecommand=(val_num, "%P"))
        self.amount_entry.grid(row=0, column=1)
        self.amount_entry.bind("<FocusOut>", lambda e: self.default_zero(self.amount))
        self.amount_entry.bind("<Return>", lambda e: self.default_zero(self.amount))
        
        buttons_frame = ctk.CTkFrame(self.add_box, fg_color=style.dark_foreground)
        buttons_frame.grid(row=1,column=0, sticky="s", pady=10)
        # reset form button
        reset_button = ctk.CTkButton(buttons_frame, width=70, height=30, fg_color="#FF2020", hover_color="#DA2020",
                                      text="Reset", font=(style.normal_font, 22), text_color="white",
                                      command=(lambda : self.reset_form()))
        reset_button.grid(row=0, column=0, padx=10)
        
        # submit form button
        submit_button = ctk.CTkButton(buttons_frame, width=100, height=35, fg_color=style.main_green, hover_color="#1d966c",
                                      text="Submit", font=(style.normal_font, 25, "bold"), text_color="white",
                                      command=(lambda : None))
        submit_button.grid(row=0, column=1, padx=10)
        
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
        
    def validate_num(self, num):
        return num.isdigit() or num == ""
    
    def default_zero(self, var):
        if var.get() == "":
            var.set(0)
            
    def submit_form(self):
        pass
    
    def reset_form(self):
        self.material_name.set("")
        self.weight.set(0)
        self.amount.set(0)