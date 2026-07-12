# SchoolPro Ghana - GUI Version
# Developer: Issahak Abdul Halim (Hafiz)
# Version: 2.0

import tkinter as tk
from tkinter import messagebox
import sqlite3 
from datetime import date 
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch 
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os 
import time 

# Connect to database 
conn = sqlite3.connect("/home/hafiz/my-first-project/schoolpro.db")
cursor = conn.cursor()

def get_setting(key):
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cursor.fetchone()
    return result[0] if result else ""

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
    att_window.geometry("500x600")
    att_window.configure(bg="darkblue")

    tk.Label(att_window, text="ATTENDANCE", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(att_window, text="Select Class:", bg="darkblue", fg="white").pack()
    cursor.execute("SELECT DISTINCT class_name FROM students WHERE status='Active'")
    classes = [row[0] for row in cursor.fetchall()]
    class_var = tk.StringVar()
    class_dropdown = tk.OptionMenu(att_window, class_var, *classes)
    class_dropdown.pack(pady=5)

    tk.Label(att_window, text="Date:", bg="darkblue", fg="white").pack()
    date_entry = tk.Entry(att_window, width=30)
    date_entry.insert(0, str(date.today()))
    date_entry.pack(pady=5)

    student_entries = []

    canvas = tk.Canvas(att_window, bg="darkblue", height=250)
    scrollbar = tk.Scrollbar(att_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    students_frame = tk.Frame(canvas, bg="darkblue")
    canvas.create_window((0,0), window=students_frame, anchor="nw")
    students_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    def load_students():
        for widget in students_frame.winfo_children():
            widget.destroy()
        student_entries.clear()

        selected_class = class_var.get()
        if not selected_class:
            messagebox.showinfo("Error", "Please select a class!")
            return

        cursor.execute(
            "SELECT name FROM students WHERE class_name=? AND status='Active'",
            (selected_class,))
        students = cursor.fetchall()

        if len(students) == 0:
            messagebox.showinfo("Error", "No active students found in this class!")
            return

        for student in students:
            row = tk.Frame(students_frame, bg="darkblue")
            row.pack(pady=3, fill="x", padx=10)
            tk.Label(row, text=student[0], width=20, bg="darkblue",
                     fg="white", anchor="w").pack(side="left")
            status_var = tk.StringVar(value="Present")
            btn = tk.Button(row, text="Present", bg="green", fg="white",width=10)
            def make_toggle(v, b):
                def toggle():
                    if v.get() == "Present":
                        v.set("Absent")
                        b.config(text="Absent", bg="red")
                    else:
                        v.set("Present")
                        b.config(text="Present", bg="green")
                return toggle
            btn.config(command=make_toggle(status_var, btn))
            btn.pack(side="left", padx=5)
            student_entries.append((student[0], status_var))

    tk.Button(att_window, text="Load Students", bg="orange", fg="white", font=("Arial", 11), command=load_students).pack(pady=5)

    def save_attendance():
        if len(student_entries) == 0:
            messagebox.showinfo("Error", "Load students first!")
            return
        today = date_entry.get()
        for student_name, status_var in student_entries:
            cursor.execute(
                "INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)",
                (student_name, today, status_var.get()))                    
        conn.commit()
        messagebox.showinfo("Success", "Attendance saved for all students!")
        att_window.destroy()

    tk.Button(att_window, text="Save All Attendance", bg="green", fg="white", font=("Arial", 12), command=save_attendance).pack(pady=10)
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

    tk.Label(grades_window, text="Class Score (out of 30):", bg="darkblue", fg="white").pack()
    class_score_entry = tk.Entry(grades_window, width=30)
    class_score_entry.pack(pady=5)

    tk.Label(grades_window, text="Exam Score (out of 70):", bg="darkblue", fg="white").pack()
    exam_score_entry = tk.Entry(grades_window, width=30)
    exam_score_entry.pack(pady=5)

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
        class_score = class_score_entry.get()
        exam_score = exam_score_entry.get()
        grade = grade_entry.get()
        term = term_entry.get()
        year = year_entry.get()
        cursor.execute(
            "INSERT INTO grades(student_name, subject, class_score, exam_score, grade, term, year) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_name, subject, class_score, exam_score, grade, term, year)
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
            text_box.insert(tk.END, "Date Registered: " + str(student[8]) + "\n")
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
                text_box.insert(tk.END, "Parent: " + student[6] + "\n")
                text_box.insert(tk.END, "Phone: " + student[7] + "\n")
                text_box.insert(tk.END, "Date Registered: " + str(student[8]) + "\n")
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
            text_box.insert(tk.END, "Student: " + str(record[2]) + "\n")
            text_box.insert(tk.END, "Date: " + str(record[3]) + "\n")
            text_box.insert(tk.END, "Status: " + str(record[4]) + "\n")
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
def check_login():
    entered_user = user_entry.get()
    entered_pass = pass_entry.get()

    if entered_user == "admin" and entered_pass == get_setting('password'):
        login_window.destroy()
        window.deiconify()
    else:
        messagebox.showerror("Error", "Wrong username or password!")  

def open_report_card():
    report_window = tk.Toplevel(window)
    report_window.title("Print Report Card")
    report_window.geometry("450x550")
    report_window.configure(bg="darkblue")

    tk.Label(report_window, text="PRINT REPORT CARD", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(report_window, text="Student Name:", bg="darkblue", fg="white").pack()
    name_entry = tk.Entry(report_window, width=30)
    name_entry.pack(pady=5)

    tk.Label(report_window, text="Class:", bg="darkblue", fg="white").pack()
    class_entry = tk.Entry(report_window, width=30)
    class_entry.pack(pady=3)

    tk.Label(report_window, text="Position In Class:", bg="darkblue", fg="white").pack()
    position_entry = tk.Entry(report_window, width=30)
    position_entry.pack(pady=3)
    
    tk.Label(report_window, text="Class Size:", bg="darkblue", fg="white").pack()
    class_size_entry = tk.Entry(report_window, width=30)
    class_size_entry.pack(pady=3)

    tk.Label(report_window, text="Term:", bg="darkblue", fg="white").pack()
    term_entry = tk.Entry(report_window, width=30)
    term_entry.pack(pady=3)

    tk.Label(report_window, text="Closing Date:", bg="darkblue", fg="white").pack()
    closing_date_entry = tk.Entry(report_window, width=30)
    closing_date_entry.pack(pady=3)

    tk.Label(report_window, text="Reporting Date:", bg="darkblue", fg="white").pack()
    reporting_date_entry = tk.Entry(report_window, width=30)
    reporting_date_entry.pack(pady=3)

    tk.Label(report_window, text=" Attendance Present:", bg="darkblue", fg="white").pack()
    attendance_present_entry = tk.Entry(report_window, width=30)
    attendance_present_entry.pack(pady=3)

    tk.Label(report_window, text="Attendance Total:", bg="darkblue", fg="white").pack()
    attendance_total_entry = tk.Entry(report_window, width=30)
    attendance_total_entry.pack(pady=3)

    tk.Label(report_window, text="Conduct:", bg="darkblue", fg="white").pack()
    conduct_entry = tk.Entry(report_window, width=30)
    conduct_entry.pack(pady=3)

    tk.Label(report_window, text="Class Teacher's Remarks:", bg="darkblue", fg="white").pack()
    remarks_entry = tk.Entry(report_window, width=30)
    remarks_entry.pack(pady=3)

    tk.Label(report_window, text="Next Term School Fees (GHS):", bg="darkblue", fg="white").pack()
    fees_entry = tk.Entry(report_window, width=30)
    fees_entry.pack(pady=3)

    def generate_report():
        student_name = name_entry.get()
        cursor.execute("SELECT * FROM grades WHERE student_name = ?", (student_name,))
        grade_rows = cursor.fetchall()

        if len(grade_rows) == 0:
            messagebox.showinfo("Error", "No grades found for this student!")
            return
        # Calculate total raw score automatically by adding up all subject totals
        total_raw_score = 0
        for grade in grade_rows:
            total_raw_score += int(grade[4]) + int(grade[5])
        filename = "/home/hafiz/Desktop/" + student_name + "_report_card.pdf"

        doc = SimpleDocTemplate(filename, pagesize=A4,
            leftMargin=0.5*inch, rightMargin=0.5*inch,
            topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        suffix = str(int(time.time()))
        styles = getSampleStyleSheet()

        software_label_style = ParagraphStyle("SoftwareLabel" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
            textColor=colors.gray, spaceAfter=10)

        school_name_style = ParagraphStyle("SchoolName" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=16, alignment=TA_CENTER, spaceAfter=8)

        subtitle_style = ParagraphStyle("Subtitle" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER)  

        info_label_style = ParagraphStyle("InfoLabel" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=10, leading=14)

        info_value_style = ParagraphStyle("InfoValue" + suffix, paren=styles["Normal"],
            fontName="Helvetica", fontSize=10, leading=14)

        table_header_style = ParagraphStyle("TableHeader" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=10, alignment=TA_CENTER, textColor=colors.white)

        table_cell_style = ParagraphStyle("TableCell" + suffix, parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, alignment=TA_CENTER)

        table_subject_style = ParagraphStyle("TableSubject" + suffix, parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, alignment=TA_LEFT)

        remarks_label_style = ParagraphStyle("RemarksLabel" + suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=10, spaceAfter=2, spaceBefore=8)
        
        remarks_value_style = ParagraphStyle("RemarksValue" + suffix, parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, leading=14)
        
        story = []

        # SchoolPro Ghana watermark at the very top
        story.append(Paragraph("Generated by SchoolPro Ghana", software_label_style))

        # Logo space (left) + school name + subtitle
        logo_path = "/home/hafiz/Desktop/school_logo.png"
        if os.path.exists(logo_path):
            logo_cell = Image(logo_path, width=0.9*inch, height=0.9*inch)
        else:
            logo_cell = Paragraph("[LOGO]", ParagraphStyle("LogoPlaceholder",
                fontSize=9, alignment=TA_CENTER, textColor=colors.gray))

        header_text =[
            Paragraph("DAARIL QURAN ACADEMY &ndash; WULENSI", school_name_style),
            Paragraph("<u>STUDENT'S TERMINAL REPORT</u>", subtitle_style)
        ]        

        header_table = Table([[logo_cell, header_text]], colWidths=[1.1*inch, 6.4*inch])
        header_table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (0,0), "CENTER")
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.2*inch))

        # Student info grid
        info_data = [
            [Paragraph("Student's Name:", info_label_style), Paragraph(student_name, info_value_style),
             Paragraph("Term:", info_label_style), Paragraph(term_entry.get(), info_value_style)],
            [Paragraph("Class:", info_label_style), Paragraph(class_entry.get(), info_value_style),
             Paragraph("Closing Date:", info_label_style), Paragraph(closing_date_entry.get(), info_value_style)],
            [Paragraph("Position In Class:", info_label_style), Paragraph(position_entry.get(), info_value_style),
             Paragraph("Reporting Date:", info_label_style), Paragraph(reporting_date_entry.get(), info_value_style)],
            [Paragraph("Class Size:", info_label_style), Paragraph(class_size_entry.get(), info_value_style),
             Paragraph("", info_label_style), Paragraph("", info_value_style)],  
        ]
        info_table = Table(info_data, colWidths=[1.5*inch, 2.0*inch, 1.5*inch, 2.0*inch])
        info_table.setStyle(TableStyle([
            ("VALING", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.25*inch))

        # Academic performance table
        table_data = [[
            Paragraph("SUBJECTS", table_header_style),
            Paragraph("CLASS SCORE<br/>(30) MARKS", table_header_style),
            Paragraph("EXAM SCORE<br/>(70) MARKS", table_header_style),
            Paragraph("TOTAL MARKS<br/>SCORE", table_header_style),
        ]]

        for grade in grade_rows:
            table_data.append([
                Paragraph(str(grade[3]), table_subject_style),   # subject
                Paragraph(str(grade[4]), table_cell_style),       # class_score
                Paragraph(str(grade[5]), table_cell_style),       # exam_score
                Paragraph(str(int(grade[4]) + int(grade[5])), table_cell_style),  # total
            ])

        perf_table = Table(table_data, colWidths=[2.5*inch, 1.6*inch, 1.6*inch, 1.3*inch], repeatRows=1)
        perf_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1, 0), colors.HexColor("#1F3864")),
            ("TEXTCOLOR", (0,0), (-1, 0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.6, colors.grey),
            ("BOX", (0,0), (-1,-1), 1, colors.black),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white,colors.HexColor("#F2F2F2")]),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))    
        story.append(perf_table)
        story.append(Spacer(1, 0.3*inch))

        # Remarks section
        story.append(Paragraph("TOTAL RAW SCORE:"+ str(total_raw_score), remarks_label_style))
        story.append(Paragraph("ATTENDANCE: " + attendance_present_entry.get() + "out of" + attendance_total_entry.get(), remarks_value_style))
        story.append(Paragraph("CONDUCT: " + conduct_entry.get(), remarks_value_style))
        story.append(Paragraph("CLASS TEACHER'S REMARKS:", remarks_label_style))
        story.append(Paragraph(remarks_entry.get(), remarks_value_style))
        story.append(Paragraph("NEXT term school fees: GHS " + fees_entry.get(), remarks_label_style))
        story.append(Spacer(1, 0.5*inch))

        signature_table = Table([
            ["-------------------------", ""],
            ["Headmaster's Signature", ""],
        ], colWidths=[3*inch, 4*inch])
        signature_table.setStyle(TableStyle([
            ("ALIGN", (0,0), (0,-1), "LEFT"),
        ]))
        story.append(signature_table)

        doc.build(story)
        messagebox.showinfo("Sucess", "Report Card Generated! Check your Desktop.")
        report_window.destroy()


    tk.Button(report_window, text="Generate Report Card", bg="green", fg="white", font=("Arial", 12), command=generate_report).pack(pady=15)

def open_bulk_report_card():
    bulk_window = tk.Toplevel(window)
    bulk_window.title("Bulk Print Report Cards")
    bulk_window.geometry("500x600")
    bulk_window.configure(bg="darkblue")

    tk.Label(bulk_window, text="BULK PRINT REPORT CARDS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(bulk_window, text="Class:", bg="darkblue", fg="white").pack()
    bulk_class_entry = tk.Entry(bulk_window, width=30)
    bulk_class_entry.pack(pady=3)

    tk.Label(bulk_window, text="Term:", bg="darkblue", fg="white").pack()
    bulk_term_entry = tk.Entry(bulk_window, width=30)
    bulk_term_entry.pack(pady=3)

    tk.Label(bulk_window, text="Class Size:", bg="darkblue", fg="white").pack()
    bulk_class_size_entry = tk.Entry(bulk_window, width=30)
    bulk_class_size_entry.pack(pady=3)

    tk.Label(bulk_window, text="Closing Date:", bg="darkblue", fg="white").pack()
    bulk_closing_date_entry = tk.Entry(bulk_window, width=30)
    bulk_closing_date_entry.pack(pady=3)

    tk.Label(bulk_window, text="Reporting Date:", bg="darkblue", fg="white").pack()
    bulk_reporting_date_entry = tk.Entry(bulk_window, width=30)
    bulk_reporting_date_entry.pack(pady=3)

    tk.Label(bulk_window, text="Attendance Total:", bg="darkblue", fg="white").pack()
    bulk_attendance_total_entry = tk.Entry(bulk_window, width=30)
    bulk_attendance_total_entry.pack(pady=3)    

    tk.Label(bulk_window, text="Conduct:", bg="darkblue", fg="white").pack()
    bulk_conduct_entry = tk.Entry(bulk_window, width=30)
    bulk_conduct_entry.pack(pady=3)

    tk.Label(bulk_window, text="Class Teacher's Remarks:", bg="darkblue", fg="white").pack()
    bulk_remarks_entry = tk.Entry(bulk_window, width=30)
    bulk_remarks_entry.pack(pady=3)

    tk.Label(bulk_window, text="Next Term School Fees (GHS):", bg="darkblue", fg="white").pack()
    bulk_fees_entry = tk.Entry(bulk_window, width=30)
    bulk_fees_entry.pack(pady=3)

    tk.Label(bulk_window, text="Load students for this class, then enter position + Attendance Present for each:",
             bg="darkblue", fg="white", wraplength=400).pack(pady=10)               
    
    canvas = tk.Canvas(bulk_window, bg="darkblue", height=200)
    scrollbar = tk.Scrollbar(bulk_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    students_frame = tk.Frame(canvas, bg="darkblue")
    canvas.create_window((0,0), window=students_frame, anchor="nw")
    students_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    student_entries = []

    def load_students():
        for widget in students_frame.winfo_children():
            widget.destroy()
        student_entries.clear()

        class_name = bulk_class_entry.get()
        cursor.execute("SELECT name FROM students WHERE class_name = ?AND status = 'Active'", (class_name,))
        students = cursor.fetchall()

        if len(students) == 0:
            messagebox.showinfo("Error", "No active students found in this class!")
            return

        for student in students:
            row = tk.Frame(students_frame, bg="darkblue")
            row.pack(pady=2) 
            tk.Label(row, text=student[0], width=20, bg="darkblue", fg="white", anchor="w").pack(side="left")
            tk.Label(row, text="Position:", bg="darkblue", fg="white").pack(side="left")
            pos_entry = tk.Entry(row, width=5)
            pos_entry.pack(side="left", padx=3)
            tk.Label(row, text="Present:", bg="darkblue", fg="white").pack(side="left")
            present_entry = tk.Entry(row, width=5)
            present_entry.pack(side="left", padx=3)
            student_entries.append((student[0], pos_entry, present_entry))

    tk.Button(bulk_window, text="Load students", bg="orange", fg="white", command=load_students).pack(pady=5)

    def generate_bulk_reports():
        class_name = bulk_class_entry.get()
        if len(student_entries) == 0:
            messagebox.showinfo("Error", "Loadd student first!")
            return

        success_count = 0 
        skipped = []

        for student_name, pos_entry, present_entry in student_entries:
            cursor.execute("SELECT * FROM grades WHERE student_name = ?", (student_name,))
            grade_rows = cursor.fetchall()

            if len(grade_rows) == 0:
                skipped.append(student_name)
                continue
            total_raw_score = 0
            for grade in grade_rows:
                total_raw_score += int(grade[4]) + int(grade[5])

            filename = "/home/hafiz/Desktop/" + student_name + "_report_card_pdf"

            doc = SimpleDocTemplate(filename, pagesize=A4,
                leftMargin=0.5*inch, rightMargin=0.5*inch,
                topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            suffix = str(int(time.time()))
            styles = getSampleStyleSheet()  

            software_label_style = ParagraphStyle("SoftwareLabel" + suffix, parent=styles["Normal"],
                fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER, 
                textColor=colors.gray, spaceAfter=10)

            school_name_style = ParagraphStyle("SchoolName" + suffix, parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=16, alignment=TA_CENTER, spacsAfter=8)

            subtitle_style = ParagraphStyle("Subtitle" + suffix, parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER)

            info_label_style = ParagraphStyle("InfoLabel" + suffix, parent=styles["Normal"],
                fontNmae="Helvetica-Bold", fontSize=10, leading=14)

            info_value_style = ParagraphStyle("InfoValue" + suffix, parent=styles["Normal"],
                fontName="Helvetica", fontSize=10, leading=14)

            table_header_style = ParagraphStyle("TableHeader" + suffix, parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=10, alignment=TA_CENTER, textColor=colors.white)

            table_cell_style = ParagraphStyle("TableCall" + suffix, parent=styles["Normal"], 
                fontName="Helvetica", fontSize=10, alignment=TA_CENTER)

            table_subject_style = ParagraphStyle("TableSubject" + suffix, parent=styles["Normal"],
                fontName="Helvetica", fontSize=10, alignment=TA_LEFT)

            remarks_label_style = ParagraphStyle("RemarksLabel" + suffix, parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=10, spaceAfter=2, spaceBefore=8)
            
            remarks_value_style = ParagraphStyle("RemarksValue" + suffix, parent=styles["Normal"],
                fontName="Helvetica", fontSize=10, leading=14)
            
            story = []

            story.append(Paragraph("Generated by SchoolPro Ghana", software_label_style))

            logo_path = "/home/hafiz/Desktop/school_logo.png"
            if os.path.exists(logo_path):
                logo_cell = Image(logo_path, width=0.9*inch, height=0.9*inch)
            else:
                logo_cell = Paragraph("[LOGO]", ParagraphStyle("LogoPlaceholder",
                    fontSize=9, alignment=TA_CENTER, textColor=colors.gray))

            header_text =[
                Paragraph("DAARIL QURAN ACADEMY &ndash; WULENSI", school_name_style),
                Spacer(1, 0.1*inch),
                Paragraph("<u>STUDENT'S TERMINAL REPORT</u>", subtitle_style)
            ]        

            header_table = Table([[logo_cell, header_text]], colWidths=[1.1*inch, 6.4*inch])
            header_table.setStyle(TableStyle([
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("ALIGN", (0,0), (0,0), "CENTER")
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            info_data = [
                [Paragraph("Student's Name:", info_label_style), Paragraph(student_name, info_value_style),
                 Paragraph("Term:", info_label_style), Paragraph(bulk_term_entry.get(), info_value_style)],
                [Paragraph("Class:", info_label_style), Paragraph(class_name, info_value_style),
                 Paragraph("Closing Date:", info_label_style), Paragraph(bulk_closing_date_entry.get(), info_value_style)],
                [Paragraph("Position In Class:", info_label_style), Paragraph(pos_entry.get(), info_value_style),
                 Paragraph("Reporting Date:", info_label_style), Paragraph(bulk_reporting_date_entry.get(), info_value_style)],
                [Paragraph("Class Size:", info_label_style), Paragraph(bulk_class_size_entry.get(), info_value_style),
                 Paragraph("", info_label_style), Paragraph("", info_value_style)],  
            ]
            info_table = Table(info_data, colWidths=[1.5*inch, 2.0*inch, 1.5*inch, 2.0*inch])
            info_table.setStyle(TableStyle([
                ("VALING", (0,0), (-1,-1), "TOP"),
                ("TOPPADDING", (0,0), (-1,-1), 3),
                ("BOTTOMPADDING", (0,0), (-1,-1), 3)
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.25*inch))

            table_data = [[
                Paragraph("SUBJECTS", table_header_style),
                Paragraph("CLASS SCORE<br/>(30) MARKS", table_header_style),
                Paragraph("EXAM SCORE<br/>(70) MARKS", table_header_style),
                Paragraph("TOTAL MARKS<br/>SCORE", table_header_style),
            ]]

            for grade in grade_rows:
                table_data.append([
                    Paragraph(str(grade[3]), table_subject_style),   
                    Paragraph(str(grade[4]), table_cell_style),       
                    Paragraph(str(grade[5]), table_cell_style),       
                    Paragraph(str(int(grade[4]) + int(grade[5])), table_cell_style),  
                ])

            perf_table = Table(table_data, colWidths=[2.5*inch, 1.6*inch, 1.6*inch, 1.3*inch], repeatRows=1)
            perf_table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1, 0), colors.HexColor("#1F3864")),
                ("TEXTCOLOR", (0,0), (-1, 0), colors.white),
                ("GRID", (0,0), (-1,-1), 0.6, colors.grey),
                ("BOX", (0,0), (-1,-1), 1, colors.black),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white,colors.HexColor("#F2F2F2")]),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]))    
            story.append(perf_table)
            story.append(Spacer(1, 0.3*inch))

            story.append(Paragraph("TOTAL RAW SCORE:"+ str(total_raw_score), remarks_label_style))
            story.append(Paragraph("ATTENDANCE: " + present_entry.get() + "out of" + bulk_attendance_total_entry.get(), remarks_value_style))
            story.append(Paragraph("CONDUCT: " +bulk_conduct_entry.get(), remarks_value_style))
            story.append(Paragraph("CLASS TEACHER'S REMARKS:", remarks_label_style))
            story.append(Paragraph(bulk_remarks_entry.get(), remarks_value_style))
            story.append(Paragraph("NEXT term school fees: GHS " + bulk_fees_entry.get(), remarks_label_style))
            story.append(Spacer(1, 0.5*inch))

            signature_table = Table([
                ["-------------------------", ""],
                ["Headmaster's Signature", ""],
            ], colWidths=[3*inch, 4*inch])
            signature_table.setStyle(TableStyle([
                ("ALIGN", (0,0), (0,-1), "LEFT"),
            ]))
            story.append(signature_table)

            doc.build(story)
            success_count += 1

        msg = f"Denerated {success_count} reportcard(s) on your Desktop."
        if skipped:
            msg += "\n\nSkipped (no grades found): " + ", ".join(skipped)
        messagebox.showinfo("Bulk Generation Complete", msg)
        bulk_window.destroy()

    tk.Button(bulk_window, text="Generate All Report Cards", bg="green", fg="white",
              font=("Arial", 12), command=generate_bulk_reports).pack(pady=15)

def open_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("450x550")
    settings_window.configure(bg="darkblue")

    tk.Label(settings_window, text="SETTINGS", font=("Arial", 16, "bold"),
             bg="darkblue", fg="white").pack(pady=10)

    fields = {}

    labels = [
        ("school_name", "School Name:"),
        ("school_address", "School Address:"),
        ("currency", "Currency (e.g. GHS):"),
        ("house_name", "House Names (comma-separated):"),
        ("grade_A", "Minimum Score for A:"),
        ("grade_B", "Minimum Score for B:"),
        ("grade_C", "Minimum Score for C:"),
        ("grade_D", "Minimum Score for D:"),
    ]                           

    for key, label in labels:
        tk.Label(settings_window, text=label, bg="darkblue", fg="white").pack()
        entry = tk.Entry(settings_window, width=35)
        entry.insert(0, get_setting(key))
        entry.pack(pady=3)
        fields[key] = entry

    def save_settings():
        for key, entry in fields.items():
            cursor.execute("UPDATE settings SET value = ? WHERE key = ?",
                           (entry.get(), key))
        conn.commit()
        messagebox.showinfo("Success", "Settings saved successfully!")
        settings_window.destroy()

    tk.Button(settings_window, text="Save Settings", bg="green", fg="white", 
              font=("Arial", 12), command=save_settings).pack(pady=15)
    
    tk.Label(settings_window, text="---- Change Password ----", bg="darkblue", fg="white").pack(pady=5)

    tk.Label(settings_window, text="Old Password:", bg="darkblue", fg="white").pack()
    old_pass_entry = tk.Entry(settings_window, width=35, show="*")
    old_pass_entry.pack(pady=3)

    tk.Label(settings_window, text="New Password:", bg="darkblue", fg="white").pack()
    new_pass_entry = tk.Entry(settings_window, width=35, show="*")
    new_pass_entry.pack(pady=3)

    tk.Label(settings_window, text="Confirm New Password:", bg="darkblue", fg="white").pack()
    confirm_pass_entry = tk.Entry(settings_window, width=35, show="*")
    confirm_pass_entry.pack(pady=3)

    def change_password(): 
        old_pw = old_pass_entry.get()
        new_pw = new_pass_entry.get()
        confirm_pw = confirm_pass_entry.get()
        if old_pw != get_setting('password'):
            messagebox.showerror("Error", "old password is incorrect!")
            return
        if new_pw == "":
            messagebox.showerror("Error", "New password cannot be empty!")
            return
        if new_pw != confirm_pw:
            messagebox.showerror("Error", "New passwords do not match!")
            return
        cursor.execute("UPDATE settings SET value = ? WHERE key ='password'", (new_pw,))
        conn.commit()
        messagebox.showinfo("Success", "Password changed successfully!")

    tk.Button(settings_window, text="Change Password", bg="orange", fg="white", font=("Arial", 12), command=change_password).pack(pady=10)

def backup_database():
    import shutil
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schoolpro.db")
    dst = os.path.join(os.path.expanduser("~"), "Desktop", "schoolpro_backup_" + timestamp + ".db")
    shutil.copy2(src, dst)
    messagebox.showinfo("Backup Complete",
        "Database backed up to Desktop as:\nschoolpro_backup_" + timestamp + ".db")
            
# Create main window
window = tk.Tk()
window.withdraw()
window.title("SchoolPro Ghana")
window.geometry("800x600")
window.configure(bg="darkblue")

# Title lable
title = tk.Label(window, text="SchoolPro Ghana", font=("Arial", 24, "bold"), bg="darkblue", fg="white")
title.pack(pady=20)

# Dashboard - Statistics
def get_stats():
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT amount FROM fees")
    all_fees = cursor.fetchall()
    total_fees = 0
    for fee in all_fees:
        try:
            total_fees += float(fee[0])
        except:
            pass    

    return total_students, total_teachers, total_fees

total_students, total_teachers, total_fees = get_stats()

stats_frame = tk.Frame(window,bg="darkblue")
stats_frame.pack(pady=10)

tk.Label(stats_frame, text="Total Students: " + str(total_students), font=("Arial", 12), bg="darkblue", fg="yellow").pack()
tk.Label(stats_frame, text="Total Teachers: " + str(total_teachers), font=("Arial", 12), bg="darkblue", fg="yellow").pack()
tk.Label(stats_frame, text="Total Fees Collected: GHS " + str(total_fees), font=("Arial", 12), bg="darkblue", fg="yellow").pack()

subtitle = tk.Label(window, text="School Management Software", font=("Arial", 14), bg="darkblue", fg="white")
subtitle.pack()

# Button frame
button_frame = tk.Frame(window, bg="darkblue")
button_frame.pack(pady=30)

# Buttons
btn_register = tk.Button(button_frame, text="Student Registration", font=("Arial", 12), width=25, bg="green", fg="white", command=open_registration)
btn_register.grid(row=0, column=0, pady=4, padx=4)

btn_attendance = tk.Button(button_frame, text="Attendance", font=("Arial", 12), width=25, bg="green", fg="white", command=open_attendance)
btn_attendance.grid(row=1, column=0, pady=4, padx=4)

btn_grades = tk.Button(button_frame, text="Grades & Results", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_grades)
btn_grades.grid(row=2, column=0, pady=4, padx=4)

btn_fees = tk.Button(button_frame, text="Fee Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_fees)
btn_fees.grid(row=3, column=0, pady=4, padx=4)

btn_teachers = tk.Button(button_frame, text="Teacher Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_teachers)
btn_teachers.grid(row=4, column=0, pady=4, padx=4)

btn_View_students = tk.Button(button_frame, text="View All Students", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_students)
btn_View_students.grid(row=5, column=0, pady=4, padx=4)

btn_search = tk.Button(button_frame, text="Search Student", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_search)
btn_search.grid(row=6, column=0, pady=4, padx=4)


btn_attendance_view = tk.Button(button_frame, text="View Attendance", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_attendance)
btn_attendance_view.grid(row=7, column=0, pady=4, padx=4)

btn_fees_view = tk.Button(button_frame, text="View Fees", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_fees)
btn_fees_view.grid(row=8, column=0, pady=4, padx=4)

btn_teachers_view = tk.Button(button_frame, text="View Teachers", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_teachers)
btn_teachers_view.grid(row=9, column=0, pady=4, padx=4)

btn_archive = tk.Button(button_frame, text="Update Student Status", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_update_status)
btn_archive.grid(row=10, column=0, pady=4, padx=4)

btn_report = tk.Button(button_frame, text="Print Report Card", font=("Arial", 12), width=25, bg="purple", fg="white", command=open_report_card)
btn_report.grid(row=11, column=0, pady=4, padx=4)

btn_bulk = tk.Button(button_frame, text="Bulk Print Report Cards", font=("Arial", 12), width=25, bg="purple", fg="white", command=open_bulk_report_card)
btn_bulk.grid(row=12, column=0, pady=4, padx=4)

btn_settings = tk.Button(button_frame, text="Settings", font=("Arial, 12"), width=25, bg="gray", fg="white", command=open_settings)
btn_settings.grid(row=13, column=0, pady=4, padx=10)

btn_backup = tk.Button(button_frame, text="Backup Database", font=("Arial", 12), width=25, bg="teal", fg="white", command=backup_database)
btn_backup.grid(row=14, column=0, pady=4, padx=10)

btn_exit = tk.Button(button_frame, text="Exit", font=("Arial, 12"), width=25, bg="red", fg="white", command=window.quit)
btn_exit.grid(row=15, column=0, pady=4, padx=4)

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