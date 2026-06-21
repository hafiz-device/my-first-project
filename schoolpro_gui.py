# SchoolPro Ghana - GUI Version
# Developer: Issahak Abdul Halim (Hafiz)
# Version: 2.0

import tkinter as tk
from tkinter import messagebox
import sqlite3 
from datetime import date 

# Connect to database 
conn = sqlite3.connect("/home/hafiz/my-first-project/schoolpro.db")
cursor = conn.cursor()

def open_registration():
    reg_window = tk.Toplevel(window)
    reg_window.title("Student Registration")
    reg_window.geometry("500x400")
    reg_window.configure(bg="darkblue")

    tk.Label(reg_window, text="STUDENT REGISTRATION", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(reg_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(reg_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(reg_window, text="Age:", bg="darkblue", fg="white").pack()
    age_entry = tk.Entry(reg_window, width=30)
    age_entry.pack(pady=5)

    tk.Label(reg_window, text="Gender:", bg="darkblue", fg="white").pack()
    gender_entry = tk.Entry(reg_window, width=30)
    gender_entry.pack(pady=5)

    tk.Label(reg_window, text="Class:", bg="darkblue", fg="white").pack()
    class_entry = tk.Entry(reg_window, width=30)
    class_entry.pack(pady=5)

    tk.Label(reg_window, text="Section (Academic/Islamic):", bg="darkblue", fg="white").pack()
    section_entry = tk.Entry(reg_window, width=30)
    section_entry.pack(pady=5)

    tk.Label(reg_window, text="Parent Name:", bg="darkblue", fg="white").pack()
    parent_entry = tk.Entry(reg_window, width=30)
    parent_entry.pack(pady=5)

    tk.Label(reg_window, text="Parent Phone:", bg="darkblue", fg="white").pack()
    phone_entry = tk.Entry(reg_window, width=30)
    phone_entry.pack(pady=5)

    def save_student():
        name = name_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        class_name = class_entry.get()
        section = section_entry.get()
        parent_name = parent_entry.get()
        parent_phone = phone_entry.get()
        today = str(date.today())

        cursor.execute(
            "INSERT INTO students (name, age, gender, class_name, section, parent_name, parent_phone, date_registered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, gender, class_name, section, parent_name, parent_phone, today)
        ) 
        conn.commit()
        messagebox.showinfo("Success", "Student Registered Successfully!")
        reg_window.destroy()
    tk.Button(reg_window, text="Save Student", bg="green", fg="white", font=("Arial", 12), command=save_student).pack(pady=10)

def open_attendance():
    att_window = tk.Toplevel(window)
    att_window.title("Attendance")
    att_window.geometry("400x300")
    att_window.configure(bg="darkblue")

    tk.Label(att_window, text="ATTENDANCE", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(att_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(att_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(att_window, text="Status (Present/Absent):", bg="darkblue", fg="white").pack()
    status_entry = tk.Entry(att_window, width=30)
    status_entry.pack(pady=5)

    def save_attendance():
        student_name = name_entry.get()
        status = status_entry.get()
        today = str(date.today())
        cursor.execute(
            "INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)",
            (student_name, today, status)
        ) 
        conn.commit()
        messagebox.showinfo("Success", "Attendance Recorded Successfully!")
        att_window.destroy()

    tk.Button(att_window, text="Save Attendance", bg="green", fg="white", font=("Arial", 12), command=save_attendance).pack(pady=10)
def open_grades():
    grades_window = tk.Toplevel(window)
    grades_window.title("Grades & Results")
    grades_window.geometry("400x400")
    grades_window.configure(bg="darkblue")

    tk.Label(grades_window, text="GRADES & RESULTS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(grades_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(grades_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(grades_window, text="Subject:", bg="darkblue", fg="white").pack()
    subject_entry = tk.Entry(grades_window, width=30)
    subject_entry.pack(pady=5)

    tk.Label(grades_window, text="Score:", bg="darkblue", fg="white").pack()
    score_entry = tk.Entry(grades_window, width=30)
    score_entry.pack(pady=5)

    tk.Label(grades_window, text="Grade (A/B/C/D/F):", bg="darkblue", fg="white").pack()
    grade_entry =tk.Entry(grades_window, width=30)
    grade_entry.pack(pady=5)

    tk.Label(grades_window, text="Term (1/2/3):", bg="darkblue", fg="white").pack()
    term_entry = tk.Entry(grades_window, width=30)
    term_entry.pack(pady=5)

    tk.Label(grades_window, text="Year:", bg="darkblue", fg="white").pack()
    year_entry = tk.Entry(grades_window, width=30)
    year_entry.pack(pady=5)

    def save_grades():
        student_name =  name_entry.get()
        subject = subject_entry.get()
        score = score_entry.get()
        grade = grade_entry.get()
        term = term_entry.get()
        year = year_entry.get()
        cursor.execute(
            "INSERT INTO grades(student_name, subject, score, grade, term, year) VALUES (?, ?, ?, ?, ?, ?)",
            (student_name, subject, score, grade, term, year)
        ) 
        conn.commit()
        messagebox.showinfo("Success", "Grades Recorded Successfully!")
        grades_window.destroy()

    tk.Button(grades_window, text="Save Grades", bg="green", fg="white", font=("Arial, 12"), command=save_grades).pack(pady=10)    

def open_fees():
    fee_window = tk.Toplevel(window)
    fee_window.title("Fee Management")
    fee_window.geometry("400x350")
    fee_window.configure(bg="darkblue")

    tk.Label(fee_window, text="FEE MANAGEMET", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(fee_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(fee_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(fee_window, text="Amount Paid (GHS):", bg="darkblue", fg="white").pack()
    amount_entry = tk.Entry(fee_window, width=30)
    amount_entry.pack(pady=5)

    tk.Label(fee_window, text="Term (1/2/3):", bg="darkblue", fg="white").pack()
    term_entry = tk.Entry(fee_window, width=30)
    term_entry.pack(pady=5) 

    tk.Label(fee_window, text="Status (Paid/partial/unpaid):", bg="darkblue", fg="white").pack()
    status_entry = tk.Entry(fee_window, width=30)
    status_entry.pack(pady=5)

    def save_fees():
        student_name = name_entry.get() 
        amount = amount_entry.get()
        term = term_entry.get()
        status = status_entry.get()
        today = str(date.today())
        cursor.execute(
            "INSERT INTO fees (student_name, amount, date, term, status) VALUES (?, ?, ?, ?, ?)",
            (student_name, amount, today, term, status)
        )
        conn.commit()
        messagebox.showinfo("Success", "Fee Recorded Successfully!")
        fee_window.destroy()

    tk.Button(fee_window, text="Save Fee", bg="green", fg="white", font=("Arial, 12"), command=save_fees).pack(pady=10)  

def open_teachers():
    teacher_window = tk.Toplevel(window)
    teacher_window.title("Teacher Management")
    teacher_window.geometry("400x350")
    teacher_window.configure(bg="darkblue")

    tk.Label(teacher_window, text="TEACHER MANAGEMENT", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(teacher_window, text="Teacher Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(teacher_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(teacher_window, text="Subject:", bg="darkblue", fg="white").pack()
    subject_entry = tk.Entry(teacher_window, width=30)
    subject_entry.pack(pady=5)

    tk.Label(teacher_window, text="Class:", bg="darkblue", fg="white").pack()
    class_entry = tk.Entry(teacher_window, width=30)
    class_entry.pack(pady=5)

    tk.Label(teacher_window, text="Phone:", bg="darkblue", fg="white").pack()
    phone_entry = tk.Entry(teacher_window, width=30)
    phone_entry.pack(pady=5)

    tk.Label(teacher_window, text="Section (Academic/Islamic):", bg="darkblue", fg="white").pack()      
    section_entry = tk.Entry(teacher_window, width=30)
    section_entry.pack(pady=5)

    def save_teacher():
        name = name_entry.get()
        subject = subject_entry.get()
        class_name = class_entry.get()
        phone = phone_entry.get()
        section = section_entry.get()
        cursor.execute(
            "INSERT INTO teachers (name, subject, class_name, phone, section) VALUES (?, ?, ?, ?, ?)",
            (name, subject, class_name, phone, section)
        )
        conn.commit()
        messagebox.showinfo("Success", "Teacher Registered Successfully!")
        teacher_window.destroy()

    tk.Button(teacher_window, text="Save Teacher", bg="green", fg="white", font=("Arial", 12), command=save_teacher).pack(pady=10)

def open_view_students():
    view_window = tk.Toplevel(window)
    view_window.title("All Students")
    view_window.geometry("600x400")
    view_window.configure(bg="darkblue")

    tk.Label(view_window, text="ALL STUDENTS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    # Text box to display students
    text_box = tk.Text(view_window, width=70, height=20)
    text_box.pack(pady=10)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if len(students) == 0:
        text_box.insert(tk.END, "No students registered yet!")
    else: 
        for student in students:
            text_box.insert(tk.END, "ID: " + str(student[0]) + "\n")
            text_box.insert(tk.END, "Name: " + student[1] + "\n")
            text_box.insert(tk.END, "Age: " + student[2] + "\n")
            text_box.insert(tk.END, "Gender: " + student[3] + "\n")
            text_box.insert(tk.END, "Class: " + student[4] + "\n")
            text_box.insert(tk.END, "Section: " + student[5] + "\n")
            text_box.insert(tk.END, "Parent: " + student[6] + "\n")
            text_box.insert(tk.END, "Phone: " + student[7] + "\n")
            text_box.insert(tk.END, "Status: " + str(student[9]) + "\n")
            text_box.insert(tk.END, "------------------------\n")

def open_search():
    search_window = tk.Toplevel(window)
    search_window.title("Search Student")
    search_window.geometry("600x400")
    search_window.configure(bg="darkblue")

    tk.Label(search_window, text="SEARCH STUDENT", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(search_window, text="Entry Student Name:", bg="darkblue", fg="white").pack()
    search_entry = tk.Entry(search_window, width=30)
    search_entry.pack(pady=5)

    text_box = tk.Text(search_window, width=70, height=15)
    text_box.pack(pady=10)

    def search_student():
        text_box.delete(1.0,tk.END)
        search_name = search_entry.get()
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_name + '%',))
        results = cursor.fetchall()
        if len(results) == 0:
            text_box.insert(tk.END, "No student found!")
        else:
            for student in results:
                text_box.insert(tk.END, "ID: " + str(student[0]) + "\n")
                text_box.insert(tk.END, "Name: " + student[1] + "\n")
                text_box.insert(tk.END, "Age: " + student[2] + "\n")
                text_box.insert(tk.END, "Gender: " + student[3] + "\n")
                text_box.insert(tk.END, "Class: " + student[4] + "\n")
                text_box.insert(tk.END, "Section: " + student[5] + "\n")
                text_box.insert(tk.END, "Perent: " + student[6] + "\n")
                text_box.insert(tk.END, "Phone: " + student[7] + "\n")
                text_box.insert(tk.END, "Status: " + str(student[9]) + "\n")
                text_box.insert(tk.END, "------------------------\n")

    tk.Button(search_window, text="Search", bg="green", fg="white", font=("Arial", 12), command=search_student).pack(pady=5)

def open_view_attendance():
    att_view_window = tk.Toplevel(window)
    att_view_window.title("View Attendance")
    att_view_window.geometry("600x400")
    att_view_window.configure(bg="darkblue")

    tk.Label(att_view_window, text="VIEW ATTENDANCE", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    text_box = tk.Text(att_view_window, width=70, height=20)
    text_box.pack(pady=10)                    

    cursor.execute("SELECT *FROM attendance")
    records = cursor.fetchall()

    if len(records) == 0:
        text_box.insert(tk.END, "No attendance yet!")
    else:
        for record in records:
            text_box.insert(tk.END, "ID: " + str(record[0]) + "\n")
            text_box.insert(tk.END, "Student: " + record[1] + "\n")
            text_box.insert(tk.END, "Date: " + record[2] + "\n")
            text_box.insert(tk.END, "Status: " + record[3] + "\n")
            text_box.insert(tk.END, "--------------------------")

def open_view_fees():
    fee_view_window = tk.Toplevel(window)
    fee_view_window.title("View Fees")
    fee_view_window.geometry("600x400")
    fee_view_window.configure(bg="darkblue")

    tk.Label(fee_view_window, text="VIEW FEES", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    text_box = tk.Text(fee_view_window, width=70, height=20)
    text_box.pack(pady=10)

    cursor.execute("SELECT * FROM fees")
    records = cursor.fetchall()
    if len(records) == 0:
        text_box.insert(tk.END, "No fee recorded yet!")
    else:
        for record in records:
            text_box.insert(tk.END, "ID: " + str(record[0]) + "\n")
            text_box.insert(tk.END, "Student: " + str(record[1] or "") + "\n")
            text_box.insert(tk.END, "Amount: GHS " + str(record[2] or "") + "\n")
            text_box.insert(tk.END, "Date: " + str(record[3] or "") + "\n")
            text_box.insert(tk.END, "Term: " + str(record[4] or "") + "\n")
            text_box.insert(tk.END, "Status: " + str(record[5] or "") + "\n")
            text_box.insert(tk.END, "------------------------\n") 

def open_view_teachers():
    teacher_view_window = tk.Toplevel(window)
    teacher_view_window.title("View Teachers")
    teacher_view_window.geometry("600x400")
    teacher_view_window.configure(bg="darkblue")

    tk.Label(teacher_view_window, text="VIEW TEACHERS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    text_box = tk.Text(teacher_view_window, width=70, height=20)     
    text_box.pack(pady=10)

    cursor.execute("SELECT * FROM teachers")
    records = cursor.fetchall()

    if len(records) == 0:
        text_box.insert(tk.END, "No teachers registered yet!")
    else:
        for record in records:
            text_box.insert(tk.END, "ID: " + str(record[0] or "") + "\n")
            text_box.insert(tk.END, "Name: " + str(record[1] or "") + "\n")
            text_box.insert(tk.END, "Subject: " + str(record[2] or "") + "\n")
            text_box.insert(tk.END, "Class: " + str(record[3] or "") + "\n")
            text_box.insert(tk.END, "Phone: " + str(record[4] or "") + "\n")
            text_box.insert(tk.END, "Section: " + str(record[5] or "") + "\n")
            text_box.insert(tk.END, "------------------------\n") 

def open_update_status():
    status_window = tk.Toplevel(window)
    status_window.title("Update Student Status")
    status_window.geometry("400x300")
    status_window.configure(bg="darkblue")

    tk.Label(status_window, text="UPDATE STUDENT STATUS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(status_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(status_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(status_window, text="New Status (Active/Graduate/Transferred/Suspended):", bg="darkblue", fg="white").pack()
    status_entry = tk.Entry(status_window, width=30)
    status_entry.pack(pady=5)

    def update_status():
        search_name = name_entry.get()
        new_status = status_entry.get()
        cursor.execute(
            "UPDATE students SET status = ? WHERE name LIKE?",
            (new_status, '%' + search_name + '%')
        )
        conn.commit()
        messagebox.showinfo("Success", "Student Status Updated Successfully!")
        status_window.destroy()

    tk.Button(status_window, text="Update Status", bg="green", fg="white", font=("Arial", 12), command=update_status).pack(pady=10)

# Login credentials (simple version)
USERNAME = "admin"
PASSWORD = "schoolpro123"

def check_login():
    entered_user = user_entry.get()
    entered_pass = pass_entry.get()

    if entered_user == USERNAME and entered_pass == PASSWORD:
        login_window.destroy()
        window.deiconify()
    else:
        messagebox.showerror("Error", "Wrong username or password!")    

# Create main window
window = tk.Tk()
window.withdraw()
window.title("SchoolPro Ghana")
window.geometry("800x600")
window.configure(bg="darkblue")

# Title lable
title = tk.Label(window, text="SchoolPro Ghana", font=("Arial", 24, "bold"), bg="darkblue", fg="white")
title.pack(pady=20)

subtitle = tk.Label(window, text="School Management Software", font=("Arial", 14), bg="darkblue", fg="white")
subtitle.pack()

# Button frame
button_frame = tk.Frame(window, bg="darkblue")
button_frame.pack(pady=30)

# Buttons
btn_register = tk.Button(button_frame, text="Student Registration", font=("Arial", 12), width=25, bg="green", fg="white", command=open_registration)
btn_register.grid(row=0, column=0, pady=10, padx=10)

btn_attendance = tk.Button(button_frame, text="Attendance", font=("Arial", 12), width=25, bg="green", fg="white", command=open_attendance)
btn_attendance.grid(row=1, column=0, pady=10, padx=10)

btn_grades = tk.Button(button_frame, text="Grades & Results", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_grades)
btn_grades.grid(row=2, column=0, pady=10, padx=10)

btn_fees = tk.Button(button_frame, text="Fee Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_fees)
btn_fees.grid(row=3, column=0, pady=10, padx=10)

btn_teachers = tk.Button(button_frame, text="Teacher Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_teachers)
btn_teachers.grid(row=4, column=0, pady=10, padx=10)

btn_View_students = tk.Button(button_frame, text="View All Students", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_students)
btn_View_students.grid(row=5, column=0, pady=10, padx=10)

btn_search = tk.Button(button_frame, text="Search Student", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_search)
btn_search.grid(row=6, column=0, pady=10, padx=10)


btn_attendance_view = tk.Button(button_frame, text="View Attendance", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_attendance)
btn_attendance_view.grid(row=7, column=0, pady=10, padx=10)

btn_fees_view = tk.Button(button_frame, text="View Fees", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_fees)
btn_fees_view.grid(row=8, column=0, pady=10, padx=10)

btn_teachers_view = tk.Button(button_frame, text="View Teachers", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_teachers)
btn_teachers_view.grid(row=9, column=0, pady=10, padx=10)

btn_archive = tk.Button(button_frame, text="Update Student Status", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_update_status)
btn_archive.grid(row=10, column=0, pady=10, padx=10)

btn_exit = tk.Button(button_frame, text="Exit", font=("Arial, 12"), width=25, bg="red", fg="white", command=window.quit)
btn_exit.grid(row=11, column=0, pady=10, padx=10)

#Login window
login_window = tk.Toplevel()
login_window.title("SchoolPro Ghana - Login")
login_window.geometry("400x300")
login_window.configure(bg="darkblue")

tk.Label(login_window, text="SchoolPro Ghana", font=("Arial", 18, "bold"), bg="darkblue", fg="white").pack(pady=20)

tk.Label(login_window, text="Username:", bg="darkblue", fg="white").pack()
user_entry = tk.Entry(login_window, width=25)
user_entry.pack(pady=5)

tk.Label(login_window, text="Password:", bg="darkblue", fg="white").pack()
pass_entry = tk.Entry(login_window, width=25, show="*")
pass_entry.pack(pady=5)

tk.Button(login_window, text="Login", bg="green", fg="white", font=("Arial", 12), command=check_login).pack(pady=15)

# Start the window
window.mainloop()