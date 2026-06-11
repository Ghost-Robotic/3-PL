import customtkinter as ctk
import src.style as style
import src.helpers.popup_utils as pop


class FilamentPage(ctk.CTkFrame):
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
            if self.controller.auth_level >= 4:
                options = [" Filament Materials "," Add Material "," Edit Material "]
            else:
                options = [" Filament Materials "]
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=options, 
                                               font=(style.normal_font, 22), text_color="white",
                                               selected_color=style.main_blue, selected_hover_color=style.hover_blue,
                                               border_width=0, corner_radius=10,
                                               command=self.switch_subpage)
        option_button.grid(row=0,column=0, sticky="w",padx=25)
        option_button.set(" Filament Materials ")
        
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
        filaments = self.controller.filaments.fetch_all()
        
        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=37,
                                              scrollbar_button_color=style.dark_foreground, scrollbar_button_hover_color=style.dark_foreground)
        header_frame.grid(row=0, column=0, sticky="nswe", padx=10,pady=0)
        header_frame._scrollbar.configure(height=0)
        table_header = ["ID", "Name", "Spool Weight (g)", "No."]
        self.weights = [1,3,3,2]
        for i in range(len(table_header)):
            header_frame.columnconfigure(i, weight=self.weights[i], uniform=0)
            frame = ctk.CTkFrame(header_frame, border_width=3, border_color=style.main_blue, corner_radius=8)
            frame.grid(row=0,column=i, ipadx=7, ipady=8, sticky="ew",padx=0)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)       
            label = ctk.CTkLabel(frame, text=table_header[i], font=(style.normal_font, 20, "bold"))
            label.grid(row=0,column=0) 
        
        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in (1,3,3,2):
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in filaments:
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
        submit_button = ctk.CTkButton(buttons_frame, width=100, height=35, fg_color=style.main_green, hover_color=style.hover_green,
                                      text="Save", font=(style.normal_font, 25, "bold"), text_color="white",
                                      command=(lambda : self.submit_form()))
        submit_button.grid(row=0, column=1, padx=10)
        
#=================================================================================
        # edit page
        self.edit_box = ctk.CTkScrollableFrame(content_box,fg_color=style.dark_foreground)
        self.edit_box.grid(row=0, column=0, sticky="nsew")
        self.edit_box.columnconfigure(0, weight=1)
        self.edit_box.rowconfigure(0, weight=1)
        self.edit_box.rowconfigure(1, weight=1)
        self.edit_box.grid_remove()
        
        self.all_materials = self.controller.filaments.fetch_all_filaments()
        self.avail_materials = self.all_materials
        
        self.edit_id = ctk.StringVar()
        self.edit_material_name = ctk.StringVar()
        self.edit_weight = ctk.StringVar()
        self.edit_amount = ctk.StringVar()
        val_num = self.register(self.validate_num)
        
        edit_frame = ctk.CTkFrame(self.edit_box, fg_color=style.dark_foreground)
        edit_frame.grid(row=0,column=0, sticky="n")
        
        title_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        title_frame.grid(row=0, column=0, pady=20, sticky="w")
        profile_title = ctk.CTkLabel(title_frame, text="Edit Material:", font=(style.bold_font, 30), text_color=style.main_blue)
        profile_title.grid(row=0, column=0, padx=(0,20))
        self.edit_dropdown = ctk.CTkComboBox(title_frame, values=self.avail_materials,
                                                 width=300,font=(style.normal_font, 22, "bold"), text_color="yellow",
                                                 border_width=3, border_color=style.main_blue,
                                                 button_color=style.main_blue, button_hover_color=style.hover_blue,
                                                 command=(lambda e:self.select_filament()))
        self.edit_dropdown.bind("<KeyRelease>", lambda e: 
            self.on_dropdown_update(self.edit_dropdown,self.all_materials,self.avail_materials))
        self.edit_dropdown.grid(row=0, column=1)
        self.edit_dropdown.set("")
        
        id_frame = ctk.CTkFrame(edit_frame,fg_color=style.dark_foreground)
        id_frame.grid(row=1, column=0, sticky="w", padx=40, pady=(10,0))
        id_label = ctk.CTkLabel(id_frame, text="ID:", font=(style.normal_font, 25, "bold"), text_color="white")
        id_label.grid(row=0, column=0, padx=(0,20))
        id_entry = ctk.CTkEntry(id_frame, textvariable=self.edit_id, width=100,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", border_width=0, border_color=style.main_blue, fg_color=style.dark_foreground,
                                   state="disabled")
        id_entry.grid(row=0, column=1)
        
        name_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        name_frame.grid(row=2,column=0, padx=40, pady=(10,12),sticky="nw")
        name_frame.columnconfigure(1, weight=1)
        name_label = ctk.CTkLabel(name_frame, text="Material Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.edit_material_name,
                                   font=(style.normal_font, 25), text_color="#f5f5f5", width=300)
        self.name_entry.grid(row=0, column=1)
        
        weight_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        weight_frame.grid(row=3,column=0, padx=(60,0), pady=15, sticky="nw")
        weight_frame.columnconfigure(1, weight=1)
        weight_label = ctk.CTkLabel(weight_frame, text="Spool Weight:", font=(style.normal_font, 20, "bold"), text_color="white")
        weight_label.grid(row=0, column=0, padx=(0,20))
        self.edit_weight_entry = ctk.CTkEntry(weight_frame, textvariable=self.edit_weight,
                                   font=(style.normal_font, 20), text_color="#f5f5f5", width=80,
                                   validate="key", validatecommand=(val_num, "%P"))
        self.edit_weight_entry.grid(row=0, column=1)
        self.edit_weight_entry.bind("<FocusOut>", lambda e: self.default_zero(self.edit_weight))
        self.edit_weight_entry.bind("<Return>", lambda e: self.default_zero(self.edit_weight))
        
        amount_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        amount_frame.grid(row=4,column=0, padx=(60,0), pady=15, sticky="nw")
        amount_frame.columnconfigure(1, weight=1)
        amount_label = ctk.CTkLabel(amount_frame, text="No. available spools:", font=(style.normal_font, 20, "bold"), text_color="white")
        amount_label.grid(row=0, column=0, padx=(0,20))
        self.amount_entry = ctk.CTkEntry(amount_frame, textvariable=self.edit_amount,
                                   font=(style.normal_font, 20), text_color="#f5f5f5", width=60,
                                   validate="key", validatecommand=(val_num, "%P"))
        self.amount_entry.grid(row=0, column=1)
        self.amount_entry.bind("<FocusOut>", lambda e: self.default_zero(self.edit_amount))
        self.amount_entry.bind("<Return>", lambda e: self.default_zero(self.edit_amount))
        
        buttons_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        buttons_frame.grid(row=5,column=0, sticky="n", pady=30)
        # reset form button
        reset_button = ctk.CTkButton(buttons_frame, width=70, height=30, fg_color="#FF2020", hover_color="#DA2020",
                                      text="Reset", font=(style.normal_font, 22), text_color="white",
                                      command=(lambda : self.reset_edit()))
        reset_button.grid(row=0, column=0, padx=10)
        
        # submit form button
        submit_button = ctk.CTkButton(buttons_frame, width=100, height=35, fg_color=style.main_green, hover_color=style.hover_green,
                                      text="Save", font=(style.normal_font, 25, "bold"), text_color="white",
                                      command=(lambda : self.submit_edit()))
        submit_button.grid(row=0, column=1, padx=10)
        
#=================================================================================
        
        self.grid_view()
#=================================================================================
    def switch_subpage(self,page):
        match page:
            case " Filament Materials ":
                self.remove_add()
                self.remove_edit()
                self.grid_view()
            case " Add Material ":
                self.remove_view()
                self.remove_edit()
                self.grid_add()
            case " Edit Material ":
                self.remove_view()
                self.remove_add()
                self.grid_edit()
    
    # display subpage to view filaments        
    def grid_view(self):
        self.view_box.grid()
        
    def update_view(self):
        """refresh view table"""
        self.table_frame.destroy()
        
        filaments = self.controller.filaments.fetch_all()
        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in (1,3,3,2):
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in filaments:
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
    
    # hide subpage to view filaments
    def remove_view(self):
        self.view_box.grid_remove()
    
    # display subpage to add filaments
    def grid_add(self):
        self.add_box.grid()
        
    # hide subpage to add filaments    
    def remove_add(self):
        self.add_box.grid_remove()
    
    # display subpage to edit filaments    
    def grid_edit(self):
        self.edit_box.grid()
        
    # hide subpage to edit filaments    
    def remove_edit(self):
        self.edit_box.grid_remove()
        
    def validate_num(self, num):
        return (num.isdigit() and int(num)<1000000) or num == ""
    
    def default_zero(self, var):
        if var.get() == "":
            var.set(0)
            
    def submit_form(self):
        """add new material to database"""
        materials = list(self.controller.filaments.fetch_names().keys())
        
        check = [self.material_name.get().strip()!="",
                 self.weight.get().strip()!=0,
                 self.weight.get().strip()!=""]
        
        exist = False
        for material in materials:
            if material.lower() == self.material_name.get().strip().lower():
                exist = True
        
        try:
            if not exist and all(check):
                self.controller.filaments.add_filament(material=self.material_name.get(), weight=self.weight.get(), amount=self.amount.get())
                self.reset_form()
                pop.show_success(self, self.controller)
                self.update_view()
            else:
                self.show_error()
        except Exception as e:
            print(e)
            self.show_error()
    
    def reset_form(self):
        self.material_name.set("")
        self.weight.set(0)
        self.amount.set(0)
        self.hide_error()
        
    def submit_edit(self):
        """save edit form to database"""
        try:
            check = [self.edit_material_name.get().strip() !="",
                    self.edit_weight.get().strip() != "",
                    self.edit_amount.get().strip() != ""]
            
            if all(check):
                self.controller.filaments.edit_filament(filament_id=self.edit_id.get().strip(),material=self.edit_material_name.get().strip(),weight=self.edit_weight.get().strip(),amount=self.edit_amount.get().strip())
                pop.show_success(self, self.controller)
                self.reset_edit()
                self.update_view()
            else:
                pop.show_error(self,"all fields must be filled")
        except Exception as e:
            print(e)
            pop.show_error(self,"unable to save")
    
    def reset_edit(self):
        """reset edit form fields"""
        self.edit_dropdown.set("")
        self.edit_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue)
        self.edit_id.set("")
        self.edit_material_name.set("")
        self.edit_weight.set("")
        self.edit_amount.set("")
    
    def select_filament(self):
        id = str(self.edit_dropdown.get()).split(" ", maxsplit=1)[0]
        
        self.edit_id.set(id)
        self.edit_material_name.set(self.controller.filaments.fetch_name(id))
        self.edit_weight.set(self.controller.filaments.fetch_weight(id))
        self.edit_amount.set(self.controller.filaments.fetch_amount(id))
        
        
    def on_dropdown_update(self, dropdown, master_list, current_list):
        value = dropdown.get()
        if current_list != []:
            if dropdown.get() not in master_list:
                dropdown.configure(border_color="red", button_color="red")
            else:
                dropdown.configure(border_color=style.main_blue, button_color=style.main_blue)
            current_list = []
            for i in master_list:
                if value.lower() in i.lower():
                    current_list.append(i)
        else:
            current_list = master_list
    
        dropdown.configure(values=current_list)
    
    def show_error(self):
        if len(self.winfo_children()) <= 1:
            self.error_cont = ctk.CTkFrame(self, border_width=3, border_color="red",corner_radius=10, width=400, height=100)
            self.error_cont.grid(row=0, column=0)
            self.error_cont.rowconfigure(0,weight=1)
            self.error_cont.rowconfigure(1,weight=5)
            self.error_cont.columnconfigure(0,weight=1)
            
            topbar = ctk.CTkFrame(self.error_cont, fg_color="#242323", corner_radius=10)
            topbar.grid(row=0,column=0,sticky="new",padx=5,pady=5)
            error_label = ctk.CTkLabel(topbar, text="ERROR: ", font=(style.normal_font,25,"bold"), text_color="red", width=370, anchor="w")
            error_label.grid(row=0,column=0, padx=(10,0),pady=7, sticky="nw")
            
            close_button = ctk.CTkButton(topbar, text="X", font=(style.normal_font,20,"bold"), text_color="white",
                                        hover_color="red", fg_color="#242323",width=30,height=30,
                                        command=(lambda : self.hide_error()))
            close_button.grid(row=0,column=1, sticky="se", padx=7,pady=7)
            
            error_frame = ctk.CTkFrame(self.error_cont, fg_color=style.dark_background, width=500, height=100)
            error_frame.grid(row=1, column=0, sticky="nsew",padx=5,pady=5)
            error_frame.columnconfigure(0,weight=1)
            
            check = [self.material_name.get().strip()!="",
                    self.weight.get().strip()!=0,
                    self.weight.get().strip()!=""]
            materials = list(self.controller.filaments.fetch_names().keys())
            exist = False
            for material in materials:
                if material.lower() == self.material_name.get().strip().lower():
                    exist = True
            
            if not all(check):
                error = ctk.CTkLabel(error_frame, text="all fields must be filled", font=(style.normal_font,20,"bold"), text_color="white")
                error.grid(row=0,column=0, padx=(15,0))   
            elif exist:
                error = ctk.CTkLabel(error_frame, text="material already exists", font=(style.normal_font,20,"bold"), text_color="white")
                error.grid(row=0,column=0, padx=(15,0))   
            else:
                error = ctk.CTkLabel(error_frame, text="unable to save", font=(style.normal_font,20,"bold"), text_color="white")
                error.grid(row=0,column=0, padx=(15,0))
            
            okay_button = ctk.CTkButton(error_frame, text="Okay", font=(style.normal_font,22,"bold"),
                                        border_color=style.main_blue, border_width=2,hover_color=style.main_blue, fg_color=style.dark_background,width=50,
                                        command=(lambda : self.hide_error()))
            okay_button.grid(row=1,column=1, sticky="se", padx=10,pady=10)
        
    def hide_error(self):
        try:
            self.error_cont.destroy()
        except:
            pass