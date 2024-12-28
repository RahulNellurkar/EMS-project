import tkinter as tk
from tkinter import ttk  # themed tool kit
from PIL import Image, ImageTk
import os
import time

class Dashboard(tk.Tk):
    def __init__(self):  
        super().__init__()
        self.title("Employee Project Dashboard")
        self.geometry("600x400")
        self.state('zoomed')

        self.load_image("E:/final project esc/dp.jfif")

        self.create_menus()

        self.time_label = tk.Label(self, text="", font=("Helvetica", 12), bg='yellow')
        self.time_label.pack(pady=10, side="right")
        self.update_time()

    def create_menus(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        menus = [("Insert Record", self.open_department_management, self.open_employee_department, 
                  self.open_leave_details, self.open_payout_salary),
                 ("Search Record", self.open_department_management, self.open_employee_department, 
                  self.open_leave_details, self.open_payout_salary),
                 ("Update Record", self.open_department_management, self.open_employee_department, 
                  self.open_leave_details, self.open_payout_salary),
                 ("Delete Record", self.open_department_management, self.open_employee_department, 
                  self.open_leave_details, self.open_payout_salary)]

        for menu_title, *commands in menus:
            new_menu = tk.Menu(self.menu, tearoff=0)
            self.menu.add_cascade(label=menu_title, menu=new_menu)
            for i, cmd in enumerate(commands):
                new_menu.add_command(label=commands[i].__name__.replace("_", " ").title(), command=cmd)
            new_menu.add_separator()
            new_menu.add_command(label="Close", command=self.destroy)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((800, 500))
        self.dashboard_image = ImageTk.PhotoImage(image)

        self.image_frame = tk.Frame(self)
        self.image_frame.pack(fill='both', expand=True)

        self.image_label = tk.Label(self.image_frame, image=self.dashboard_image)
        self.image_label.pack()
        tk.Label(self.image_frame, text='Employee Management Application', bg='orange', fg='teal', font='sans 18 bold').pack(fill='both')
        tk.Label(self.image_frame, text='Developed by RAHUL, MIT India', bg='green', fg='white', font='sans 16 bold').pack(fill='both')

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

    def open_employee_department(self):
        self.open_file("C:/Users/Skrah/OneDrive/Desktop/python project/employee_department.py")

    def open_department_management(self):
        self.open_file("C:/Users/Skrah/OneDrive/Desktop/python project/department_management.py")

    def open_leave_details(self):
        self.open_file("C:/Users/Skrah/OneDrive/Desktop/python project/leave_details.py")

    def open_payout_salary(self):
        self.open_file("C:/Users/Skrah/OneDrive/Desktop/python project/payout_salary.py")

    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.system(f'\"{file_path}\"')
        else:
            tk.messagebox.showerror("Error", f"File not found: {file_path}")

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
