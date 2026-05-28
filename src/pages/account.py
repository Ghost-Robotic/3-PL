import customtkinter as ctk
import src.style as style
import src.database as db
class AccountPage(ctk.CTkFrame):
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
                options = [" Profile ", " All Users "," Add New Account "]
            elif self.controller.auth_level >= 4:
                options = [" Profile ", " All Users "]
            else:
                options = [" Profile "]
        option_button = ctk.CTkSegmentedButton(topbar, width=200, values=options, 
                                               font=(style.normal_font, 22), text_color="white",
                                               selected_color=style.main_blue, selected_hover_color=style.hover_blue,
                                               border_width=0, corner_radius=10,
                                               command=self.switch_subpage)
        option_button.grid(row=0,column=0, sticky="w",padx=25)
        option_button.set(" Profile ")
        
        line = ctk.CTkFrame(topbar, height=5, fg_color="#585858")
        line.grid(row=1,column=0, sticky="we", padx=10, pady=(10,0))

        content_box = ctk.CTkFrame(container,fg_color=style.dark_foreground)
        content_box.grid(row=1, column=0, sticky="nsew")
        content_box.rowconfigure(0, weight=1)
        content_box.columnconfigure(0, weight=1)

#=================================================================================
        # initialise profile subpage
        self.profile_box = ctk.CTkScrollableFrame(content_box,fg_color=style.dark_foreground)
        self.profile_box.grid(row=0, column=0, sticky="nsew", ipadx=20, ipady=10, padx=30)
        #self.profile_box.rowconfigure(0, weight=1)
        #self.profile_box.rowconfigure(1, weight=1)
        #self.profile_box.columnconfigure(0, weight=1)
        self.profile_box.grid_remove()
        
        name = (db.accounts.fetch_name(self.controller.current_user)).split()
        
        id = ctk.StringVar(value=self.controller.current_user)
        fname = ctk.StringVar(value=name[0])
        lname = ctk.StringVar(value=name[1])
        auth_level = ctk.StringVar(value=self.controller.auth_level)
        
        self.password = ctk.StringVar()
        self.new_pass = ctk.StringVar()
        self.new_pass2 = ctk.StringVar()
        
        profile_title = ctk.CTkLabel(self.profile_box, text="Profile", font=(style.bold_font, 30), text_color=style.main_blue)
        profile_title.grid(row=0, column=0, pady=20, sticky="w")
        
        id_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        id_frame.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        id_label = ctk.CTkLabel(id_frame, text="Your ID:", font=(style.normal_font, 25, "bold"), text_color="white")
        id_label.grid(row=0, column=0, padx=(0,20))
        id_entry = ctk.CTkEntry(id_frame, textvariable=id, width=88,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", state="disabled")
        id_entry.grid(row=0, column=1)
        
        username_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        username_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        fname_label = ctk.CTkLabel(username_frame, text="First Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        fname_label.grid(row=0, column=0, padx=(0,20))
        fname_entry = ctk.CTkEntry(username_frame, textvariable=fname, width=300,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", state="disabled")
        fname_entry.grid(row=0, column=1)
        lname_label = ctk.CTkLabel(username_frame, text="Last Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        lname_label.grid(row=0, column=2, padx=(40,20))
        lname_entry = ctk.CTkEntry(username_frame, textvariable=lname, width=300,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", state="disabled")
        lname_entry.grid(row=0, column=3)
        
        auth_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        auth_frame.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        auth_label = ctk.CTkLabel(auth_frame, text="Authentication Level:", font=(style.normal_font, 25, "bold"), text_color="white")
        auth_label.grid(row=0, column=0, padx=(0,20))
        auth_entry = ctk.CTkEntry(auth_frame, textvariable=auth_level, width=26,
                                   font=(style.normal_font, 22), text_color="#f5f5f5", state="disabled")
        auth_entry.grid(row=0, column=1)
        
        # change password widget
        change_pass_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        change_pass_frame.grid(row=4, column=0, sticky="w", pady=(30,0))
        pass_title = ctk.CTkLabel(change_pass_frame, text="Change Password", font=(style.bold_font, 27), text_color=style.main_blue)
        pass_title.grid(row=0, column=0, padx=(0,20), pady=10, sticky="w")
        
        entry_widget = ctk.CTkFrame(change_pass_frame,fg_color=style.dark_foreground)
        entry_widget.grid(row=1,column=0)
        pass_label = ctk.CTkLabel(entry_widget, text="Current Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        pass_label.grid(row=0, column=0, padx=(10,20), pady=10, sticky="e")
        pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.password, width=300, show="•",
                                   font=(style.normal_font, 22), text_color="#f5f5f5", border_color=style.main_blue)
        pass_entry.grid(row=0, column=1)
        
        new_pass_label = ctk.CTkLabel(entry_widget, text="New Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        new_pass_label.grid(row=1, column=0, padx=(10,20), pady=(20,10), sticky="e")
        self.new_pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.new_pass, width=300, show="•",
                                   font=(style.normal_font, 22), text_color="#f5f5f5", border_color=style.main_blue)
        self.new_pass_entry.bind("<KeyRelease>", lambda e: self.compare_new_pass())
        self.new_pass_entry.grid(row=1, column=1)
        
        new2_pass_label = ctk.CTkLabel(entry_widget, text="Confirm New Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        new2_pass_label.grid(row=2, column=0, padx=(10,20), sticky="e")
        self.new2_pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.new_pass2, width=300, show="•",
                                   font=(style.normal_font, 22), text_color="#f5f5f5", border_color=style.main_blue)
        self.new2_pass_entry.bind("<KeyRelease>", lambda e: self.compare_new_pass())
        self.new2_pass_entry.grid(row=2, column=1)
        
        button_widget = ctk.CTkFrame(change_pass_frame,fg_color=style.dark_foreground)
        button_widget.grid(row=2,column=0, pady=10)
        
        reset_button = ctk.CTkButton(button_widget, width=70, height=30, fg_color="#FF2020", hover_color="#DA2020",
                                      text="Reset", font=(style.normal_font, 22), text_color="white",
                                      command=(lambda : self.reset_pass()))
        reset_button.grid(row=0, column=0, padx=10)
        
        # submit form button
        submit_button = ctk.CTkButton(button_widget, width=75, height=35, fg_color=style.main_green, hover_color="#1d966c",
                                      text="Save", font=(style.normal_font, 25, "bold"), text_color="white",
                                      command=(lambda : None))
        submit_button.grid(row=0, column=1, padx=10)

#=================================================================================
        # initialise view subpage
        self.view_box = ctk.CTkFrame(content_box,fg_color=style.dark_foreground)
        self.view_box.grid(row=0, column=0, sticky="nsew", ipadx=10, ipady=10)
        self.view_box.rowconfigure(0, weight=1)
        self.view_box.rowconfigure(1, weight=30)
        self.view_box.columnconfigure(0, weight=1)
        self.view_box.grid_remove()
        users = db.accounts.fetch_table()

        header_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground, height=37,
                                              scrollbar_button_color=style.dark_foreground, scrollbar_button_hover_color=style.dark_foreground)
        header_frame.grid(row=0, column=0, sticky="nswe", padx=10,pady=0)
        header_frame._scrollbar.configure(height=0)
        table_header = ["ID", "Name", "Authentication Level"]
        weights = [1,5,5]
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
        for i in weights:
            table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in users:
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
        
        self.grid_profile()
#=================================================================================
    def switch_subpage(self,page):
        match page:
            case " Profile ":
                self.remove_add()
                self.remove_view()
                self.grid_profile()
            case " All Users ":   
                self.remove_add()
                self.remove_profile()
                self.grid_view()
            case " Add New Account ":
                self.remove_view()
                self.remove_profile()
                self.grid_add()
            
    
    # display subpage to view current user profile
    def grid_profile(self):
        self.profile_box.grid()
    
    # hide subpage to view current user profile
    def remove_profile(self):
        self.profile_box.grid_remove()
    
    # display subpage to view all users        
    def grid_view(self):
        self.view_box.grid()
    
    # hide subpage to view all users
    def remove_view(self):
        self.view_box.grid_remove()
    
    # display subpage to add user
    def grid_add(self):
        self.add_box.grid()
        
    # hide subpage to add user    
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
        
    def save_pass(self):
        pass
    
    def reset_pass(self):
        self.password.set("")
        self.new_pass.set("")
        self.new_pass2.set("")
        
    def compare_new_pass(self):
        if self.new_pass.get() == self.new_pass2.get():
            self.new_pass_entry.configure(border_color=style.main_blue)
            self.new2_pass_entry.configure(border_color=style.main_blue)
        else:
            self.new_pass_entry.configure(border_color="red")
            self.new2_pass_entry.configure(border_color="red")