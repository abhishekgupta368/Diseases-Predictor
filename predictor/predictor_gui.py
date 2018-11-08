import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from clean_data import get_clean_data
from predictor import detect_dis
LARGE_FONT= ("Verdana", 12)


class Project(tk.Tk):

    def __init__(self):
        
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Diseases Prediction System")
        tk.Tk.geometry(self,"500x700")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #-----------------------------------------------------------
        #-----------------------------------------------------------
        self.frames = {}

        for F in (StartPage, Check_des, Clean_data):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = ttk.Label(self, text="Welcome \n  To Our \n  Sytem", font=("Verdana", 32))
        label.place(x=150,y=10)

        button = ttk.Button(self, text="Check Disease",command=lambda: controller.show_frame(Check_des))
        button.place(x=100,y=200)

        button2 = ttk.Button(self, text="Clean Data", command=lambda: controller.show_frame(Clean_data))
        button2.place(x=300,y=200)


class Check_des(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.comment = tk.StringVar()
        def get_problem():
            input_Value = text_area.get("1.0","end-1c")
            res = detect_dis(str(input_Value))
            ans_label.configure(text=res)
            
        self.problem = tk.StringVar()
        label = ttk.Label(self, text="Enter your Problem:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        text_area = tk.Text(self, height=5, width=40)
        text_area.place(x=100,y=50)
        
        button2 = ttk.Button(self, text="Submit",command=get_problem)
        button2.place(x=220,y=150)
        
        button2 = ttk.Button(self, text="Go back",
                            command=lambda: controller.show_frame(StartPage))
        button2.place(x=220,y=200)
        
        ans_label=tk.Label(self,text='',font=('arail',9,'bold'))
        ans_label.place(x=160,y=250)



class Clean_data(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.url = tk.StringVar()
        def print_clean():
            get_clean_data(str(self.url.get()))
            a="data is cleaned!!!!"
            ans_label.configure(text=a)
        #--------------------------------------------------------------
        label = ttk.Label(self, text="Clean data", font=("Verdana", 20))
        label.place(x=150,y=20)
        
        url_label = ttk.Label(self,text="Url: ",font=("Verdana", 10))
        url_label.place(x=140,y=80)
        url_label_entry = ttk.Entry(self,width=30,textvariable=self.url)
        url_label_entry.place(x=170,y=80)
        
        button1 = ttk.Button(self, text="Clean Data",command=print_clean)
        button1.place(x=160,y=120)
        
        button2 = ttk.Button(self, text="Home Page",command=lambda: controller.show_frame(StartPage))
        button2.place(x=160,y=160)
        
        ans_label=tk.Label(self,text='',font=('arail',15,'bold'))
        ans_label.place(x=160,y=200)


app = Project()
app.mainloop()