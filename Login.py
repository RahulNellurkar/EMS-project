from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

# Connect to MySQL database
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif usernameEntry.get() == 'rahul' and passwordEntry.get() == '1234':
        messagebox.showinfo('Success', 'Login is successful')
        root.destroy()
        import dashboard  # Ensure 'dashboard.py' exists in the same directory
        dashboard.Dashboard()  # Launch the dashboard
    else:
        messagebox.showerror('Error', 'Wrong credentials')

root = Tk()
root.geometry('930x478')
root.resizable(0, 0)
root.title('Login Page')

image = Image.open('C:/Users/Skrah/OneDrive/Desktop/final project esc/emplimage.jfif')
image = ImageTk.PhotoImage(image)
imageLabel = Label(root, image=image)
imageLabel.place(x=350, y=150)

headingLabel = Label(root, text='Employee Management System', bg='#FAFAFA', font=('Goudy old style', 20, 'bold'), fg='dark blue')
headingLabel.place(x=20, y=100)

usernameEntry = Entry(root, width=25)
usernameEntry.insert(0, 'Enter Your Username')
usernameEntry.place(x=50, y=150)

passwordEntry = Entry(root, width=25, show='*')
passwordEntry.insert(0, 'Enter Your Password')
passwordEntry.place(x=50, y=200)

loginButton = Button(root, text='Login', cursor='hand2', command=login)
loginButton.place(x=70, y=250)

root.mainloop()
