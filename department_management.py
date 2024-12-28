from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as sql

class Database:
    def __init__(self):
        self.conn = sql.connect(host='localhost', user='root', password='', database='employee dpt')
        self.cursor = self.conn.cursor()

    def insert(self, department_id, department_name, joining_date, attendance, performance_score):
        self.cursor.execute('''
            INSERT INTO department (department_id, department_name, joining_date, attendance, performance_score)
            VALUES (%s, %s, %s, %s, %s)
        ''', (department_id, department_name, joining_date, attendance, performance_score))
        self.conn.commit()

    def fetch_department_ids(self):
        self.cursor.execute('SELECT * FROM department')
        return self.cursor.fetchall()

    def department_id_exists(self, department_id):
        self.cursor.execute('SELECT COUNT(*) FROM department WHERE department_id=%s', (department_id,))
        return self.cursor.fetchone()[0] > 0

database = Database()

def treeview_data():
    department_ids = database.fetch_department_ids()
    tree.delete(*tree.get_children())
    for department_id in department_ids:
        tree.insert('', END, values=department_id)

def add_department_id():
    if (department_idEntry.get() == '' or department_nameEntry.get() == '' or 
        joining_dateEntry.get() == '' or attendanceEntry.get() == '' or 
        performance_scoreEntry.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    elif database.department_id_exists(department_idEntry.get()):
        messagebox.showerror('Error', 'Department ID already exists')
    else:
        database.insert(department_idEntry.get(), department_nameEntry.get(), 
                        joining_dateEntry.get(), attendanceEntry.get(), performance_scoreEntry.get())
        treeview_data()
        messagebox.showinfo('Success', 'Data is added')

def delete_all():
    if messagebox.askyesno('Delete All', 'Are you sure you want to delete all departments?'):
        database.cursor.execute('DELETE FROM department')
        database.conn.commit()
        treeview_data()
        messagebox.showinfo('Success', 'All departments have been deleted')

window = Tk()
window.geometry('1200x950')
window.resizable(False, False)
window.title('DEPARTMENT SYSTEM')
window.configure(bg='#161C30')

logo = Image.open('C:/Users/Skrah/OneDrive/Desktop/final project esc/download (1).jpg')
logo = ImageTk.PhotoImage(logo)
logoLabel = Label(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

leftFrame = Frame(window, bg='#161C30')
leftFrame.grid(row=1, column=0)

department_idLabel = Label(leftFrame, text='Department ID', font=('Arial', 18, 'bold'), bg='white')
department_idLabel.grid(row=0, column=0, padx=20, pady=15, sticky='w')
department_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
department_idEntry.grid(row=0, column=1)

department_nameLabel = Label(leftFrame, text='Department Name', font=('Arial', 18, 'bold'), bg='white')
department_nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
department_nameEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
department_nameEntry.grid(row=1, column=1)

joining_dateLabel = Label(leftFrame, text='Joining Date', font=('Arial', 18, 'bold'), bg='white')
joining_dateLabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')
joining_dateEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
joining_dateEntry.grid(row=2, column=1)

attendanceLabel = Label(leftFrame, text='Attendance', font=('Arial', 18, 'bold'), bg='white')
attendanceLabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
attendanceEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
attendanceEntry.grid(row=3, column=1)

performance_scoreLabel = Label(leftFrame, text='Performance Score', font=('Arial', 18, 'bold'), bg='white')
performance_scoreLabel.grid(row=4, column=0, padx=20, pady=15, sticky='w')
performance_scoreEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
performance_scoreEntry.grid(row=4, column=1)

rightFrame = Frame(window)
rightFrame.grid(row=1, column=1, padx=10, pady=10)

search_options = ['Department ID', 'Department Name', 'Joining Date', 'Attendance', 'Performance Score']
searchbox = ttk.Combobox(rightFrame, values=search_options, state='readonly')
searchbox.grid(row=0, column=0)
searchbox.set('Search by')
searchEntry = Entry(rightFrame)
searchEntry.grid(row=0, column=1)
searchButton = Button(rightFrame, text='Search', width=10)
searchButton.grid(row=0, column=2)
showallButton = Button(rightFrame, text='Show All', width=50)
showallButton.grid(row=0, column=3, pady=5)

tree = ttk.Treeview(rightFrame, height=9)
tree.grid(row=1, column=0, columnspan=4)
tree['columns'] = ['Department ID', 'Department Name', 'Joining Date', 'Attendance', 'Performance Score']
tree.heading('Department ID', text='Department ID')
tree.heading('Department Name', text='Department Name')
tree.heading('Joining Date', text='Joining Date')
tree.heading('Attendance', text='Attendance')
tree.heading('Performance Score', text='Performance Score')

tree.config(show='headings')
tree.column('Department ID', anchor=CENTER, width=100)
tree.column('Department Name', anchor=CENTER, width=100)
tree.column('Joining Date', width=100)
tree.column('Attendance', width=100)
tree.column('Performance Score', width=100)

style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 18, 'bold'))
style.configure('Treeview', font=('Arial', 15, 'bold'))
scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')

buttonFrame = Frame(window, bg='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2)

newButton = Button(buttonFrame, text='New Department', font=('Arial', 15, 'bold'))
newButton.grid(row=0, column=1, pady=5)
AddButton = Button(buttonFrame, text='Add Department', font=('Arial', 16, 'bold'), command=add_department_id)
AddButton.grid(row=0, column=2, pady=5, padx=5)

deleteButton = Button(buttonFrame, text='Delete All', font=('Arial', 16, 'bold'), command=delete_all)
deleteButton.grid(row=0, column=3, pady=5, padx=5)

window.mainloop()
