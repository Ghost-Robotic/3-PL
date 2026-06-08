import customtkinter as ctk
import tkinter as tk
import sys
sys.path.append("../3_PL")
import src.helpers.loading as ld

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("IntVar Entry Example")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)


        self.canvas = ctk.CTkCanvas(self)
        self.canvas.grid(row=0,column=0,sticky="nsew", padx=50,pady=50)
        
        self.x=0
        y=0
        self.speed = 1
        self.line = self.canvas.create_line(0,50,self.x,50,width=10,fill="red")
        self.increase()
        
    def increase(self):
        print(self.x)
        if self.x<200:
            self.x +=1
            self.canvas.coords(self.line,0,50,self.x,50)
            self.line_increase = self.canvas.after(self.speed, self.increase)


if __name__ == "__main__":
    a = "hello"
    print(a[-4:])
    # app = App()
    # app.mainloop()
