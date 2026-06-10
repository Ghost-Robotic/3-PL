import customtkinter as ctk
import src.style as style
import src.helpers.popup_utils as pop


class PrintersPage(ctk.CTkFrame):
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
            if self.controller.auth_level >= 5:
                options = [" Printer Models "," Add Printer ", " Edit Printer "]
            else:
                options = [" Printer Models "]
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=options, 
                                               font=(style.normal_font, 22), text_color="white",
                                               selected_color=style.main_blue, selected_hover_color=style.hover_blue,
                                               border_width=0, corner_radius=10,
                                               command=self.switch_subpage)
        option_button.grid(row=0,column=0, sticky="w",padx=25)
        option_button.set(" Printer Models ")
        
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
        
        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=35,
                                              scrollbar_button_color=style.dark_foreground, scrollbar_button_hover_color=style.dark_foreground)
        header_frame.grid(row=0, column=0, sticky="nswe", padx=10,pady=0)
        header_frame._scrollbar.configure(height=0)
        table_header = ["ID", "Model Name", "Brand", "Multi-Material", "Compatible Filament"]
        self.weights = [2,5,5,3,4]
        for i in range(len(table_header)):
            header_frame.columnconfigure(i, weight=self.weights[i], uniform=0)
            frame = ctk.CTkFrame(header_frame, border_width=3, border_color=style.main_blue, corner_radius=8)
            frame.grid(row=0,column=i, ipadx=7, ipady=8, sticky="nsew",padx=0, pady=0)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)       
            label = ctk.CTkLabel(frame, text=table_header[i], font=(style.normal_font, 20, "bold"))
            label.grid(row=0,column=0) 
        
        models = self.controller.printer_models.fetch_table()
        for row in models:
            filaments = self.controller.printer_filament.fetch_filaments_names(printer_id=row[0])
            row.append(filaments)

        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        row_counter = 0
        for i in (2,5,5,3,4):
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in models:
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
                if column_counter == 3:
                    check = ctk.CTkCheckBox(frame, onvalue=1, offvalue=0,variable=ctk.IntVar(value=item),
                                            state=ctk.DISABLED, text="", width=0, fg_color=style.main_blue, border_color="white")
                    check.grid(row=0,column=0, padx=(10,0))
                elif column_counter == 4:
                    if item == []: item = ["None"]
                    check = ctk.CTkOptionMenu(frame, values=item, font=(style.normal_font, 17), anchor="center", button_color=style.main_blue,button_hover_color=style.main_blue, fg_color=style.main_blue)
                    check.grid(row=0,column=0, padx=(10,0))
                else:
                    label = ctk.CTkLabel(frame, text=item, font=(style.normal_font, 17))
                    label.grid(row=0,column=0)
                    if column_counter == 0: label.configure(font=(style.normal_font, 17,'bold'))
                column_counter += 1
            row_counter += 1
        
#=================================================================================
        #initialise add subpage
        self.add_box = ctk.CTkScrollableFrame(content_box,fg_color=style.dark_foreground)
        self.add_box.grid(row=0, column=0, sticky="nsew")
        self.add_box.columnconfigure(0, weight=1)
        self.add_box.rowconfigure(0, weight=1)
        self.add_box.rowconfigure(1, weight=1)
        self.add_box.grid_remove()
        self.brand = ctk.StringVar()
        self.model_name = ctk.StringVar()
        self.multi_material = ctk.BooleanVar()
        val_num = self.register(self.validate_num)
        
        form_frame = ctk.CTkFrame(self.add_box, fg_color=style.dark_foreground)
        form_frame.grid(row=0,column=0, sticky="n")
        
        add_title = ctk.CTkLabel(form_frame, text="Add new printer model:", font=(style.bold_font, 30), text_color=style.main_blue)
        add_title.grid(row=0, column=0, pady=20, sticky="w")
        
        brand_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        brand_frame.grid(row=1,column=0, padx=20, pady=(30,12),sticky="nw")
        brand_frame.columnconfigure(1, weight=1)
        brand_label = ctk.CTkLabel(brand_frame, text="Brand:", font=(style.normal_font, 22, "bold"), text_color="white")
        brand_label.grid(row=0, column=0, padx=(0,20))
        self.brand_entry = ctk.CTkEntry(brand_frame, textvariable=self.brand,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", width=300)
        self.brand_entry.grid(row=0, column=1)
        
        name_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        name_frame.grid(row=1,column=1, padx=20, pady=(30,12),sticky="nw")
        name_frame.columnconfigure(1, weight=1)
        name_label = ctk.CTkLabel(name_frame, text="Model:", font=(style.normal_font, 22, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.model_name,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", width=300)
        self.name_entry.grid(row=0, column=1)
        
        mm_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        mm_frame.grid(row=2,column=0, padx=40, pady=(30,12),sticky="nw")
        mm_label = ctk.CTkLabel(mm_frame, text="Multi-Material Capable:", font=(style.normal_font, 20, "bold"), text_color="white")
        mm_label.grid(row=0, column=0, padx=(30,20))
        mm_check = ctk.CTkCheckBox(mm_frame, variable=self.multi_material, text="", width=0, fg_color=style.main_blue, hover_color=style.hover_blue, border_color="white")
        mm_check.grid(row=0,column=1)
        
        self.filament_options = {}
        
        filament_frame = ctk.CTkFrame(form_frame, fg_color=style.dark_foreground)
        filament_frame.grid(row=2,column=1, padx=40, pady=(30,12), sticky="nw")
        select_label = ctk.CTkLabel(filament_frame, text="Select compatible filaments:", font=(style.normal_font, 20, "bold"), text_color="white")
        select_label.grid(row=0,column=0,sticky="nw", pady=(0,5))
        self.add_border_box = ctk.CTkFrame(filament_frame, fg_color=style.main_blue, corner_radius=10)
        self.add_border_box.grid(row=1,column=0, sticky="n")
        self.grid_scroll_options(frame=self.add_border_box, options=self.filament_options)
        
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
        
        self.all_models = self.controller.printer_models.fetch_all_models()
        self.avail_models = self.all_models
        
        self.edit_id = ctk.StringVar()
        self.edit_brand = ctk.StringVar()
        self.edit_model_name = ctk.StringVar()
        self.edit_multi_material = ctk.BooleanVar()
        self.edit_filament_options = {}
        
        val_id = self.register(self.validate_id)
        
        edit_frame = ctk.CTkFrame(self.edit_box, fg_color=style.dark_foreground)
        edit_frame.grid(row=0,column=0, sticky="n")
        
        title_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        title_frame.grid(row=0, column=0, pady=(0,10), sticky="w")
        add_title = ctk.CTkLabel(title_frame, text="Edit printer model:", font=(style.bold_font, 30), text_color=style.main_blue)
        add_title.grid(row=0, column=0, padx=(0,20), pady=(0,10), sticky="w")
        self.edit_dropdown = ctk.CTkComboBox(title_frame, values=self.avail_models,
                                                 width=300,font=(style.normal_font, 22, "bold"), text_color="yellow",
                                                 border_width=3, border_color=style.main_blue,
                                                 button_color=style.main_blue, button_hover_color=style.hover_blue,
                                                 command=(lambda model:self.select_model(model)))
        self.edit_dropdown.bind("<KeyRelease>", lambda e: 
            self.on_dropdown_update(self.edit_dropdown,self.all_models,self.avail_models))
        self.edit_dropdown.grid(row=0, column=1)
        self.edit_dropdown.set("")
        
        id_frame = ctk.CTkFrame(edit_frame,fg_color=style.dark_foreground)
        id_frame.grid(row=1, column=0, sticky="w", padx=20, pady=5)
        id_label = ctk.CTkLabel(id_frame, text="ID:", font=(style.normal_font, 25, "bold"), text_color="white")
        id_label.grid(row=0, column=0, padx=(0,20),pady=(0,5))
        id_entry = ctk.CTkEntry(id_frame, textvariable=self.edit_id, width=100,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", border_width=0, border_color=style.main_blue, fg_color=style.dark_foreground,
                                   validate="key", validatecommand=(val_id, "%P"), state="disabled")
        id_entry.grid(row=0, column=1)
        
        brand_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        brand_frame.grid(row=2,column=0, padx=20, pady=(0,12),sticky="nw")
        brand_frame.columnconfigure(1, weight=1)
        brand_label = ctk.CTkLabel(brand_frame, text="Brand:", font=(style.normal_font, 22, "bold"), text_color="white")
        brand_label.grid(row=0, column=0, padx=(0,20))
        self.brand_entry = ctk.CTkEntry(brand_frame, textvariable=self.edit_brand,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", width=300)
        self.brand_entry.grid(row=0, column=1)
        
        name_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        name_frame.grid(row=2,column=1, padx=20, pady=(30,12),sticky="nw")
        name_frame.columnconfigure(1, weight=1)
        name_label = ctk.CTkLabel(name_frame, text="Model:", font=(style.normal_font, 22, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.edit_model_name,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", width=300)
        self.name_entry.grid(row=0, column=1)
        
        mm_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        mm_frame.grid(row=3,column=0, padx=40, pady=(30,12),sticky="nw")
        mm_label = ctk.CTkLabel(mm_frame, text="Multi-Material Capable:", font=(style.normal_font, 20, "bold"), text_color="white")
        mm_label.grid(row=0, column=0, padx=(30,20))
        mm_check = ctk.CTkCheckBox(mm_frame, variable=self.edit_multi_material, text="", width=0, fg_color=style.main_blue, hover_color=style.hover_blue, border_color="white")
        mm_check.grid(row=0,column=1)
        
        filament_frame = ctk.CTkFrame(edit_frame, fg_color=style.dark_foreground)
        filament_frame.grid(row=3,column=1, padx=40, pady=(30,12), sticky="nw")
        select_label = ctk.CTkLabel(filament_frame, text="Select compatible filaments:", font=(style.normal_font, 20, "bold"), text_color="white")
        select_label.grid(row=0,column=0,sticky="nw", pady=(0,5))
        self.edit_border_box = ctk.CTkFrame(filament_frame, fg_color=style.main_blue, corner_radius=10)
        self.edit_border_box.grid(row=1,column=0, sticky="n")
        self.grid_scroll_options(frame=self.edit_border_box, options=self.edit_filament_options)
        
        buttons_frame = ctk.CTkFrame(self.edit_box, fg_color=style.dark_foreground)
        buttons_frame.grid(row=1,column=0, sticky="s", pady=10)
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
            case " Printer Models ":
                self.remove_add()
                self.remove_edit()
                self.grid_view()
            case " Add Printer ":
                self.remove_view()
                self.remove_edit()
                self.grid_add()
            case " Edit Printer ":
                self.remove_view()
                self.remove_add()
                self.grid_edit()
                
    
    # display subpage to view printers        
    def grid_view(self):
        self.view_box.grid()
        
    def update_view(self):
        self.table_frame.destroy()
        
        models = self.controller.printer_models.fetch_table()
        for row in models:
            filaments = self.controller.printer_filament.fetch_filaments_names(printer_id=row[0])
            row.append(filaments)

        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        row_counter = 0
        for i in (2,5,5,3,4):
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in models:
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
                if column_counter == 3:
                    check = ctk.CTkCheckBox(frame, onvalue=1, offvalue=0,variable=ctk.IntVar(value=item),
                                            state=ctk.DISABLED, text="", width=0, fg_color=style.main_blue, border_color="white")
                    check.grid(row=0,column=0, padx=(10,0))
                elif column_counter == 4:
                    if item == []: item = ["None"]
                    check = ctk.CTkOptionMenu(frame, values=item, font=(style.normal_font, 17), anchor="center", button_color=style.main_blue,button_hover_color=style.main_blue, fg_color=style.main_blue)
                    check.grid(row=0,column=0, padx=(10,0))
                else:
                    label = ctk.CTkLabel(frame, text=item, font=(style.normal_font, 17))
                    label.grid(row=0,column=0)
                    if column_counter == 0: label.configure(font=(style.normal_font, 17,'bold'))
                column_counter += 1
            row_counter += 1
    
    # hide subpage to view printers
    def remove_view(self):
        self.view_box.grid_remove()
    
    # display subpage to add printers
    def grid_add(self):
        self.reset_form()
        self.filaments = self.controller.filaments.list_id_names()
        for widget in self.add_border_box.winfo_children():
            widget.destroy()
        self.grid_scroll_options(frame=self.add_border_box, options=self.filament_options)
        self.add_box.grid()
        
    # hide subpage to add printers    
    def remove_add(self):
        self.add_box.grid_remove()
        
    # display subpage to edit printers
    def grid_edit(self):
        self.reset_edit()
        self.filaments = self.controller.filaments.list_id_names()
        for widget in self.add_border_box.winfo_children():
            widget.destroy()
        self.grid_scroll_options(frame=self.add_border_box, options=self.edit_filament_options)
        self.edit_box.grid()
        
    # hide subpage to edit printers    
    def remove_edit(self):
        self.edit_box.grid_remove()
        
    def validate_num(self, num):
        return num.isdigit() or num == ""
    
    def default_zero(self, var):
        if var.get() == "":
            var.set(0)
            
    def submit_form(self):
        """add new printer model"""
        models = self.controller.printer_models.fetch_all_names()
        check = [self.brand.get().strip()!="",
                 self.model_name.get().strip()!=""]
        try:
            
            if not (self.model_name.get().strip().lower() in models) and all(check):        
                self.controller.printer_models.add_printer_model(brand=self.brand.get(), model_name=self.model_name.get(), multimaterial=self.multi_material.get())
                
                compatible_fil = []
                for row in self.filament_options:
                    if row.get():
                        compatible_fil.append(self.filament_options.get(row))
                
                id = self.controller.printer_models.fetch_id(name=self.model_name.get())
                
                self.controller.printer_filament.add_relations(printer_id=id, material_ids=compatible_fil)
                
                self.reset_form()
                pop.show_success(self, self.controller)
                self.update_view()
            else:
                self.show_error()
        except Exception as e:
            print(e)
            self.show_error()
    
    def reset_form(self):
        self.filaments = self.controller.filaments.list_id_names()
        for widget in self.add_border_box.winfo_children():
            widget.destroy()
        self.filament_options = {}    
        self.grid_scroll_options(frame=self.add_border_box,options=self.filament_options)
        self.brand.set("")
        self.model_name.set("")
        self.multi_material.set(False)
        self.hide_error
        
    def submit_edit(self):
        """edit printer model"""
        check = [self.edit_brand.get().strip()!="",
                 self.edit_model_name.get().strip()!=""]
        try:
            if all(check):
                compatible_fil = []
                for row in self.edit_filament_options:
                    if row.get():
                        compatible_fil.append(self.edit_filament_options.get(row))                
                        
                self.controller.printer_models.edit_model(model_id=self.edit_id.get(),brand=self.edit_brand.get(), model_name=self.edit_model_name.get(), 
                                                          multimaterial=self.edit_multi_material.get(), material_ids=compatible_fil)
                                
                self.reset_edit()
                pop.show_success(self, self.controller)
                self.update_view()
            else:
                pop.show_error(self,"all fields must be filled")
        except Exception as e:
            print(e)
            pop.show_error(self,"unable to save")
    
    def reset_edit(self):
        self.filaments = self.controller.filaments.list_id_names()
        for widget in self.edit_border_box.winfo_children():
            widget.destroy()
        self.edit_filament_options = {}    
        self.grid_scroll_options(frame=self.edit_border_box,options=self.edit_filament_options)
        self.edit_id.set("")
        self.edit_brand.set("")
        self.edit_model_name.set("")
        self.edit_multi_material.set(0)
        self.edit_dropdown.set("")
        
    def grid_scroll_options(self, frame, options:dict):
        scroll_frame = ctk.CTkScrollableFrame(frame, fg_color=style.dark_foreground, width=300, height=300, corner_radius=10)
        scroll_frame.grid(row=0,column=0, sticky="nsew", padx=3,pady=3)
        
        self.filaments = self.controller.filaments.list_id_names()
        for row in self.filaments:
            checkbox = ctk.CTkCheckBox(scroll_frame, text=row[1], font=(style.normal_font, 15), fg_color=style.main_blue, hover_color=style.hover_blue, border_color="white")
            checkbox.pack(anchor="nw", pady=2)
            options.update({checkbox:row[0]})
            
        
    def validate_id(self, num):
        if len(str(num)) > 6:
            return False
        return num.isdigit() or num == ""
        
        
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
            
            check = [self.brand.get().strip()!="",
                    self.model_name.get().strip()!=""]
            models = self.controller.printer_models.fetch_all_names()
            
            if not all(check):
                error = ctk.CTkLabel(error_frame, text="all fields must be filled", font=(style.normal_font,20,"bold"), text_color="white")
                error.grid(row=0,column=0, padx=(15,0))   
            elif (self.model_name.get().strip().lower() in models):
                error = ctk.CTkLabel(error_frame, text="model already exists", font=(style.normal_font,20,"bold"), text_color="white")
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
        
        
    def select_model(self, account:str):
        self.edit_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue)
        
        id, other = account.split(" ", maxsplit=1)
        
        self.edit_id.set(id)
        self.edit_brand.set(self.controller.printer_models.fetch_brand(id))
        self.edit_model_name.set(self.controller.printer_models.fetch_model_name(id))
        self.edit_multi_material.set(self.controller.printer_models.is_mm(id))
        filaments = self.controller.printer_filament.fetch_filaments_id(printer_id=id)
        
        for checkbox, filament_id in self.edit_filament_options.items():
            #filament_id = self.edit_filament_options.get(row)
            if filament_id in filaments:
                checkbox.select()
            else:
                checkbox.deselect()