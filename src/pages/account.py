import customtkinter as ctk
import src.style as style
import src.database as db
import src.helpers.hash_utils as hsh
import src.helpers.popup_utils as pop
class AccountPage(ctk.CTkFrame):
    def __init__(self, parent, controller, parent_controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=(5,25))
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=50)

        
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
        self.profile_box.grid(row=0, column=0, sticky="nsew", ipadx=20, ipady=10, padx=30,pady=(10,0))
        #self.profile_box.rowconfigure(0, weight=1)
        #self.profile_box.rowconfigure(1, weight=1)
        #self.profile_box.columnconfigure(0, weight=1)
        self.profile_box.grid_remove()
        
        logout_button = ctk.CTkButton(content_box, command=(lambda : self.logout()), width=100, height=40, text="Logout", font=("Segoe UI Black", 30),
                                      fg_color=style.main_blue, hover_color=style.hover_blue,text_color="white")
        logout_button.grid(row=0,column=0,sticky="ne", padx=80, pady=10)
        
        
        name = (db.accounts.fetch_name(self.controller.current_user)).split()
        
        current_id = ctk.StringVar(value=self.controller.current_user)
        current_fname = ctk.StringVar(value=name[0])
        current_lname = ctk.StringVar(value=name[1])
        current_auth_level = ctk.StringVar(value=self.controller.auth_level)
        
        self.current_password = ctk.StringVar()
        self.new_pass = ctk.StringVar()
        self.new_pass2 = ctk.StringVar()
        
        profile_title = ctk.CTkLabel(self.profile_box, text="Profile", font=(style.bold_font, 30), text_color=style.main_blue)
        profile_title.grid(row=0, column=0, pady=20, sticky="w")
        
        id_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        id_frame.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        id_label = ctk.CTkLabel(id_frame, text="Your ID:", font=(style.normal_font, 25, "bold"), text_color="white")
        id_label.grid(row=0, column=0, padx=(0,20))
        id_entry = ctk.CTkLabel(id_frame, textvariable=current_id, width=100,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", state="disabled",anchor="w")
        id_entry.grid(row=0, column=1)
        
        username_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        username_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        fname_label = ctk.CTkLabel(username_frame, text="First Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        fname_label.grid(row=0, column=0, padx=(0,20))
        fname_entry = ctk.CTkLabel(username_frame, textvariable=current_fname,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", state="disabled",anchor="w")
        fname_entry.grid(row=0, column=1)
        lname_label = ctk.CTkLabel(username_frame, text="Last Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        lname_label.grid(row=0, column=2, padx=(40,20))
        lname_entry = ctk.CTkLabel(username_frame, textvariable=current_lname, width=300,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", state="disabled",anchor="w")
        lname_entry.grid(row=0, column=3)
        
        auth_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        auth_frame.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        auth_label = ctk.CTkLabel(auth_frame, text="Authentication Level:", font=(style.normal_font, 25, "bold"), text_color="white")
        auth_label.grid(row=0, column=0, padx=(0,20))
        auth_num = ctk.CTkLabel(auth_frame, textvariable=current_auth_level,font=(style.normal_font, 22, "bold"), text_color="yellow")
        auth_num.grid(row=0,column=1)
        # auth_entry = ctk.CTkEntry(auth_frame, textvariable=auth_level, width=26,
        #                            font=(style.normal_font, 22), text_color="#f5f5f5", state="disabled")
        # auth_entry.grid(row=0, column=1)
        
        # change password widget
        change_pass_frame = ctk.CTkFrame(self.profile_box,fg_color=style.dark_foreground)
        change_pass_frame.grid(row=4, column=0, sticky="w", pady=(30,0))
        pass_title = ctk.CTkLabel(change_pass_frame, text="Change Password", font=(style.bold_font, 27), text_color=style.main_blue)
        pass_title.grid(row=0, column=0, padx=(0,20), pady=10, sticky="w")
        
        entry_widget = ctk.CTkFrame(change_pass_frame,fg_color=style.dark_foreground)
        entry_widget.grid(row=1,column=0)
        pass_label = ctk.CTkLabel(entry_widget, text="Current Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        pass_label.grid(row=0, column=0, padx=(10,20), pady=10, sticky="e")
        pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.current_password, width=300, show="•",
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
        submit_button = ctk.CTkButton(button_widget, width=75, height=35, fg_color=style.main_green, hover_color=style.hover_green,
                                      text="Save", font=(style.normal_font, 25, "bold"), text_color="white",
                                      command=(lambda : self.save_new_pass()))
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
        self.weights = [1,5,5]
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
        for i in self.weights:
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in users:
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
        self.add_box = ctk.CTkScrollableFrame(content_box,fg_color=style.dark_foreground)
        self.add_box.grid(row=0, column=0, sticky="nsew")
        self.add_box.columnconfigure(0, weight=1)
        self.add_box.rowconfigure(0, weight=1)
        self.add_box.rowconfigure(1, weight=1)
        self.add_box.grid_remove()

        val_id = self.register(self.validate_id)
        
        form_frame = ctk.CTkFrame(self.add_box, fg_color=style.dark_foreground)
        form_frame.grid(row=0,column=0, sticky="n")
        
        self.id = ctk.StringVar()
        self.fname = ctk.StringVar()
        self.lname = ctk.StringVar()
        self.auth_level = ctk.IntVar(value=1)        
        self.password = ctk.StringVar()
        self.confirm_password = ctk.StringVar()

        profile_title = ctk.CTkLabel(form_frame, text="User Details:", font=(style.bold_font, 30), text_color=style.main_blue)
        profile_title.grid(row=0, column=0, pady=20, sticky="w")
        
        id_frame = ctk.CTkFrame(form_frame,fg_color=style.dark_foreground)
        id_frame.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        id_label = ctk.CTkLabel(id_frame, text="Your ID:", font=(style.normal_font, 25, "bold"), text_color="white")
        id_label.grid(row=0, column=0, padx=(0,20))
        id_entry = ctk.CTkEntry(id_frame, textvariable=self.id, width=100,
                                   font=(style.normal_font, 22, "bold"), text_color="yellow", validate="key", validatecommand=(val_id, "%P"))
        id_entry.grid(row=0, column=1)
        
        username_frame = ctk.CTkFrame(form_frame,fg_color=style.dark_foreground)
        username_frame.grid(row=2, column=0, sticky="w", padx=20, pady=10)
        fname_label = ctk.CTkLabel(username_frame, text="First Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        fname_label.grid(row=0, column=0, padx=(0,20))
        fname_entry = ctk.CTkEntry(username_frame, textvariable=self.fname, width=300,
                                   font=(style.normal_font, 22, "bold"), text_color="#f5f5f5")
        fname_entry.grid(row=0, column=1)
        lname_label = ctk.CTkLabel(username_frame, text="Last Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        lname_label.grid(row=0, column=2, padx=(40,20))
        lname_entry = ctk.CTkEntry(username_frame, textvariable=self.lname, width=300,
                                   font=(style.normal_font, 22, "bold"), text_color="#f5f5f5")
        lname_entry.grid(row=0, column=3)
        
        auth_frame = ctk.CTkFrame(form_frame,fg_color=style.dark_foreground)
        auth_frame.grid(row=3, column=0, sticky="w", padx=20, pady=10)
        auth_label = ctk.CTkLabel(auth_frame, text="Authentication Level:", font=(style.normal_font, 25, "bold"), text_color="white")
        auth_label.grid(row=0, column=0, padx=(0,20))
        # auth_entry = ctk.CTkEntry(auth_frame, textvariable=self.auth_level, width=30,
        #                            font=(style.normal_font, 22), text_color="#f5f5f5",validate="key", validatecommand=(val_auth, "%P"))
        # auth_entry.grid(row=0, column=1)
        self.auth_options = ctk.CTkOptionMenu(auth_frame, variable=self.auth_level, values=["1","2","3","4","5"],
                                         corner_radius=10, button_color=style.main_blue, button_hover_color=style.hover_blue,
                                         fg_color=style.main_blue, font=(style.normal_font, 22, "bold"), width=80,
                                         dropdown_font=(style.normal_font, 18))
        self.auth_options.grid(row=0,column=1)
        
        change_pass_frame = ctk.CTkFrame(form_frame,fg_color=style.dark_foreground)
        change_pass_frame.grid(row=4, column=0, sticky="w", pady=(30,0))
        pass_title = ctk.CTkLabel(change_pass_frame, text="Password:", font=(style.bold_font, 27), text_color=style.main_blue)
        pass_title.grid(row=0, column=0, padx=(10,20), pady=10, sticky="w")
        
        entry_widget = ctk.CTkFrame(change_pass_frame,fg_color=style.dark_foreground)
        entry_widget.grid(row=1,column=0, padx=20)

        add_pass_label = ctk.CTkLabel(entry_widget, text="Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        add_pass_label.grid(row=0, column=0, padx=(10,20), pady=(20,10), sticky="e")
        self.add_pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.password, width=300, show="•",
                                   font=(style.normal_font, 22), text_color="#f5f5f5", border_color=style.main_blue)
        self.add_pass_entry.bind("<KeyRelease>", lambda e: self.compare_pass())
        self.add_pass_entry.grid(row=0, column=1)
        
        c_add_pass_label = ctk.CTkLabel(entry_widget, text="Confirm Password:", font=(style.normal_font, 25, "bold"), text_color="white")
        c_add_pass_label.grid(row=1, column=0, padx=(10,20), sticky="e")
        self.c_add_pass_entry = ctk.CTkEntry(entry_widget, textvariable=self.confirm_password, width=300, show="•",
                                   font=(style.normal_font, 22), text_color="#f5f5f5", border_color=style.main_blue)
        self.c_add_pass_entry.bind("<KeyRelease>", lambda e: self.compare_pass())
        self.c_add_pass_entry.grid(row=1, column=1)
        
        
        buttons_frame = ctk.CTkFrame(self.add_box, fg_color=style.dark_foreground)
        buttons_frame.grid(row=1,column=0, sticky="s", pady=(30, 10))
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
        
    def update_view(self):
        self.table_frame.destroy()
        
        users = db.accounts.fetch_table()
        self.table_frame = ctk.CTkScrollableFrame(self.view_box, fg_color=style.dark_foreground)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=0)
        row_counter = 0
        for i in self.weights:
            self.table_frame.columnconfigure(row_counter, weight=i, uniform=0) 
            row_counter += 1
        row_counter = 0
        for row in users:
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
    
    # hide subpage to view all users
    def remove_view(self):
        self.view_box.grid_remove()
    
    # display subpage to add user
    def grid_add(self):
        self.add_box.grid()
        
    # hide subpage to add user    
    def remove_add(self):
        self.add_box.grid_remove()
        
    def validate_id(self, num):
        if len(str(num)) > 6:
            return False
        return num.isdigit() or num == ""
    
    def default_zero(self, var):
        if var.get() == "":
            var.set(0)
            
    def submit_form(self):
        ids = db.accounts.fetch_all_id()
        check = [len(self.id.get())==6,
                 self.fname.get()!="",
                 self.lname.get()!="",
                 self.password.get()==self.confirm_password.get(),
                 self.id.get() not in ids]
        
        try:
            if all(check):
                salt = hsh.generate_salt()
                db.accounts.create_user(user_id=self.id.get(), f_name=self.fname.get(),l_name=self.lname.get(),access_level=self.auth_level.get(), 
                                        password=(hsh.hash(self.password.get(),salt)), salt=salt)
                self.reset_form()
                pop.show_success(self, self.controller)
                self.update_view()
            else:
                    self.show_error()
        except Exception as e:
            print(e)
            self.show_error()
        
        
    
    def reset_form(self):
        for object in [self.id, self.fname,self.lname,self.password,self.confirm_password]:
            object.set("")
        self.auth_level.set(1)
        self.auth_options.set("1")
        self.add_pass_entry.configure(border_color=style.main_blue)
        self.c_add_pass_entry.configure(border_color=style.main_blue)
        self.hide_error()
        
    def save_new_pass(self):
        matched_password, salt = db.accounts.fetch_password(self.controller.current_user)
        # hashes given password
        hashed_password = hsh.hash(password=self.current_password.get(), salt=salt)
        if matched_password == hashed_password:
            if (self.new_pass.get() == self.new_pass2.get()) and self.new_pass.get()!="":
                new_salt = hsh.generate_salt()
                hashed_password = hsh.hash(password=self.new_pass.get(), salt=new_salt)
                db.accounts.change_password(id=self.controller.current_user,password=hashed_password, salt=new_salt)
                self.reset_pass()
                pop.show_success(self, self.controller)
                self.update_view()
            else:
                self.show_error(new_pass=2)
        else:
            self.show_error(new_pass=1)
    
    def reset_pass(self):
        self.current_password.set("")
        self.new_pass.set("")
        self.new_pass2.set("")
        self.new_pass_entry.configure(border_color=style.main_blue)
        self.new2_pass_entry.configure(border_color=style.main_blue)
        
    def compare_new_pass(self):
        if self.new_pass.get() == self.new_pass2.get():
            self.new_pass_entry.configure(border_color=style.main_blue)
            self.new2_pass_entry.configure(border_color=style.main_blue)
        else:
            self.new_pass_entry.configure(border_color="red")
            self.new2_pass_entry.configure(border_color="red")
            
    def compare_pass(self):
        if self.password.get() == self.confirm_password.get():
            self.add_pass_entry.configure(border_color=style.main_blue)
            self.c_add_pass_entry.configure(border_color=style.main_blue)
        else:
            self.add_pass_entry.configure(border_color="red")
            self.c_add_pass_entry.configure(border_color="red")
            
    def show_error(self, new_pass=0):
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
        

        check = [len(self.id.get())==6,
                 self.fname.get()!="",
                 self.lname.get()!=""]
        
        ids = db.accounts.fetch_all_id()
       
        if new_pass == 1:
            error = ctk.CTkLabel(error_frame, text="incorrect pasword", font=(style.normal_font,20,"bold"), text_color="white")
            error.grid(row=0,column=0, padx=(15,0))  
        elif new_pass == 2:
            error = ctk.CTkLabel(error_frame, text="passwords do not match", font=(style.normal_font,20,"bold"), text_color="white")
            error.grid(row=0,column=0, padx=(15,0))         
        elif not all(check):
            error = ctk.CTkLabel(error_frame, text="all fields must be filled", font=(style.normal_font,20,"bold"), text_color="white")
            error.grid(row=0,column=0, padx=(15,0))   
        elif self.id.get() in ids:
            error = ctk.CTkLabel(error_frame, text="user already exists", font=(style.normal_font,20,"bold"), text_color="white")
            error.grid(row=0,column=0, padx=(15,0))   
        elif self.password.get()!=self.confirm_password.get():
            error = ctk.CTkLabel(error_frame, text="passwords do not match", font=(style.normal_font,20,"bold"), text_color="white")
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
        
    def logout(self):
        self.controller.logout()