from tkinter import ttk,messagebox
from tkinter import messagebox
import mysql.connector
from tkinter import *
db=mysql.connector.connect(host="localhost",user="root",password="Dinesh@2004",database="STUDENT_DATABASE")
cursor=db.cursor()
def add_students():
    first_name=entry_fname.get()
    last_name=entry_lname.get().strip() or None
    dob=entry_dob.get()
    gender=gender_var.get()
    email=entry_email.get()
    phone=entry_phone.get()
    address=entry_address.get()
    if first_name and dob and email:
        sql="INSERT INTO STUDENT_DETAILS(FIRST_NAME,LAST_NAME,DOB,GENDER,EMAIL,PHONE_NO,ADDRESS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values=(first_name,last_name,dob,gender,email,phone,address)
        cursor.execute(sql,values)
        db.commit()
        messagebox.showinfo("SUCCESS","Student Successfully Added!")
        view_students()
    else:
        messagebox.showerror("ERROR","Please Fill All Fields!")

def view_students():
    for row in student_table.get_children():
        student_table.delete(row)

    cursor.execute("SELECT * FROM STUDENT_DETAILS")
    students=cursor.fetchall()

    for student in students:
        student_table.insert("","end",values=student)

def update_students():
    selected_item=student_table.selection()
    if not selected_item:
        messagebox.showerror("Error","Select the Student to Update")
        return

    student_id=student_table.item(selected_item)['values'][0]
    #new_dob=entry_dob.get().strip()
    new_address=entry_address.get().strip()
    new_phone=entry_phone.get().strip()
    new_email = entry_email.get().strip()

    sql="UPDATE STUDENT_DETAILS SET Email=%s,PHONE_NO=%s,Address=%s WHERE STUDENT_ID = %s"
    values=(new_address,new_phone,new_email,student_id)
    cursor.execute(sql,values)
    db.commit()
    messagebox.showinfo("Success","Student details Updates!")
    view_students()

def delete_students():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error","Select Student to Delete")
        return

    student_id = student_table.item(selected_item)['values'][0]
    sql="DELETE FROM STUDENT_DETAILS WHERE STUDENT_ID = %s"
    cursor.execute(sql,(student_id,))
    db.commit()
    messagebox.showinfo("Success","Student Deleted Successfully!")
    view_students()

root=Tk()
root.geometry("2000x600")
root.title("Student Management System")
frame=Frame(root)
frame.pack(pady=10)
Label(frame,text="First Name :    ").grid(row=0,column=0)
entry_fname=Entry(frame)
entry_fname.grid(row=0,column=3)
Label(frame,text="Last Name :     ").grid(row=1,column=0)
entry_lname=Entry(frame)
entry_lname.grid(row=1,column=3)
Label(frame,text="DOB (YYYY-MM-DD) :     ").grid(row=2,column=0)
entry_dob=Entry(frame)
entry_dob.grid(row=2,column=3)
Label(frame,text="Gender :     ").grid(row=3,column=0)
gender_var =StringVar(value="Male")
gender_dropdown=ttk.Combobox(frame,textvariable=gender_var,values=["Male","Female","Others"])
gender_dropdown.grid(row=3,column=3)
Label(frame,text="Email :     ").grid(row=4,column=0)
entry_email=Entry(frame)
entry_email.grid(row=4,column=3)
Label(frame,text="Phone No :     ").grid(row=5,column=0)
entry_phone=Entry(frame)
entry_phone.grid(row=5,column=3)
Label(frame,text="Address :     ").grid(row=6,column=0)
entry_address=Entry(frame)
entry_address.grid(row=6,column=3)
button_frame=Frame(root)
button_frame.pack(pady=10)
Button(button_frame,text="Add Student",bg="lightgreen",fg="black",activebackground="white",activeforeground="green",command=add_students).grid(row=0,column=0)
Button(button_frame,text="View Student",bg="lightblue",fg="black",activebackground="white",activeforeground="blue",command=view_students).grid(row=0,column=1)
Button(button_frame,text="Update Student",bg="yellow",fg="black",activebackground="white",activeforeground="orange",command=update_students).grid(row=0,column=2)
Button(button_frame,text="Delete Student",bg="red",fg="black",activebackground="white",activeforeground="red",command=delete_students).grid(row=0,column=3)
table_frame=Frame(root)
table_frame.pack(pady=40)
columns=("ID","First Name","Last Name","DOB","Gender","Email","Phone No","Address")
student_table=ttk.Treeview(table_frame,columns=columns,show="headings",height=10)
for col in columns:
    student_table.heading(col,text=col)
    student_table.column(col,width=150)

student_table.pack()
view_students()
root.mainloop()
