import customtkinter as ctk
import style
import shutil
from PIL import Image, ImageTk

class Add(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.gcode_source = None
        self.file_name = ctk.StringVar()
        self.print_name = ctk.StringVar()
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_foreground)
        
        container = ctk.CTkFrame(self, fg_color=style.dark_foreground)
        container.grid(row=0, column=0, sticky='nsew', padx=25, pady=25)
        container.grid_columnconfigure(0, weight=5)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        # left side of form
        l_input_frame = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        l_input_frame.grid(row=0, column=0, sticky='nsew')
        l_input_frame.columnconfigure(1, weight=1)
        
        name_label = ctk.CTkLabel(l_input_frame, text="Print Name:", font=(style.normal_font, 25, "bold"), text_color="white")
        name_label.grid(row=0, column=0, padx=(0,20))
        self.print_title = ctk.CTkEntry(l_input_frame, textvariable=self.print_name,
                                   font=(style.normal_font, 25), text_color="#f5f5f5", border_color=style.grey)
        self.print_title.grid(row=0, column=1, sticky="ew")
        
        # right side of form
        r_input_frame = ctk.CTkFrame(container, fg_color=style.dark_foreground)
        r_input_frame.grid(row=0, column=1, sticky='nsew')
        r_input_frame.grid_columnconfigure(0, weight=1)
        r_input_frame.grid_rowconfigure(2, weight=1)
        
        # upload file button
        plus = ImageTk.PhotoImage((Image.open("assets\plus.png")).resize((100,100), Image.LANCZOS))
        self.add_file_button = ctk.CTkButton(r_input_frame, width=200, image=plus, height=200, anchor='center', corner_radius=18, text="",
                                    fg_color="#272727", border_color="white", border_width=3, hover_color=style.dark_foreground,
                                    command=(lambda : self.upload_file()))
        self.add_file_button.grid(row=0, column=0, padx=10, pady=(60,10), sticky="n")
        
        self.file_name = ctk.StringVar(value="*.gcode")
        file_label = ctk.CTkLabel(r_input_frame, textvariable=self.file_name, font=(style.normal_font, 18), text_color="white")
        file_label.grid(row=1, column=0, sticky="n")
        
        # reset form button
        reset_button = ctk.CTkButton(r_input_frame, width=88, height=45, fg_color="#FF2020",
                                      text="Reset", font=(style.normal_font, 25), text_color="white",
                                      command=(lambda : None))
        reset_button.grid(row=3, column=0, sticky="s", pady=(20,10))
        
        # submit form button
        submit_button = ctk.CTkButton(r_input_frame, width=150, height=55, fg_color=style.main_green,
                                      text="Submit", font=(style.bold_font, 30), text_color="white",
                                      command=(lambda : None))
        submit_button.grid(row=4, column=0, sticky="s", pady=(10,40))
    
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
        shutil.copy2(self.gcode_source, "src\database\gcode")
        
        
