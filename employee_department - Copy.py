from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as sql

class Database:
    def __init__(self):
        self.conn = sql.connect(host='localhost', user='root', password='', database='employee dpt')
        self.cursor = self.conn.cursor()

    def insert(self, employee_id, employee_name, last_name, phone, mail):
        self.cursor.execute('''
            INSERT INTO employee_dpt (employee_id, employee_name, last_name, phone, mail)
            VALUES (%s, %s, %s, %s, %s)
        ''', (employee_id, employee_name, last_name, phone, mail))
        self.conn.commit()

    def fetch_employees_id(self):
        self.cursor.execute('SELECT * FROM employee_dpt')
        return self.cursor.fetchall()

    def employee_id_exists(self, employee_id):
        self.cursor.execute('SELECT COUNT(*) FROM employee_dpt WHERE employee_id=%s', (employee_id,))
        return self.cursor.fetchone()[0] > 0

database = Database()

def treeview_data():
    employees_id = database.fetch_employees_id()
    tree.delete(*tree.get_children())
    for employee_id in employees_id:
        tree.insert('', END, values=employee_id)

def add_employee_id():
    if (employee_idEntry.get() == '' or nameEntry.get() == '' or last_nameEntry.get() == '' or 
        phoneEntry.get() == '' or mailEntry.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    elif database.employee_id_exists(employee_idEntry.get()):
        messagebox.showerror('Error', 'ID already exists')
    else:
        database.insert(employee_idEntry.get(), nameEntry.get(), last_nameEntry.get(), 
                        phoneEntry.get(), mailEntry.get())
        treeview_data()
        messagebox.showinfo('Success', 'Data is added')

def search_employee():
    search_by = searchBox.get()
    search_value = searchEntry.get()
    if search_by and search_value:
        query = f"SELECT * FROM employee_dpt WHERE {search_by.lower().replace(' ', '_')} LIKE %s"
        database.cursor.execute(query, ('%' + search_value + '%',))
        employees = database.cursor.fetchall()
        tree.delete(*tree.get_children())
        for employee in employees:
            tree.insert('', END, values=employee)
    else:
        messagebox.showerror('Error', 'Please select a search category and enter a value')

def delete_all():
    if messagebox.askyesno('Delete All', 'Are you sure you want to delete all employees?'):
        database.cursor.execute('DELETE FROM employee_dpt')
        database.conn.commit()
        treeview_data()
        messagebox.showinfo('Success', 'All employees have been deleted')

window = Tk()
window.geometry('1200x950')
window.resizable(False, False)
window.title('Employee Management System')
window.configure(bg='#161C30')

logo = Image.open('C:/Users/Skrah/OneDrive/Desktop/final project esc/download.jpg')
logo = ImageTk.PhotoImage(logo)
logoLabel = Label(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

leftFrame = Frame(window, bg='#161C30')
leftFrame.grid(row=1, column=0)

employee_idLabel = Label(leftFrame, text='Employee_ID', font=('Arial', 18, 'bold'), bg='white')
employee_idLabel.grid(row=0, column=0, padx=20, pady=15, sticky='w')
employee_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
employee_idEntry.grid(row=0, column=1)

nameLabel = Label(leftFrame, text='Employee_Name', font=('Arial', 18, 'bold'), bg='white')
nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
nameEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
nameEntry.grid(row=1, column=1)

last_nameLabel = Label(leftFrame, text='Last_Name', font=('Arial', 18, 'bold'), bg='white')
last_nameLabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')
last_nameEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
last_nameEntry.grid(row=2, column=1)

phoneLabel = Label(leftFrame, text='Phone', font=('Arial', 18, 'bold'), bg='white')
phoneLabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
phoneEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
phoneEntry.grid(row=3, column=1)

mailLabel = Label(leftFrame, text='Mail', font=('Arial', 18, 'bold'), bg='white')
mailLabel.grid(row=4, column=0, padx=20, pady=15, sticky='w')
mailEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
mailEntry.grid(row=4, column=1)

addressLabel = Label(leftFrame, text='Address', font=('Arial', 18, 'bold'), bg='white')
addressLabel.grid(row=5, column=0, padx=20, pady=15, sticky='w')
addressEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
addressEntry.grid(row=5, column=1)

rightFrame = Frame(window)
rightFrame.grid(row=1, column=1, padx=10, pady=10)

search_options = ['Employee_ID', 'Employee_Name', 'Last_Name', 'Phone', 'Mail', 'Address']
searchBox = ttk.Combobox(rightFrame, values=search_options, state='readonly')
searchBox.grid(row=0, column=0)
searchBox.set('Search by')
searchEntry = Entry(rightFrame)
searchEntry.grid(row=0, column=1)
searchButton = Button(rightFrame, text='Search', width=10, command=search_employee)
searchButton.grid(row=0, column=2)
showallButton = Button(rightFrame, text='Show All', width=50, command=treeview_data)
showallButton.grid(row=0, column=3, pady=5)

tree = ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=4)
tree['columns'] = ('Employee_ID', 'Employee_Name', 'Last_Name', 'Phone', 'Mail', 'Address')
tree.heading('Employee_ID', text='Employee_ID')
tree.heading('Employee_Name', text='Employee_Name')
tree.heading('Last_Name', text='Last_Name')
tree.heading('Phone', text='Phone')
tree.heading('Mail', text='Mail')
tree.heading('Address', text='Address')
tree.config(show='headings')
tree.column('Employee_ID', anchor=CENTER, width=100)
tree.column('Employee_Name', width=100)
tree.column('Last_Name', width=100)
tree.column('Phone', width=100)
tree.column('Mail', width=100)
tree.column('Address', width=100)

style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 18, 'bold'))
style.configure('Treeview', font=('Arial', 15, 'bold'))
scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')

tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

buttonFrame = Frame(window, bg='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2)

newButton = Button(buttonFrame, text='New Employee_id', font=('Arial', 16, 'bold'))
newButton.grid(row=0, column=0, pady=5)

AddButton = Button(buttonFrame, text='Add Employee_id', font=('Arial', 16, 'bold'), command=add_employee_id)
AddButton.grid(row=0, column=1, pady=5, padx=5)

updateButton = Button(buttonFrame, text='Update Employee_id', font=('Arial', 16, 'bold'))
updateButton.grid(row=0, column=2, pady=5, padx=5)

deleteButton = Button(buttonFrame, text='Delete All', font=('Arial', 16, 'bold'), command=delete_all)
deleteButton.grid(row=0, column=3, pady=5, padx=5)

window.mainloop()
