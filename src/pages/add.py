import customtkinter as ctk
import src.style as style
import shutil
from PIL import Image, ImageTk
import src.helpers.popup_utils as pop

class Add(ctk.CTkFrame):
    def __init__(self, parent, controller, parent_controller=None):
        self.controller = controller
        self.parent_controller = parent_controller
        self.gcode_source = None
        self.file_name = ctk.StringVar()
        self.print_name = ctk.StringVar()
        self.duration = ctk.IntVar()
        self.weight = ctk.IntVar()
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=25)
        container.grid_columnconfigure(0, weight=5)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
       
#================================================================================================== 
        # left side of form
        l_input_frame = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        l_input_frame.grid(row=0, column=0, sticky='nsew')
        l_input_frame.columnconfigure(0, weight=1)
        l_input_frame.columnconfigure(1, weight=1)
        
        title_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        title_frame.grid(row=0,column=0, sticky="we",pady=(0,30), columnspan=2)
        title_frame.columnconfigure(1, weight=1)
        name_label = ctk.CTkLabel(title_frame, text="Print Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.print_title = ctk.CTkEntry(title_frame, textvariable=self.print_name,
                                   font=(style.normal_font, 25), text_color="#f5f5f5", border_color=style.grey)
        self.print_title.grid(row=0, column=1, sticky="ew")
        
# =================================================================================================       
        # set print duration
        self.hours = ctk.StringVar(value="0")
        self.mins = ctk.StringVar(value="0")
        self.slider_duration = ctk.IntVar()
        val_num = self.register(self.validate_num)
        val_min = self.register(self.validate_min)
        
        duration_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        duration_frame.grid(row=1, column=0, sticky="we", padx=10, pady=10)
        duration_label = ctk.CTkLabel(duration_frame, text="Print Duration:", font=(style.normal_font, 20, "bold"), text_color="white")
        duration_label.grid(row=0, column=0, padx=(0,20))
        
        duration_hours = ctk.CTkEntry(duration_frame, textvariable=self.hours,justify="center",
                                      font=(style.normal_font, 20), text_color="white", width=(16*3+4),
                                      validate="key", validatecommand=(val_num, "%P"))
        duration_hours.grid(row=0, column=1)
        duration_hours.bind("<KeyRelease>", lambda a:self.convert_dur_entry(a))
        duration_hours.bind("<FocusOut>", lambda e: self.default_zero(e,self.hours))
        duration_hours.bind("<Return>", lambda e: self.default_zero(e,self.hours))
        hr_label = ctk.CTkLabel(duration_frame, text="Hrs", font=(style.normal_font, 16, "bold"))
        hr_label.grid(row=0, column=2, padx=(5,10))
        
        duration_minutes = ctk.CTkEntry(duration_frame, textvariable=self.mins,justify="center",
                                      font=(style.normal_font, 20), text_color="white", width=(16*2+4),
                                      validate="key", validatecommand=(val_min, "%P"))
        duration_minutes.grid(row=0, column=3)
        duration_minutes.bind("<KeyRelease>", lambda a:self.convert_dur_entry(a))
        duration_minutes.bind("<FocusOut>", lambda e: self.default_zero(e,self.mins))
        duration_minutes.bind("<Return>", lambda e: self.default_zero(e,self.mins))
        min_label = ctk.CTkLabel(duration_frame, text="Mins", font=(style.normal_font, 16, "bold"))
        min_label.grid(row=0, column=4, padx=(5,0))
        
        self.duration_slider = ctk.CTkSlider(duration_frame, variable=self.slider_duration, 
                                             from_=0, to=2880, number_of_steps=576, width=300,
                                             button_color=style.main_blue, progress_color=style.main_blue, button_hover_color=style.hover_blue,
                                             command=lambda minutes: self.convert_dur_slider(minutes))
        self.duration_slider.grid(row=1, column=0, columnspan=5, pady=(6,0))
        
        
#=====================================================================================================
        # set print weight
        self.slider_weight = ctk.IntVar()
        self.entry_weight = ctk.StringVar(value="0")
        
        weight_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        weight_frame.grid(row=1, column=1, sticky="we", padx=10, pady=10)
        weight_label = ctk.CTkLabel(weight_frame, text="Weight:", font=(style.normal_font, 20, "bold"), text_color="white")
        weight_label.grid(row=0, column=0, padx=(0,20))
        
        weight_entry = ctk.CTkEntry(weight_frame, textvariable=self.entry_weight,justify="center",
                                      font=(style.normal_font, 20), text_color="white", width=(16*4+4),
                                      validate="key", validatecommand=(val_num, "%P"))
        weight_entry.grid(row=0, column=1)
        weight_entry.bind("<KeyRelease>", lambda a:self.convert_weight_entry(a))
        weight_entry.bind("<FocusOut>", lambda e: self.default_zero(e,self.entry_weight))
        weight_entry.bind("<Return>", lambda e: self.default_zero(e,self.entry_weight))
        g_label = ctk.CTkLabel(weight_frame, text="g", font=(style.normal_font, 16, "bold"))
        g_label.grid(row=0, column=2, padx=(5,0))
        
        self.weight_slider = ctk.CTkSlider(weight_frame, variable=self.slider_weight, 
                                             from_=0, to=2000, number_of_steps=400, width=180,
                                             button_color=style.main_blue, progress_color=style.main_blue, button_hover_color=style.hover_blue,
                                             command=lambda weight: self.convert_weight_slider(weight))
        self.weight_slider.grid(row=1, column=0, columnspan=5, pady=(6,0))
        
#=====================================================================================================
        # set printer
        self.print_dict = self.controller.printer_models.fetch_name_brand()
        self.printer_list = list(self.print_dict.keys())
        self.avail_printers = self.printer_list
        
        printer_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        printer_frame.grid(row=2, column=0, sticky="we", padx=10, pady=(20,10))
        printer_label = ctk.CTkLabel(printer_frame, text="Select a printer below::", font=(style.normal_font, 20, "bold"), text_color="white")
        printer_label.grid(row=0, column=0)
        self.printer_dropdown = ctk.CTkComboBox(printer_frame, values=self.avail_printers,
                                            width=240,font=(style.normal_font, 20), text_color="white",
                                            border_width=3, border_color=style.main_blue,
                                            button_color=style.main_blue, button_hover_color=style.hover_blue,
                                            command=(lambda e:self.printer_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue)))
        self.printer_dropdown.bind("<KeyRelease>", lambda e: 
            self.on_dropdown_update(self.printer_dropdown,self.printer_list,self.avail_printers))
        self.printer_dropdown.grid(row=1, column=0, pady=(5,0))
        self.printer_dropdown.set("")


#=====================================================================================================
        # set filament
        self.filament_dict = self.controller.filaments.fetch_names()
        self.filament_list = list(self.filament_dict.keys())
        self.avail_filament = self.filament_list
        
        filament_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        filament_frame.grid(row=2, column=1, sticky="we", padx=10, pady=(20,10))
        filament_label = ctk.CTkLabel(filament_frame, text="Select a filament below::", font=(style.normal_font, 20, "bold"), text_color="white")
        filament_label.grid(row=0, column=0)
        self.filament_dropdown = ctk.CTkComboBox(filament_frame, values=self.avail_filament,
                                                 width=240,font=(style.normal_font, 20), text_color="white",
                                                 border_width=3, border_color=style.main_blue,
                                                 button_color=style.main_blue, button_hover_color=style.hover_blue,
                                                 command=(lambda e:self.filament_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue)))
        self.filament_dropdown.bind("<KeyRelease>", lambda e: 
            self.on_dropdown_update(self.filament_dropdown,self.filament_list,self.avail_filament))
        self.filament_dropdown.grid(row=1, column=0, pady=(5,0))
        self.filament_dropdown.set("")
        
#=====================================================================================================        
        # right side of form
        r_input_frame = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        r_input_frame.grid(row=0, column=1, sticky='nsew')
        r_input_frame.grid_columnconfigure(0, weight=1)
        r_input_frame.grid_columnconfigure(1, weight=1)
        r_input_frame.rowconfigure(0, weight=1)
        r_input_frame.rowconfigure(1, weight=1)
        
        # upload file button
        #self.plus = ImageTk.PhotoImage((Image.open(r"assets/plus.png")).resize((100,100), Image.LANCZOS))
        self.plus = ctk.CTkImage(dark_image=Image.open(r"assets/plus.png"),size=(100,100))
        self.add_file_button = ctk.CTkButton(r_input_frame, width=200, image=self.plus, height=200, anchor='center', corner_radius=18, text="",
                                    fg_color="#272727", border_color="white", border_width=3, hover_color=style.dark_foreground,
                                    command=(lambda : self.upload_file()))
        self.add_file_button.grid(row=0, column=0, padx=10,sticky="s",columnspan=2)
        
        self.file_name = ctk.StringVar(value="*.gcode")
        file_label = ctk.CTkLabel(r_input_frame, textvariable=self.file_name, font=(style.normal_font, 18), text_color="white")
        file_label.grid(row=1, column=0, sticky="n",columnspan=2)
        
        # reset form button
        reset_button = ctk.CTkButton(r_input_frame, width=88, height=45, fg_color="#FF2020", hover_color="#DA2020",
                                      text="Reset", font=(style.normal_font, 25), text_color="white",
                                      command=(lambda : self.reset_form()))
        reset_button.grid(row=2, column=0, sticky="se", pady=(20,14),padx=7)
        
        # submit form button
        submit_button = ctk.CTkButton(r_input_frame, width=140, height=53, fg_color=style.main_green, hover_color=style.hover_green,
                                      text="Save", font=(style.bold_font, 30), text_color="white",
                                      command=(lambda : self.submit_form()))
        submit_button.grid(row=2, column=1, sticky="sw", pady=(20,10),padx=7)
        
#=================================================================================================================================
    
    def upload_file(self):
        self.gcode_source = ctk.filedialog.askopenfilename(title="Select G-code file",filetypes=[("g-Code files","*.gcode")])

        if self.gcode_source != "":
            #grey_plus = ImageTk.PhotoImage((Image.open("assets/plusGrey.png")).resize((100,100), Image.LANCZOS))
            grey_plus = ctk.CTkImage(dark_image=Image.open(r"assets/plusGrey.png"),size=(100,100))
            self.add_file_button.configure(fg_color=style.dark_foreground, border_color="#a7a7a7", image=grey_plus)
            
            name = ""
            counter = len(self.gcode_source)-1
            while self.gcode_source[counter] != "/" or counter == -1:
                name = self.gcode_source[counter] + name
                counter -= 1
            self.file_name.set(name)
            if self.print_title.get() == "":
                self.print_name.set(name[0:-6])
                
    def validate(self):
        try:
            check = [self.print_name.get()!="",
                     self.file_name.get()!="",
                     self.file_name.get()!="*.gcode",
                     self.file_name.get()[-6:]==".gcode",
                     (int(self.hours.get())*60 + int(self.mins.get())) !=0,
                     int(self.entry_weight.get())!=0,
                     self.printer_dropdown.get() in self.printer_list,
                     self.filament_dropdown.get() in self.filament_list]
            if all(check):
                return True
        except:
            return False
            
        
    def submit_form(self):
        """add new print job to database"""
        if self.validate():
            try:
                self.duration = int(self.hours.get())*60 + int(self.mins.get())
                self.weight = int(self.entry_weight.get())
                printer_id = self.print_dict.get(self.printer_dropdown.get())
                filament_id = self.filament_dict.get(self.filament_dropdown.get())
                self.controller.logs.add_log(user_id=self.controller.current_user, print_name=self.print_name.get(), gcode=self.file_name.get(), 
                            duration=self.duration, weight=self.weight, 
                            printer_id=printer_id, filament_id=filament_id)
                
                shutil.copy2(str(self.gcode_source), r"database/gcode")
                self.reset_form() 
                pop.show_success(self, self.controller)
                self.parent_controller.update_view()
            except Exception as e:
                print(e)
                self.show_error()            
        else:
            self.show_error()
        
        
    def reset_form(self):
        strings = [self.print_name,self.printer_dropdown,self.filament_dropdown]
        integers = [self.hours,self.mins,self.slider_duration,self.entry_weight,self.slider_weight]
        
        for string in strings:
            string.set("")
            
        for integer in integers:
            integer.set(0)
        
        self.avail_printers = self.printer_list
        self.avail_filament = self.filament_list        
        
        self.printer_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue, values = self.avail_printers)
        self.filament_dropdown.configure(border_color=style.main_blue, button_color=style.main_blue, values=self.avail_filament)
        
        self.file_name.set("*.gcode")
        self.add_file_button.configure(image=self.plus,border_color="white")
        self.gcode_source = None
        
        self.hide_error()
        
    def convert_dur_slider(self, minutes):
        self.hours.set(str(int(minutes//60)))
        self.mins.set(str(int(minutes%60)))
        
    def convert_dur_entry(self,a):
        if self.hours.get() != "" and self.mins.get()!="":
            total_duration = int(self.hours.get())*60 + int(self.mins.get())
            if total_duration <= (48*60):
                self.slider_duration.set(total_duration)
            else:
                self.slider_duration.set(48*60)
            
    def convert_weight_slider(self, weight):
        self.entry_weight.set(int(weight))
        
    def convert_weight_entry(self, a):
        if self.entry_weight.get() != "":
            weight = int(self.entry_weight.get())
            if weight <= 2000:
                self.weight_slider.set(weight)
            else:
                self.weight_slider.set(2000)
        
    def validate_num(self, num):
        return (num.isdigit() and int(num)<1000000) or num == ""
        
    def validate_min(self, minutes):
        return (minutes.isdigit() and int(minutes)<60) or minutes == ""
    
    def default_zero(self, event, var):
        if var.get() == "":
            var.set(0)
        
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
            
            check = [self.print_name.get()!="",
                (int(self.hours.get())*60 + int(self.mins.get())) !=0,
                int(self.entry_weight.get())!=0,
                self.printer_dropdown.get() in self.printer_list,
                self.filament_dropdown.get() in self.filament_list]
            
            if not all(check):
                error = ctk.CTkLabel(error_frame, text="all fields must be filled", font=(style.normal_font,20,"bold"), text_color="white")
                error.grid(row=0,column=0, padx=(15,0))   
            elif self.file_name.get()=="*.gcode" or self.file_name.get()[-6:]!=".gcode":
                error = ctk.CTkLabel(error_frame, text="no gcode file", font=(style.normal_font,20,"bold"), text_color="white")
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