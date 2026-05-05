import customtkinter as ctk
import shutil

source = ctk.filedialog.askopenfilename(title="Select G-code File",filetypes=[("G-code files","*.gcode")])
shutil.copy2(source, "tests\\file upload")