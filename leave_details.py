from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as sql

class Database:
    def __init__(self):
        self.conn = sql.connect(host='localhost', user='root', password='', database='employee dpt')
        self.cursor = self.conn.cursor()

    def insert(self, leave_id, employee_id, leave_type, leave_start, leave_end, status):
        self.cursor.execute('''
            INSERT INTO leave_details (leave_id, employee_id, leave_type, leave_start, leave_end, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (leave_id, employee_id, leave_type, leave_start, leave_end, status))
        self.conn.commit()

    def fetch_leave_ids(self):
        self.cursor.execute('SELECT * FROM leave_details')
        return self.cursor.fetchall()

    def leave_id_exists(self, leave_id):
        self.cursor.execute('SELECT COUNT(*) FROM leave_details WHERE leave_id=%s', (leave_id,))
        return self.cursor.fetchone()[0] > 0

    def update_leave_status(self, leave_id, status):
        self.cursor.execute('UPDATE leave_details SET status=%s WHERE leave_id=%s', (status, leave_id))
        self.conn.commit()

    def delete_all(self):
        self.cursor.execute("DELETE FROM leave_details")
        self.conn.commit()

    def search_leave(self, column, value):
        query = f"SELECT * FROM leave_details WHERE {column} LIKE %s"
        self.cursor.execute(query, (f"%{value}%",))
        return self.cursor.fetchall()

database = Database()

def treeview_data():
    leave_ids = database.fetch_leave_ids()
    tree.delete(*tree.get_children())
    for leave_id in leave_ids:
        tree.insert('', END, values=leave_id)

def add_leave_id():
    if (leave_idEntry.get() == '' or employee_idEntry.get() == '' or 
        leave_typeEntry.get() == '' or leave_startEntry.get() == '' or 
        leave_endEntry.get() == '' or statusEntry.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    elif database.leave_id_exists(leave_idEntry.get()):
        messagebox.showerror('Error', 'Leave_ID already exists')
    else:
        database.insert(leave_idEntry.get(), employee_idEntry.get(), leave_typeEntry.get(), 
                        leave_startEntry.get(), leave_endEntry.get(), statusEntry.get())
        treeview_data()
        messagebox.showinfo('Success', 'Data is added')

def approve_leave_id():
    selected_item = tree.selection()[0]
    leave_id = tree.item(selected_item, 'values')[0]
    database.update_leave_status(leave_id, 'Approved')
    treeview_data()
    messagebox.showinfo('Success', 'Leave Approved')

def reject_leave_id():
    selected_item = tree.selection()[0]
    leave_id = tree.item(selected_item, 'values')[0]
    database.update_leave_status(leave_id, 'Rejected')
    treeview_data()
    messagebox.showinfo('Success', 'Leave Rejected')

def delete_all():
    if messagebox.askyesno('Delete All', 'Are you sure you want to delete all leaves?'):
        database.delete_all()
        treeview_data()
        messagebox.showinfo('Success', 'All leaves have been deleted')

def search_leave_id():
    column = searchbox.get()
    search_value = searchEntry.get()
    if column and search_value:
        results = database.search_leave(column.lower(), search_value)
        tree.delete(*tree.get_children())
        for leave_id in results:
            tree.insert('', END, values=leave_id)
    else:
        messagebox.showerror('Error', 'Please select a column and enter a search term')

window = Tk()
window.geometry('1200x950')
window.resizable(False, False)
window.title('Leave Management System')
window.configure(bg='#161C30')

logo = Image.open('C:/Users/Skrah/OneDrive/Desktop/final project esc/leave.jpg')
logo = ImageTk.PhotoImage(logo)
logoLabel = Label(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

leftFrame = Frame(window, bg='#161C30')
leftFrame.grid(row=1, column=0)

leave_idLabel = Label(leftFrame, text='LEAVE_ID', font=('Arial', 18, 'bold'), bg='white')
leave_idLabel.grid(row=0, column=0, padx=20, pady=15, sticky='w')
leave_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
leave_idEntry.grid(row=0, column=1)

employee_idLabel = Label(leftFrame, text='EMPLOYEE ID', font=('Arial', 18, 'bold'), bg='white')
employee_idLabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
employee_idEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
employee_idEntry.grid(row=1, column=1)

leave_typeLabel = Label(leftFrame, text='LEAVE_TYPE', font=('Arial', 18, 'bold'), bg='white')
leave_typeLabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')
leave_typeEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
leave_typeEntry.grid(row=2, column=1)

leave_startLabel = Label(leftFrame, text='LEAVE_START', font=('Arial', 18, 'bold'), bg='white')
leave_startLabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
leave_startEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
leave_startEntry.grid(row=3, column=1)

leave_endLabel = Label(leftFrame, text='LEAVE_END', font=('Arial', 18, 'bold'), bg='white')
leave_endLabel.grid(row=4, column=0, padx=20, pady=15, sticky='w')
leave_endEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
leave_endEntry.grid(row=4, column=1)

statusLabel = Label(leftFrame, text='STATUS', font=('Arial', 18, 'bold'), bg='white')
statusLabel.grid(row=5, column=0, padx=20, pady=15, sticky='w')
statusEntry = Entry(leftFrame, font=('Arial', 15, 'bold'), bg='white')
statusEntry.grid(row=5, column=1)

rightFrame = Frame(window)
rightFrame.grid(row=1, column=1, padx=10, pady=10)

search_options = ['Leave_ID', 'Employee_ID', 'Leave_Type', 'Leave_Start', 'Leave_End', 'Status']
searchbox = ttk.Combobox(rightFrame, values=search_options, state='readonly')
searchbox.grid(row=0, column=0)
searchbox.set('Search by')
searchEntry = Entry(rightFrame)
searchEntry.grid(row=0, column=1)
searchButton = Button(rightFrame, text='Search', width=10, command=search_leave_id)
searchButton.grid(row=0, column=2)
showallButton = Button(rightFrame, text='Show All', width=50, command=treeview_data)
showallButton.grid(row=0, column=3, pady=5)

tree = ttk.Treeview(rightFrame, height=9)
tree.grid(row=1, column=0, columnspan=4)
tree['columns'] = ['Leave_ID', 'Employee_ID', 'Leave_Type', 'Leave_Start', 'Leave_End', 'Status']
tree.heading('Leave_ID', text='Leave_ID')
tree.heading('Employee_ID', text='Employee_ID')
tree.heading('Leave_Type', text='Leave_Type')
tree.heading('Leave_Start', text='Leave_Start')
tree.heading('Leave_End', text='Leave_End')
tree.heading('Status', text='Status')
tree.config(show='headings')
tree.column('Leave_ID', anchor=CENTER, width=100)
tree.column('Employee_ID', anchor=CENTER, width=100)
tree.column('Leave_Type', width=100)
tree.column('Leave_Start', width=100)
tree.column('Leave_End', width=100)
tree.column('Status', width=100)

style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 18, 'bold'))
style.configure('Treeview', font=('Arial', 15, 'bold'))
scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')

tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

buttonFrame = Frame(window, bg='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2)

newButton = Button(buttonFrame, text='New Leave_ID', font=('Arial', 15, 'bold'))
newButton.grid(row=0, column=0, pady=5)

AddButton = Button(buttonFrame, text='Add Leave_ID', font=('Arial', 16, 'bold'), command=add_leave_id)
AddButton.grid(row=0, column=1, pady=5, padx=5)

updateButton = Button(buttonFrame, text='Update Leave_ID', font=('Arial', 16, 'bold'))
updateButton.grid(row=0, column=2, pady=5, padx=5)

approveButton = Button(buttonFrame, text='Approve', font=('Arial', 16, 'bold'), command=approve_leave_id)
approveButton.grid(row=0, column=3, pady=5, padx=5)

rejectButton = Button(buttonFrame, text='Reject', font=('Arial', 16, 'bold'), command=reject_leave_id)
rejectButton.grid(row=0, column=4, pady=5, padx=5)

deleteButton = Button(buttonFrame, text='Delete All', font=('Arial', 16, 'bold'), command=delete_all)
deleteButton.grid(row=0, column=5, pady=5, padx=5)

window.mainloop()
