import customtkinter as ctk
import sys
sys.path.append("../3_PL")
import src.style as style
import math
from PIL import Image, ImageTk

class Loading(ctk.CTkFrame):
    """loading animations frame"""
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent, fg_color=style.dark_background)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)


    def grid_triple(self):
        """animation with three stacked lines"""
        self.container = ctk.CTkCanvas(self, width=800, height=800, bg=style.dark_background, borderwidth=0,highlightthickness=0)
        self.container.grid(row=0,column=0)        
        
        self.canvas = ctk.CTkCanvas(self.container, bg=style.dark_background, width=400,height=400, borderwidth=0,highlightthickness=0)
        self.container.create_window(400,800, window=self.canvas,anchor="s")  
        
        self.speed = 10
        self.distance = 400
        
        self.line_1_x = 0
        self.line_2_x = self.distance
        self.line_3_x = 0
        
        self.line1 = self.canvas.create_line(0,50,self.line_1_x,50,width=100,fill=style.main_blue)
        self.line2 = self.canvas.create_line(400,200,self.line_2_x,200,width=100,fill=style.main_blue)
        self.line3= self.canvas.create_line(0,350,self.line_3_x,350,width=100,fill=style.main_blue)
        
        self.img_canvas = ctk.CTkCanvas(self.container, bg=style.dark_background, width=400,height=400, borderwidth=0,highlightthickness=0)
        self.image_cont =self.container.create_window(200,700, window=self.img_canvas,anchor="s") 
        
        self.img = ImageTk.PhotoImage((Image.open(r"assets\toolhead-transp.png")).resize((400,400), Image.LANCZOS))
        self.img_canvas.create_image(200,400, image=self.img, anchor="s")
        self.canvas.itemconfig(self.line3, capstyle="round")
        self.increase_triple()
        
    def increase_triple(self):
        """begin animation"""
        if self.line_3_x < 399.99:      
            percentage = (self.line_3_x)/self.distance
            #print(f"{step} , {percentage} , {self.line_3_x}")
            change = self.speed  + ((5/2)*(math.sin((2*math.pi*percentage) - (math.pi/2)) + 1))
            self.line_3_x += change
            # print((5/2) * (math.sin((2*math.pi*percentage) - (math.pi/2)) + 1))
            self.container.move(self.image_cont,change,0)
            self.canvas.coords(self.line3,0,350,self.line_3_x,350)
            self.canvas.after(15,self.increase_triple)
            return
        self.container.coords(self.image_cont,600,550)
        if (self.line_3_x>399.99) and self.line_2_x > 0.01:
            self.canvas.itemconfig(self.line2,capstyle="round") 
            percentage = (self.line_2_x)/self.distance
            #print(f"{percentage} , {self.line_2_x}")
            change = -self.speed  - ((5/2)*(math.sin((2*math.pi*percentage) - (math.pi/2)) + 1))
            self.line_2_x += change
            self.container.coords(self.image_cont,200+self.line_2_x,550)
            self.canvas.coords(self.line2,400,200,self.line_2_x,200)
            self.canvas.after(15,self.increase_triple)
            return
        self.container.coords(self.image_cont,200,400)
        if self.line_2_x < 0.01 and self.line_1_x < 399.99:
            self.canvas.itemconfig(self.line1,capstyle="round") 
            percentage = (self.line_1_x)/self.distance
            #print(f"{percentage} , {self.line_1_x}")
            change = self.speed  + ((5/2)*(math.sin((2*math.pi*percentage) - (math.pi/2)) + 1))
            self.line_1_x += change
            self.container.coords(self.image_cont,200+self.line_1_x,400)
            self.canvas.coords(self.line1,0,50,self.line_1_x,50)
            self.canvas.after(15,self.increase_triple)
            return
        self.container.coords(self.image_cont,600,400)
        self.after(10,self.destroy)
        
        
    def grid_single(self):
        """loading animation with single line"""
        self.length = 800
        self.height = 70
        size = 200
        self.speed = 60
        
        self.configure(fg_color=style.dark_foreground)
        self.container = ctk.CTkCanvas(self, width=self.length+size, height=size+self.height, bg=style.dark_foreground, borderwidth=0,highlightthickness=0)
        self.container.grid(row=0,column=0)        
        
        self.canvas = ctk.CTkCanvas(self.container, bg=style.dark_background, width=self.length,height=self.height, borderwidth=0,highlightthickness=0)
        self.container.create_window((self.length+size)/2,size+self.height, window=self.canvas,anchor="s")  
        
        self.linex = 0
        self.line = self.canvas.create_line(0,self.height/2,self.linex,self.height/2,width=self.height,fill=style.main_blue, capstyle="round")
        
        self.img_canvas = ctk.CTkCanvas(self.container, bg=style.dark_foreground, width=size,height=size, borderwidth=0,highlightthickness=0)
        self.image_cont =self.container.create_window(size/2,size, window=self.img_canvas,anchor="s") 
        
        self.img = ImageTk.PhotoImage((Image.open(r"assets\toolhead-transp.png")).resize((size,size), Image.LANCZOS))
        self.img_canvas.create_image(size/2,size, image=self.img, anchor="s")
        
        self.increase_single()
        
    def increase_single(self):
        """begin animation"""
        if self.linex < (self.length-0.01):      
            percentage = (self.linex)/self.length
            change = self.speed  + ((5/2)*(math.sin((2*math.pi*percentage) - (math.pi/2)) + 1))
            self.linex += change
            self.container.move(self.image_cont,change,0)
            self.canvas.coords(self.line,0,self.height/2,self.linex,self.height/2)
            self.canvas.after(16,self.increase_single)
            return

        self.after(10,self.destroy)

        
if __name__ == "__main__":
    class Test(ctk.CTk):
        def __init__(self, *args, **kwargs):
            ctk.CTk.__init__(self, *args, **kwargs)
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            
            frame = Loading(self,self)
            frame.grid(row=0, column=0, sticky="nsew")       
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            #frame.grid_triple()
            #frame.grid_single()
            self.after(1, lambda : self.state('zoomed'))
            
    app = Test()
    app.mainloop()