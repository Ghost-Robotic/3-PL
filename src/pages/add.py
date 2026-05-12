from turtle import title

import customtkinter as ctk
import style
import shutil
from PIL import Image, ImageTk

class Add(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.gcode_source = None
        self.file_name = ctk.StringVar()
        self.print_name = ctk.StringVar()
        self.duration = ctk.IntVar()
        self.weight = ctk.StringVar()
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
        self.hours = ctk.IntVar()
        self.mins = ctk.IntVar()
        self.slider_duration = ctk.IntVar()
        val_num = self.register(self.validate_num)
        val_min = self.register(self.validate_min)
        
        duration_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        duration_frame.grid(row=1, column=0, sticky="we")
        duration_label = ctk.CTkLabel(duration_frame, text="Print Duration:", font=(style.normal_font, 20, "bold"), text_color="white")
        duration_label.grid(row=0, column=0, padx=(0,20))
        
        duration_hours = ctk.CTkEntry(duration_frame, textvariable=self.hours,justify="center",
                                      font=(style.normal_font, 20), width=(16*3+4),
                                      validate="key", validatecommand=(val_num, "%P"))
        duration_hours.grid(row=0, column=1)
        duration_hours.bind("<KeyRelease>", lambda a:self.convert_dur_entry(a))
        duration_hours.bind("<FocusOut>", lambda e: self.default_zero(e,self.hours))
        duration_hours.bind("<Return>", lambda e: self.default_zero(e,self.hours))
        hr_label = ctk.CTkLabel(duration_frame, text="Hrs", font=(style.normal_font, 16, "bold"))
        hr_label.grid(row=0, column=2, padx=(5,10))
        
        duration_minutes = ctk.CTkEntry(duration_frame, textvariable=self.mins,justify="center",
                                      font=(style.normal_font, 20), width=(16*2+4),
                                      validate="key", validatecommand=(val_min, "%P"))
        duration_minutes.grid(row=0, column=3)
        duration_minutes.bind("<KeyRelease>", lambda a:self.convert_dur_entry(a))
        duration_minutes.bind("<FocusOut>", lambda e: self.default_zero(e,self.mins))
        duration_minutes.bind("<Return>", lambda e: self.default_zero(e,self.mins))
        min_label = ctk.CTkLabel(duration_frame, text="Mins", font=(style.normal_font, 16, "bold"))
        min_label.grid(row=0, column=4, padx=(5,0))
        
        self.duration_slider = ctk.CTkSlider(duration_frame, variable=self.slider_duration, 
                                             from_=0, to=2880, number_of_steps=576, width=300,
                                             command=lambda minutes: self.convert_slider(minutes))
        self.duration_slider.grid(row=1, column=0, columnspan=5, pady=(6,0))
        
        
#=====================================================================================================
        # set print weight
        weight_frame = ctk.CTkFrame(l_input_frame, fg_color=style.dark_foreground)
        weight_frame.grid(row=1, column=1, sticky="we")
        weight_label = ctk.CTkLabel(weight_frame, text="Weight:", font=(style.normal_font, 20, "bold"), text_color="white")
        weight_label.grid(row=0, column=0, padx=(0,20))
        
        weight_hours = ctk.CTkEntry(weight_frame, textvariable=self.weight,justify="center",
                                      font=(style.normal_font, 20), width=(16*4+4),
                                      validate="key", validatecommand=(val_num, "%P"))
        weight_hours.grid(row=0, column=1)
        weight_hours.bind("<FocusOut>", lambda e: self.default_zero(e,self.weight))
        weight_hours.bind("<Return>", lambda e: self.default_zero(e,self.weight))
        g_label = ctk.CTkLabel(weight_frame, text="g", font=(style.normal_font, 16, "bold"))
        g_label.grid(row=0, column=2, padx=(5,0))
        
#=====================================================================================================        
        # right side of form
        r_input_frame = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        r_input_frame.grid(row=0, column=1, sticky='nsew')
        r_input_frame.grid_columnconfigure(0, weight=1)
        r_input_frame.rowconfigure(0, weight=1)
        r_input_frame.rowconfigure(1, weight=1)
        
        # upload file button
        plus = ImageTk.PhotoImage((Image.open("assets\plus.png")).resize((100,100), Image.LANCZOS))
        self.add_file_button = ctk.CTkButton(r_input_frame, width=200, image=plus, height=200, anchor='center', corner_radius=18, text="",
                                    fg_color="#272727", border_color="white", border_width=3, hover_color=style.dark_foreground,
                                    command=(lambda : self.upload_file()))
        self.add_file_button.grid(row=0, column=0, padx=10,sticky="s")
        
        self.file_name = ctk.StringVar(value="*.gcode")
        file_label = ctk.CTkLabel(r_input_frame, textvariable=self.file_name, font=(style.normal_font, 18), text_color="white")
        file_label.grid(row=1, column=0, sticky="n")
        
        # reset form button
        reset_button = ctk.CTkButton(r_input_frame, width=88, height=45, fg_color="#FF2020", hover_color="#FA5C5C",
                                      text="Reset", font=(style.normal_font, 25), text_color="white",
                                      command=(lambda : None))
        reset_button.grid(row=2, column=0, sticky="s", pady=(20,10))
        
        # submit form button
        submit_button = ctk.CTkButton(r_input_frame, width=150, height=55, fg_color=style.main_green,
                                      text="Submit", font=(style.bold_font, 30), text_color="white",
                                      command=(lambda : None))
        submit_button.grid(row=3, column=0, sticky="s", pady=(10,40))
        
#=================================================================================================================================
    
    def upload_file(self):
        self.gcode_source = ctk.filedialog.askopenfilename(title="Select G-code file",filetypes=[("g-Code files","*.gcode")])

        if self.gcode_source is not "":
            grey_plus = ImageTk.PhotoImage((Image.open("assets\plusGrey.png")).resize((100,100), Image.LANCZOS))
            self.add_file_button.configure(fg_color=style.dark_foreground, border_color="#a7a7a7", image=grey_plus)
            
            name = ""
            counter = len(self.gcode_source)-1
            while self.gcode_source[counter] != "/" or counter == -1:
                name = self.gcode_source[counter] + name
                counter -= 1
            self.file_name.set(name)
            if self.print_title.get() == "":
                self.print_name.set(name[0:-6])
            
        
    def submit_form(self):
        self.duration = self.hours.get()*60 + self.mins.get()
        shutil.copy2(self.gcode_source, r"src\database\gcode")
        
    def convert_slider(self, minutes):
        self.hours.set(int(minutes//60))
        self.mins.set(int(minutes%60))
        
    def convert_dur_entry(self,a):
        total_duration = self.hours.get()*60 + self.mins.get()
        if total_duration <= (48*60):
            self.slider_duration.set(total_duration)
        else:
            self.slider_duration.set(48*60)
        
    def validate_num(self, num):
        return num.isdigit() or num == ""
        
    def validate_min(self, minutes):
        return (minutes.isdigit() and int(minutes)<60) or minutes == ""
    
    def default_zero(self, event, var):
        var.set(0)
        