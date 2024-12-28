from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as sql

class Database:
    def __init__(self):
        self.conn = sql.connect(host='localhost', user='root', password='', database='employee dpt')
        self.cursor = self.conn.cursor()

    def insert(self, payout_id, employee_id,salary,payout_date):
        self.cursor.execute('''
            INSERT INTO  payout_salary_details (payout_id,employee_id,salary,payout_date)
            VALUES (%s, %s, %s, %s)
        ''', (payout_id,employee_id,salary,payout_date  ))
        self.conn.commit()

    def fetch_payout_id(self):
        self.cursor.execute('SELECT * FROM  payout_salary_details')
        return self.cursor.fetchall()

    def payout_id_exists(self, payout_id):
        self.cursor.execute('SELECT COUNT(*) FROM  payout_salary_details WHERE payout_id=%s', (payout_id,))
        return self.cursor.fetchone()[0] > 0

database = Database()

def treeview_data():
    payout_id = database.fetch_payout_id()
    tree.delete(*tree.get_children())
    for payout_id in payout_id:
        tree.insert('', END, values=payout_id)

def add_payout_id():
    if (payout_idEntry.get() == '' or employee_idEntry.get() == '' or salaryEntry.get() == '' or 
        payout_dateEntry.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    elif database.payout_id_exists(payout_idEntry.get()):
        messagebox.showerror('Error', 'ID already exists')
    else:
        database.insert(payout_idEntry.get(), employee_idEntry.get(),salaryEntry.get(), 
                        payout_dateEntry.get())
        treeview_data()
        messagebox.showinfo('Success', 'Data is added')

def search_employee():
    search_by = searchBox.get()
    search_value = searchEntry.get()
    if search_by and search_value:
        query = f"SELECT * FROM  payout_salary_details WHERE {search_by.lower().replace(' ', '_')} LIKE %s"
        database.cursor.execute(query, ('%' + search_value + '%',))
        employees = database.cursor.fetchall()
        tree.delete(*tree.get_children())
        for payout_id in payout_ids:
            tree.insert('', END, values=payout_id)
    else:
        messagebox.showerror('Error', 'Please select a search category and enter a value')

def delete_all():
    if messagebox.askyesno('Delete All', 'Are you sure you want to delete all  payout_salary_details?'):
        database.cursor.execute('DELETE FROM  payout_salary_details')
        database.conn.commit()
        treeview_data()
        messagebox.showinfo('Success', 'All payout have been deleted')

window = Tk()
window.geometry('1200x950')
window.resizable(False, False)
window.title('Salary Management System')
window.configure(bg='#161C30')

logo = Image.open('C:/Users/Skrah/OneDrive/Desktop/final project esc/salary.jpg')
logo = ImageTk.PhotoImage(logo)
logoLabel = Label(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

leftFrame = Frame(window, bg='#161C30')
leftFrame.grid(row=1, column=0)

payout_idLabel = Label(leftFrame, text='payout_id', font=('Arial', 18, 'bold'), bg='white')
payout_idLabel.grid(row=0, column=0, padx=20, pady=15, sticky='w')
payout_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
payout_idEntry.grid(row=0, column=1)

employee_idLabel = Label(leftFrame, text='employee_id', font=('Arial', 18, 'bold'), bg='white')
employee_idLabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
employee_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
employee_idEntry.grid(row=1, column=1)

salaryLabel = Label(leftFrame, text='salary', font=('Arial', 18, 'bold'), bg='white')
salaryLabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')
salaryEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
salaryEntry.grid(row=2, column=1)

payout_dateLabel = Label(leftFrame, text='payout_date', font=('Arial', 18, 'bold'), bg='white')
payout_dateLabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
payout_dateEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), width=18)
payout_dateEntry.grid(row=3, column=1)

rightFrame = Frame(window)
rightFrame.grid(row=1, column=1, padx=10, pady=10)

search_options = ['payout_id', 'employee_id', 'salary', 'payout_date']
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
tree['columns'] = ('payout_id', 'employee_id', 'salary', 'payout_date')
tree.heading('payout_id', text='payout_id')
tree.heading('employee_id', text='employee_id')
tree.heading('salary', text='salary')
tree.heading('payout_date', text='payout_date')
tree.config(show='headings')
tree.column('payout_id', anchor=CENTER, width=100)
tree.column('employee_id', width=100)
tree.column('salary', width=100)
tree.column('payout_date', width=100)


style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 18, 'bold'))
style.configure('Treeview', font=('Arial', 15, 'bold'))
scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')

tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

buttonFrame = Frame(window, bg='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2)

AddButton = Button(buttonFrame, text='Add payout_id', font=('Arial', 16, 'bold'), command=add_payout_id)
AddButton.grid(row=0, column=0, pady=5, padx=5)

deleteButton = Button(buttonFrame, text='Delete All', font=('Arial', 16, 'bold'), command=delete_all)
deleteButton.grid(row=0, column=1, pady=5, padx=5)

window.mainloop()
 
