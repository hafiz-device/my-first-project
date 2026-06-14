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
                                                                                                                         
# Create main window
window = tk.Tk()
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

btn_attendance = tk.Button(button_frame, text="Attendance", font=("Arial", 12), width=25, bg="green", fg="white")
btn_attendance.grid(row=1, column=0, pady=10, padx=10)

btn_grades = tk.Button(button_frame, text="Grades & Results", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_grades.grid(row=2, column=0, pady=10, padx=10)

btn_fees = tk.Button(button_frame, text="Fee Management", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_fees.grid(row=3, column=0, pady=10, padx=10)

btn_teachers = tk.Button(button_frame, text="Teacher Management", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_teachers.grid(row=4, column=0, pady=10, padx=10)

btn_View_students = tk.Button(button_frame, text="View All Students", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_View_students.grid(row=5, column=0, pady=10, padx=10)

btn_search = tk.Button(button_frame, text="Search Student", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_search.grid(row=6, column=0, pady=10, padx=10)


btn_attendance_view = tk.Button(button_frame, text="View Attendance", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_attendance_view.grid(row=7, column=0, pady=10, padx=10)

btn_fees_view = tk.Button(button_frame, text="View Fees", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_fees_view.grid(row=8, column=0, pady=10, padx=10)

btn_teachers_view = tk.Button(button_frame, text="View Teachers", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_teachers_view.grid(row=9, column=0, pady=10, padx=10)

btn_archive = tk.Button(button_frame, text="Update Student Status", font=("Arial, 12"), width=25, bg="green", fg="white")
btn_archive.grid(row=10, column=0, pady=10, padx=10)

btn_exit = tk.Button(button_frame, text="Exit", font=("Arial, 12"), width=25, bg="red", fg="white", command=window.quit)
btn_exit.grid(row=11, column=0, pady=10, padx=10)

# Start the window
window.mainloop()