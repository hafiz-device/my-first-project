# SchoolPro Ghana - GUI Version
# Developer: Issahak Abdul Halim (Hafiz)
# Version: 2.0

import tkinter as tk
from tkinter import messagebox
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
from database import conn, cursor

def get_setting(key):
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cursor.fetchone()
    return result[0] if result else ""

def get_grade(total_score):
    try:
        grade_A = int(get_setting('grade_A'))
        grade_B = int(get_setting('grade_B'))
        grade_C = int(get_setting('grade_C'))
        grade_D = int(get_setting('grade_D'))
        if total_score >= grade_A:
            return 'A'
        elif total_score >= grade_B:
            return 'B'
        elif total_score >= grade_C:
            return 'C'
        elif total_score >= grade_D:
            return 'D'
        else:
            return 'F'
    except:
        return 'N/A'   

def generate_student_id():
    from datetime import datetime
    year = datetime.now().year
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0] + 1
    return f"SPG-{year}-{count:05d}"

def get_teacher_info(full_name):
    """
    Returns a list of assignments for a teacher, e.g:
    [{'subject': 'Math', 'class_name': 'Class 4', 'section': 'Academic'}, ...]
    Returns an empty list if no assignments are found.
    """
    cursor.execute("""
        SELECT subject, class_name, section
        FROM teacher_assignments
        WHERE UPPER(teacher_name) = UPPER(?)
    """, (full_name,))
    rows = cursor.fetchall()
    assignments = []
    for row in rows:
        assignments.append({
            "subject": row[0],
            "class_name": row[1],
            "section": row[2]
        })              
    return assignments

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

    tk.Label(reg_window, text="House:", bg="darkblue", fg="white").pack()
    house_names = get_setting('house_name').split(',')
    house_var = tk.StringVar(value=house_names[0])
    house_dropdown = tk.OptionMenu(reg_window, house_var, *house_names)
    house_dropdown.pack(pady=5)

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

        house = house_var.get()
        student_code = generate_student_id()
        cursor.execute(
            "INSERT INTO students (name, age, gender, class_name, section, house, parent_name, parent_phone, date_registered, student_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, gender, class_name, section, house, parent_name, parent_phone, today, student_code)
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
    fee_window.geometry("550x650")
    fee_window.configure(bg="darkblue")

    tk.Label(fee_window, text="FEE MANAGEMET", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    top_frame = tk.Frame(fee_window, bg="darkblue")
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Class:", bg="darkblue", fg="white").pack(side="left", padx=5)
    cursor.execute("SELECT DISTINCT class_name FROM students WHERE status='Active'")
    classes = [row[0] for row in cursor.fetchall()]
    class_var = tk.StringVar()
    class_dropdown = tk.OptionMenu(top_frame, class_var, *classes)
    class_dropdown.pack(side="left", padx=5)

    tk.Label(top_frame, text="Term:", bg="darkblue", fg="white").pack(side="left", padx=5)
    term_var = tk.StringVar()
    term_dropdown = tk.OptionMenu(top_frame, term_var, "1", "2", "3")
    term_dropdown.pack(side="left", padx=5)

    tk.Label(fee_window, text="Expected Amount (GHS):", bg="darkblue", fg="white").pack()
    expected_entry = tk.Entry(fee_window, width=20)
    expected_entry.pack(pady=3)

    student_entries = []

    canvas = tk.Canvas(fee_window, bg="darkblue", height=300)
    scrollbar = tk.Scrollbar(fee_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    students_frame = tk.Frame(canvas, bg="darkblue")
    canvas.create_window((0,0),window=students_frame, anchor="nw")
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
            messagebox.showinfo("Error", "No active students found!")
            return
        for student in students: 
            row = tk.Frame(students_frame, bg="darkblue")
            row.pack(pady=3, fill="x", padx=10)

            tk.Label(row, text=student[0], width=20, bg="darkblue", fg="white", anchor="w").pack(side="left")

            status_var = tk.StringVar(value="Not Paid")
            status_btn = tk.Button(row, text="Not Paid", bg="red", fg="white", width=12)

            amount_entry =tk.Entry(row, width=8)
            amount_entry.insert(0, expected_entry.get())

            def make_toggle(v, b):
                def toggle():
                    if v.get() == "Not Paid":
                        v.set("Full Payment")
                        b.config(text="Full Payment", bg="green")
                    elif v.get() == "Full Payment":
                        v.set("Partial Payment")
                        b.config(text="Partial", bg="orange")
                    else:
                        v.set("Not Paid")
                        b.config(text="Not Paid", bg="red")
                return toggle

            status_btn.config(command=make_toggle(status_var, status_btn))
            status_btn.pack(side="left", padx=5)
            amount_entry.pack(side="left", padx=3)
            student_entries.append((student[0], status_var, amount_entry))

    tk.Button(fee_window, text="Load Students", bg="orange", fg="white", font=("Arial", 11), command=load_students).pack(pady=5)

    def save_fees():
        if len(student_entries) == 0:
            messagebox.showinfo("Error", "Load students first!")
            return
        term = term_var.get()
        if not term:
            messagebox.showinfo("Error", "Please select a term!")
            return
        today = str(date.today())
        for student_name, status_var, amount_entry in student_entries:
            status = status_var.get()
            amount = amount_entry.get()
            cursor.execute(
                "INSERT INTO fees (student_name, amount, date, term, status) VALUES (?, ?, ?, ?, ?)",
                (student_name, amount, today, term, status))                               
        conn.commit()

        # Ask if they want to generate receipts
        generate = messagebox.askyesno("Generate Receipts",
            "Fee records saved! Do you want to generate PDF receipts for students who paid?")
        
        if generate:
            import shutil
            suffix = str(int(time.time()))
            receipt_count = 0
            for student_name, status_var, amount_entry in student_entries:
                status = status_var.get()
                if status in "Full Payment":
                    amount = amount_entry.get()
                    receipt_num = "REC-" + str(int(time.time())) + "-" + str(receipt_count)
                    filename = os.path.join(os.path.expanduser("~"), "Desktop",
                        student_name + "_fee_receipt.pdf")

                    doc = SimpleDocTemplate(filename, pagesize=A4,
                        leftMargin=0.75*inch, rightMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle("RTitle" + suffix, parent=styles["Normal"],
                        fontName="Helvetica-Bold", fontSize=18, alignment=TA_CENTER, spaceAfter=10)
                    center_style = ParagraphStyle("RCenter" + suffix, parent=styles["Normal"],
                        fontName="Helvetica", fontSize=11, alignment=TA_CENTER, spaceAfter=6)
                    labe_style = ParagraphStyle("RLabel" + suffix, parent=styles["Normal"],
                        fontName="Helvetica-Bold", fontSize=11, spaceAfter=4)
                    value_style= ParagraphStyle("RValue" + suffix, parent=styles["Normal"],
                        fontName="Helvetica", fontSize=11, spaceAfter=4)

                    story =[]
                    story.append(Paragraph("Generated by SchoolPro Ghana",
                        ParagraphStyle("FRWater"+suffix, parent=styles["Normal"],
                        fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
                        textColor=colors.gray, spaceAfter=10)))
                    story.append(Paragraph(get_setting('school_name'), title_style))
                    story.append(Paragraph("OFFICIAL FEE RECEIPT", center_style))
                    story.append(Spacer(1, 0.2*inch))

                    receipt_data = [
                        ["Receipt No:", receipt_num],
                        ["Student Name:", student_name],
                        ["Term:", term],
                        ["Amount Paid:", f"GHS {amount}"],
                        ["Payment Status:", status],
                    ]

                    receipt_table = Table(receipt_data, colWidths=[2*inch, 4*inch])
                    receipt_table.setStyle(TableStyle([
                        ("GRID", (0,0), (-1,-1), 0.5, colors.gray),
                        ("TOPPADDING", (0,0), (-1,-1), 6),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EBF3FF")),
                    ]))            
                    story.append(receipt_table)
                    story.append(Spacer(1, 0.5*inch))

                    sig_data = [
                        ["________________________", "________________________"],
                        ["Headmaster's Signature", "Accountant's Signature"],
                    ]
                    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
                    sig_table.setStyle(TableStyle([
                        ("ALIGN", (0,0), (-1,-1), "CENTER"),
                        ("FONTNAME", (0,1), (-1,-1), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,-1), 10),
                    ]))
                    story.append(sig_table)

                    doc.build(story)
                    receipt_count += 1
                    suffix = str(int(time.time())) + str(receipt_count)

            if receipt_count > 0:
                messagebox.showinfo("Success", str(receipt_count) + " receipt(s) save to Desktop!")
            else:
                messagebox.showinfo("Info", "No paid students - no receipts generated.")
        else:
            messagebox.showinfo("Success", "Fee records saved successfully!")

        fee_window.destroy                        

    tk.Button(fee_window, text="Save All Fee Records", bg="green", fg="white", font=("Arial, 12"), command=save_fees).pack(pady=10)  

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

def open_assign_teacher():
    assign_window = tk.Toplevel(window)
    assign_window.title("Assign Class")
    assign_window.configure(bg="darkblue")

    window_width = 550
    window_height = 650
    screen_width = assign_window.winfo_screenwidth()
    screen_height = assign_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    assign_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(assign_window, text="ASSIGN CLASS/SUBJECT", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(assign_window, text="Teacher Name:", bg="darkblue", fg="white").pack()
    cursor.execute("SELECT DISTINCT name FROM teachers")
    teacher_names = [row[0] for row in cursor.fetchall()]  
    teacher_var = tk.StringVar()
    teacher_dropdown = tk.OptionMenu(assign_window, teacher_var, *teacher_names)
    teacher_dropdown.pack(pady=5)

    tk.Label(assign_window, text="Section (Academic/Islamic):", bg="darkblue", fg="white").pack()
    section_entry = tk.Entry(assign_window, width=30)
    section_entry.pack(pady=5)

    tk.Label(assign_window, 
             text="This assigns EVERY checked subject to EVERY checked class.\n"
                  "if this teacher teaches different subjects to different classes,\n"
                  "save separatly for each class.",
            bg="darkblue", fg="yellow", font=("Arial", 9), justify="center").pack(pady=10)

    main_frame = tk.Frame(assign_window, bg="darkblue")
    main_frame.pack(pady=10, fill="both", expand=True)

    subjects_col = tk.Frame(main_frame, bg="darkblue")
    subjects_col.pack(side="left", padx=15, anchor="n", fill="both", expand=True)

    classes_col = tk.Frame(main_frame, bg="darkblue")
    classes_col.pack(side="left", padx=15, anchor="n", fill="both", expand=True)

    # --- subjects (scrollabel) ---
    tk.Label(subjects_col, text="select Subjects:", bg="darkblue", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 5))

    subjects_text = get_setting('subjects')
    subject_list = [s.strip() for s in subjects_text.splitlines() if s.strip()]
    subject_vars ={}

    subject_canvas = tk.Canvas(subjects_col, bg="darkblue", height=200, width=180, highlightthickness=0)
    subject_scrollbar = tk.Scrollbar(subjects_col, orient="vertical", command=subject_canvas.yview)
    subject_canvas.configure(yscrollcommand=subject_scrollbar.set)
    subject_canvas.pack(side="left", fill="both", expand=True)
    subject_scrollbar.pack(side="right", fill="y")

    subject_list_frame = tk.Frame(subject_canvas, bg="darkblue")
    subject_canvas.create_window((0, 0), window=subject_list_frame, anchor="nw")
    subject_list_frame.bind("<Configure>", lambda e: subject_canvas.configure(scrollregion=subject_canvas.bbox("all")))


    if not subject_list:
        tk.Label(subject_list_frame, text="No subjects found.\nAdd them in  Settings .", bg="darkblue", fg="yellow").pack()
    else:
        for subject in subject_list:
            var = tk.BooleanVar()
            subject_vars[subject] = var
            tk.Checkbutton(subject_list_frame, text=subject, variable=var, bg="darkblue", fg="white", selectcolor="green",
                            font=("Arial", 11), anchor="w").pack(fill="x")

    # --- Classes (scrollable) ---
    tk.Label(classes_col, text="Select Classes:", bg="darkblue", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 5))
    
    cursor.execute("SELECT DISTINCT class_name FROM students WHERE status='Active'")
    class_names = [row[0] for row in cursor.fetchall()]
    class_vars = {}
    
    class_canvas = tk.Canvas(classes_col, bg="darkblue", height=200, width=180, highlightthickness=0)
    class_scrollbar = tk.Scrollbar(classes_col, orient="vertical", command=class_canvas.yview)
    class_canvas.configure(yscrollcommand=class_scrollbar.set)
    class_canvas.pack(side="left", fill="both", expand=True)
    class_scrollbar.pack(side="right", fill="y")
    
    class_list_frame = tk.Frame(class_canvas, bg="darkblue")
    class_canvas.create_window((0, 0), window=class_list_frame, anchor="nw")
    class_list_frame.bind("<Configure>", lambda e: class_canvas.configure(scrollregion=class_canvas.bbox("all")))
    
    
    if not class_names:
            tk.Label(class_list_frame, text="No classes found.", bg="darkblue", fg="yellow").pack()
    else:
        for class_name in class_names:
            var = tk.BooleanVar()
            class_vars[class_name] = var
            tk.Checkbutton(class_list_frame, text=class_name, variable=var, bg="darkblue", fg="white", selectcolor="green",
                                font=("Arial", 11), anchor="w").pack(fill="x")
            
    # --- Save with confirmation ---
    def save_assignment():
        teacher_name = teacher_var.get()
        section = section_entry.get()
        selected_subjects = [subj for subj, var in subject_vars.items() if var.get()]
        selected_classes = [cls for cls, var in class_vars.items() if var.get()]

        if not teacher_name:
            messagebox.showinfo("Error", "Please select a teacher!")
            return
        if not selected_subjects:
            messagebox.showinfo("Error", "Please select at least one subject!")
            return
        if not selected_classes:
            messagebox.showinfo("Error", "Please select at least one class!")
            return

        preview_lines = []
        for subject in selected_subjects:
             for class_name in selected_classes:
                 preview_lines.append(f"{subject} - {class_name}")

        preview_text = "\n".join(preview_lines)
        confirm = messagebox.askyesno("Confirm Assignment", f"This willcreate the following {len(preview_lines)} assignment(s) for {teacher_name}:\n\n" f"{preview_text}\n\nContinue?", parent=assign_window)
        if not confirm:
             return

        count = 0
        for subject in selected_subjects:
             for class_name in selected_classes:
                cursor.execute("""
                    INSERT INTO teacher_assignments (teacher_name, subject, class_name, section) VALUES (?, ?, ?, ?)
                """, (teacher_name, subject, class_name, section))
                count += 1
        conn.commit()
        messagebox.showinfo("Success", f"{count} assignment(s) created for {teacher_name}!")
        assign_window.destroy()

    tk.Button(assign_window, text="Save Assignment(s)", bg="green", fg="white", font=("Arial", 12), command=save_assignment).pack(pady=20)      

def open_view_students():
    view_window = tk.Toplevel(window)
    view_window.title("All Students")
    view_window.geometry("600x450")
    view_window.configure(bg="darkblue")

    tk.Label(view_window, text="ALL STUDENTS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    # Text box to display students
    filter_frame = tk.Frame(view_window, bg="darkblue")
    filter_frame.pack()

    tk.Label(filter_frame, text="Filter by Section:", bg="darkblue", fg="white").pack(side="left", padx=5)
    section_var = tk.StringVar(value="All")
    section_dropdown = tk.OptionMenu(filter_frame, section_var, "All", "Academic", "Islamic")
    section_dropdown.pack(side="left", padx=5)

    tk.Label(filter_frame, text="Filter by House:", bg="darkblue", fg="white").pack(side="left", padx=5)
    house_var = tk.StringVar(value="All")
    house_options = ["All"] + get_setting('house_name').split(',')
    house_dropdown = tk.OptionMenu(filter_frame, house_var, *house_options)
    house_dropdown.pack(side="left", padx=5)

    tk.Button(filter_frame, text="Filter", bg="orange", fg="white", command=lambda: show_students()).pack(side="left", padx=5)

    text_box = tk.Text(view_window, width=70, height=20)
    text_box.pack(pady=10)

    def show_students():
        text_box.delete(1.0, tk.END)
        section = section_var.get()
        house = house_var.get()

        if section == "All" and house == "All":
            cursor.execute("SELECT * FROM students")
        elif section == "All":
            cursor.execute("SELECT * FROM students WHERE house=?", (house,))
        elif house == "All":
            cursor.execute("SELECT * FROM students WHERE UPPER(section)=UPPER(?)", (section,))   
        else:
            cursor.execute("SELECT * FROM students WHERE UPPER(section)=UPPER(?) AND UPPER(house)=UPPER(?)",
                           (section, house))

        students = cursor.fetchall()            

        if len(students) == 0:
            text_box.insert(tk.END, "No students found!")
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
                text_box.insert(tk.END, "Student ID: " + str(student[10]) + "\n")
                text_box.insert(tk.END, "House: " + str(student[11]) + "\n")
                text_box.insert(tk.END, "------------------------\n")

    show_students()        

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
    fee_view_window.geometry("600x500")
    fee_view_window.configure(bg="darkblue")

    tk.Label(fee_view_window, text="VIEW FEES", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    top_frame = tk.Frame(fee_view_window, bg="darkblue")
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Class:", bg="darkblue", fg="white").pack(side="left", padx=5)
    cursor.execute("SELECT DISTINCT class_name FROM students WHERE status='Active'")
    classes = [row[0] for row in cursor.fetchall()]
    class_var = tk.StringVar()
    class_dropdown = tk.OptionMenu(top_frame, class_var, *classes)
    class_dropdown.pack(side="left", padx=5)

    tk.Label(top_frame, text="Term:", bg="darkblue", fg="white").pack(side="left", padx=5)
    term_var = tk.StringVar()
    term_dropdown = tk.OptionMenu(top_frame, term_var, "1", "2", "3")
    term_dropdown.pack(side="left", padx=5)

    tk.Button(top_frame, text="Search", bg="orange", fg="white", command=lambda: show_fees()).pack(side="left", padx=5)

    text_box = tk.Text(fee_view_window, width=70, height=22)
    text_box.pack(pady=10)

    def show_fees():
        text_box.delete(1.0, tk.END)
        selected_class = class_var.get()
        term = term_var.get()

        if not selected_class or not term:
            messagebox.showinfo("Error", "Please select class and term!")
            return
        
        cursor.execute(
            "SELECT name FROM students WHERE class_name=? AND status='Active'",
            (selected_class,))
        students = cursor.fetchall()

        full_payment = []
        partial_payment = []
        not_paid = []

        for student in students:
            cursor.execute(
                "SELECT amount, status FROM fees WHERE student_name=? AND term=? ORDER BY date DESC LIMIT 1",
                (student[0], term))
            fee = cursor.fetchone()
            if fee:
                if fee[1] == "Full Payment":
                    full_payment.append((student[0], fee[0]))
                elif fee[1] == "Partial Payment":
                    partial_payment.append((student[0], fee[0]))
                else:
                    not_paid.append(student[0])
            else:
                not_paid.append(student[0])

        text_box.insert(tk.END, f"CLASS: {selected_class} | TERM: {term}\n")
        text_box.insert(tk.END, "="*50 + "\n\n")  

        text_box.insert(tk.END, f"FULL PAYMENT ({len(full_payment)}):\n")
        for name, amount in full_payment:
            text_box.insert(tk.END, f" {name} - GHS {amount}\n")

        text_box.insert(tk.END, f"\nPARTIAL PAYMENT ({len(partial_payment)}):\n")
        for nmae, amount in partial_payment:
            text_box.insert(tk.END, f" {name} - GHS {amount}\n")

        text_box.insert(tk.END, f"\nNOT PAID ({len(not_paid)}):\n")
        for name in not_paid:
            text_box.insert(tk.END, f" {name}\n")

        text_box.insert(tk.END, f"\n" + "="*50 + "\n")
        text_box.insert(tk.END, f"Total Paid: {len(full_payment)} | Partial: {len(partial_payment)} | Not Paid: {len(not_paid)}\n")        

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

current_user_role = ""
current_user_name = ""

def check_login():
    global current_user_role, current_user_name
    entered_user = user_entry.get()
    entered_pass = pass_entry.get()

    cursor.execute("SELECT role, full_name FROM users WHERE username=? AND password=?",
                   (entered_user, entered_pass))
    result = cursor.fetchone()

    if result:
        current_user_role = result[0]
        current_user_name = result[1]
        login_window.destroy()
        window.deiconify()
        apply_role(current_user_role)
    else:
        messagebox.showinfo("Error", "Wrong username or password!") 

def apply_role(role):
    if role == "admin":
        # Show all bottuns
        # --- COLUMN 0 (LEFT) ---
        btn_register.grid(row=0, column=0, pady=3, padx=5)
        btn_attendance.grid(row=1, column=0, pady=3, padx=5)
        btn_grades.grid(row=2, column=0, pady=3, padx=5)
        btn_fees.grid(row=3, column=0, pady=3, padx=5)
        btn_teachers.grid(row=4, column=0, pady=3, padx=5)
        btn_view_students.grid(row=5, column=0, pady=3, padx=5)

        # --- COLUMN 1 (MIDDLE) ---
        btn_search.grid(row=0, column=1, pady=3, padx=5)
        btn_attendance_view.grid(row=1, column=1, pady=3, padx=5)
        btn_fees_view.grid(row=2, column=1, pady=3, padx=5)
        btn_teachers_view.grid(row=3, column=1, pady=3, padx=5)        
        btn_archive.grid(row=4, column=1, pady=3, padx=5)
        btn_settings.grid(row=5, column=1, pady=3, padx=5)
        
        
        # --- COLUMN 2 (RIGHT) ---
        btn_report.grid(row=0, column=2, pady=3, padx=5)
        btn_bulk.grid(row=1, column=2, pady=3, padx=5)
        btn_backup.grid(row=2, column=2, pady=3, padx=5)
        btn_manage_users.grid(row=3, column=2, pady=3, padx=5)
        btn_assign_teacher.grid(row=4, column=2, pady=3, padx=5)
        btn_teacher_portal.grid(row=5, column=2, pady=3, padx=5)
        btn_term.grid(row=6, column=2, pady=3, padx=5)

        # BOTTOM: EXIT
        btn_exit.grid(row=7, column=0, columnspan=3, pady=15, padx=5)



    elif role == "accountant":
        # Hide everything except fees
        btn_register.grid_remove()
        btn_attendance.grid_remove()
        btn_grades.grid_remove()
        btn_teachers.grid_remove()
        btn_assign_teacher.grid_remove()
        btn_view_students.grid_remove()
        btn_search.grid_remove()
        btn_attendance_view.grid_remove()
        btn_teachers_view.grid_remove()
        btn_archive.grid_remove()
        btn_report.grid_remove()
        btn_bulk.grid_remove()
        btn_settings.grid_remove()
        btn_backup.grid_remove()
        btn_term.grid_remove()
        btn_manage_users.grid_remove()

        # Only show fees, view fees, exit
        btn_fees.grid(row=1, column=0, pady=4, padx=10)
        btn_fees_view.grid(row=2, column=0, pady=4, padx=10)
        btn_exit.grid(row=3, column=0, pady=10, padx=10)

    elif role == "teacher":
        # Hide everything except the teacher portal
        btn_register.grid_remove()
        btn_attendance.grid_remove()
        btn_grades.grid_remove()
        btn_fees.grid_remove()
        btn_teachers.grid_remove()
        btn_assign_teacher.grid_remove()
        btn_view_students.grid_remove()
        btn_search.grid_remove()
        btn_attendance_view.grid_remove()
        btn_fees_view.grid_remove()
        btn_teachers_view.grid_remove()
        btn_archive.grid_remove()
        btn_report.grid_remove()
        btn_bulk.grid_remove()
        btn_settings.grid_remove()
        btn_backup.grid_remove()
        btn_term.grid_remove()
        btn_manage_users.grid_remove()
        
        # Only show the teacher portal button, exit
        btn_teacher_portal.grid(row=1, column=0, pady=4, padx=10)
        btn_exit.grid(row=2, column=0, pady=4, padx=10)
            

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
            Paragraph("GRADE", table_header_style),
        ]]

        for grade in grade_rows:
            total = int(grade[4]) + int(grade[5])
            letter = get_grade(total)
            table_data.append([
                Paragraph(str(grade[3]), table_subject_style),   # subject
                Paragraph(str(grade[4]), table_cell_style),       # class_score
                Paragraph(str(grade[5]), table_cell_style),       # exam_score
                Paragraph(str(total), table_cell_style),  # total
                Paragraph(letter, table_cell_style),
            ])

        perf_table = Table(table_data, colWidths=[2.0*inch, 1.3*inch, 1.3*inch, 1.2*inch, 0.9*inch], repeatRows=1)
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
                Paragraph("GRADE", table_header_style),
            ]]

            for grade in grade_rows:
                total = int(grade[4]) + int(grade[5])
                letter = get_grade(total)
                table_data.append([
                    Paragraph(str(grade[3]), table_subject_style),   
                    Paragraph(str(grade[4]), table_cell_style),       
                    Paragraph(str(grade[5]), table_cell_style),       
                    Paragraph(str(total), table_cell_style),
                    Paragraph(letter, table_cell_style),  
                ])

            perf_table = Table(table_data, colWidths=[2.0*inch, 1.3*inch, 1.3*inch, 1.2*inch, 0.9*inch], repeatRows=1)
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
    settings_window.geometry("450x650")
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

    # Multi-line Subjects Box (Press Enter for new line)
    tk.Label(settings_window, text="Subjects (one per line):", bg="darkblue", fg="white").pack(pady=(5, 0))
    subjects_box = tk.Text(settings_window, width=35, height=5)

    # Load subjects and make sure they display line-by-line 
    raw_subjects = get_setting('subjects')
    formatted_subjects = raw_subjects.replace(',', '\n')
    subjects_box.insert("1.0", formatted_subjects)
    subjects_box.pack(pady=3)

    def save_settings():
        # save reguler fields
        for key, entry in fields.items():
            cursor.execute("UPDATE settings SET value = ? WHERE key = ?",
                           (entry.get(), key))

        # Read lines from text box, strip whitespace, remove empty lines
        subjects_text = subjects_box.get("1.0", "end-1c").strip()
        subjects_list = [line.strip() for line in subjects_text.splitlines() if line.strip()]
        clean_subjects = "\n".join(subjects_list)

        # Save clean subjects back to settings
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ('subjects', clean_subjects))

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

def open_term_report():
    term_window = tk.Toplevel(window)
    term_window.title("Term Reports")
    term_window.geometry("500x300")
    term_window.configure(bg="darkblue")

    tk.Label(term_window, text="TERM REPORT", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    top_frame = tk.Frame(term_window, bg="darkblue")
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Class:", bg="darkblue", fg="white").pack(side="left", padx=5)
    cursor.execute("SELECT DISTINCT class_name FROM students WHERE  status='Active'")
    classes = [row[0] for row in cursor.fetchall()]
    class_var = tk.StringVar()
    class_dropdown = tk.OptionMenu(top_frame, class_var, *classes)
    class_dropdown.pack(side="left", padx=5)

    tk.Label(top_frame, text="Term:", bg="darkblue", fg="white").pack(side="left", padx=5)
    term_var = tk.StringVar()
    term_dropdown = tk.OptionMenu(top_frame, term_var, "1", "2", "3")
    term_dropdown.pack(side="left", padx=5)

    tk.Label(top_frame, text="Year:", bg="darkblue", fg="white").pack(side="left", padx=5)
    year_entry = tk.Entry(top_frame, width=6)
    year_entry.insert(0, str(date.today().year))
    year_entry.pack(side="left", padx=5)

    def generate_term_report():
        selected_class = class_var.get()
        term = term_var.get()
        year = year_entry.get()

        if not selected_class or not term:
            messagebox.showinfo("Error", "Please select class and term!")
            return

        cursor.execute("SELECT name FROM students WHERE class_name=? AND status='Active'",
                       (selected_class,))
        students = cursor.fetchall()

        if len(students) == 0:
            messagebox.showinfo("Error", "No students found in this class!")          
            return

        students_totals =[]
        for student in students:
            cursor.execute(
                "SELECT class_score, exam_score FROM grades WHERE student_name=? AND term=?",
                (student[0], term))
            grade_rows = cursor.fetchall()
            if grade_rows:
                total = sum(int(g[0]) + int(g[1]) for g in grade_rows)
                students_totals.append((student[0], total))

        if len(students_totals) == 0:
            messagebox.showinfo("Error" "No grade found for this class and term!")
            return

        students_totals.sort(key=lambda x: x[1], reverse=True)

        suffix = str(int(time.time()))
        filename = os.path.join(os.path.expanduser("~"), "Desktop", 
            f"TermReport_class{selected_class}_Term{term}_{year}.pdf")

        doc = SimpleDocTemplate(filename, pagesize=A4,
            leftMargin=0.75*inch, rightMargin=0.75*inch,
            topMargin=0.75*inch, bottomMargin=0.75*inch) 

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("TRTitle"+suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=16, alignment=TA_CENTER, spaceAfter=6) 
        subtitle_style = ParagraphStyle("TRSub"+suffix, parent=styles["Normal"],
            fontName="Helvetica", fontSize=11, alignment=TA_CENTER, spaceAfter=10)
        header_style = ParagraphStyle("TRHeader"+suffix, parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=10, alignment=TA_CENTER, textColor=colors.white)
        cell_style = ParagraphStyle("TRCell"+suffix, parent=styles["Normal"],
            fontName="Helvetica", fontSize=10, alignment=TA_CENTER)
        cell_left_style = ParagraphStyle("TRCellL"+suffix, parent=styles["Normal"],
            fontName="HElvetica", fontSize=10, alignment=TA_LEFT)
        
        story = []
        story.append(Paragraph("Generated by SchoolPro Ghana",
            ParagraphStyle("TRWater"+suffix, parent=styles["Normal"],
            fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
            textColor=colors.gray, spaceAfter=10)))
        story.append(Paragraph(get_setting('school_name'), title_style))
        story.append(Paragraph(f"CLASS {selected_class} - TERM {term} - {year}", subtitle_style))
        story.append(Paragraph("ACADEMIC PERFORMANCE SUMMARY", subtitle_style))
        story.append(Spacer(1, 0.2*inch))

        table_data = [[
            Paragraph("POSITION", header_style),
            Paragraph("STUDENT NAME", header_style),
            Paragraph("TOTAL SCORE", header_style),
            Paragraph("GRADE", header_style),
        ]]

        total_scores = []
        for i, (name, total) in enumerate(students_totals):
            position = str(i + 1)
            grade = get_grade(total)
            total_scores.append(total)
            table_data.append([
                Paragraph(position, cell_style),
                Paragraph(name, cell_left_style),
                Paragraph(str(total), cell_style),
                Paragraph(grade, cell_style),
            ])

        perf_table = Table(table_data, colWidths=[1*inch, 3*inch, 1.5*inch, 1*inch])
        perf_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1F3864")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.gray),
            ("BOX", (0,0), (-1,-1), 1, colors.black),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F2F2")]),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))    
        story.append(perf_table)
        story.append(Spacer(1, 0.3*inch))

        class_average = sum(total_scores) / len(total_scores)
        highest = max(total_scores)
        lowest = min(total_scores)

        summary_data = [
            [Paragraph("Class Average:", header_style), Paragraph(f"{class_average:.1f}", cell_style)],
            [Paragraph("Highest Score:", header_style), Paragraph(str(highest), cell_style)],
            [Paragraph("Lowest Score:", header_style), Paragraph(str(lowest), cell_style)],
            [Paragraph("Total Students:", header_style), Paragraph(str(len(students_totals)), cell_style)],
        ]
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#1f3864")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.gray),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*inch))

        sig_data = [
            ["_______________________", "_______________________"],
            ["Class Teacher's Signature", "Headmaster's Signature"]
        ]
        sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
        sig_table.setStyle(TableStyle([
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTNAME", (0,1), (-1,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 10),
        ]))
        story.append(sig_table)

        doc.build(story)
        messagebox.showinfo("Success", f"Term report saved to Desktop!")
        term_window.destroy()

    tk.Button(term_window, text="Generate Term Report", bg="green", fg="white", font=("Arial", 12), command=generate_term_report).pack(pady=20)
def open_teacher_portal():
    assignments = get_teacher_info(current_user_name)

    if not assignments:
        messagebox.showinfo("Error", f"No assigments found for '{current_user_name}'.\n" "Please ask admin to assign a class/subject in Manage Teachers.")
        return

    if len(assignments) == 1:
        launch_teacher_dashboard(assignments[0])
    else:
        choose_assignment(assignments)

def choose_assignment(assignments):
    choose_window = tk.Toplevel(window)
    choose_window.title("Select Class/Subject")
    choose_window.geometry("400x300")
    choose_window.configure(bg="darkblue")

    tk.Label(choose_window, text="SELECT CLASS/SUBJECT", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(choose_window, text=f"{current_user_name}, yuo teach multiple classes.\nPick one to continue:", bg="darkblue", fg="yellow", font=("Arial", 11)).pack(pady=10)

    for assignment in assignments:
        label = f"{assignment['subject']} - {assignment['class_name']}"
        tk.Button(choose_window, text=label, font=("Arial", 12), bg="green", fg="white", width=30, command=lambda a=assignment: [choose_window.destroy(), launch_teacher_dashboard(a)]).pack(pady=8)

def launch_teacher_dashboard(assignment):
    portal_window = tk.Toplevel(window)
    portal_window.title("Teacher Portal")
    portal_window.geometry("450x400")
    portal_window.configure(bg="darkblue")

    tk.Label(portal_window, text="TEACHER PORTAL", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    tk.Label(portal_window, text=f"Welcome, {current_user_name}", font=("Arial", 12), bg="darkblue", fg="white").pack(pady=5)

    tk.Label(portal_window, text=f"Class: {assignment['class_name']}  |   Subject: {assignment['subject']}", font=("Arial", 11), bg="darkblue", fg="yellow").pack(pady=5)

    tk.Button(portal_window, text="Mark Attendance", font=("Arial", 12), bg="green", fg="white", width=25, command=lambda: open_teacher_attendance(assignment)).pack(pady=15)

    tk.Button(portal_window, text="Enter Grades", font=("Arial", 12), bg="green", fg="white", width=25, command=lambda: open_teacher_grades(assignment)).pack(pady=15)

    tk.Button(portal_window, text="Close", font=("Arial", 12), bg="red", fg="white", width=25, command=portal_window.destroy).pack(pady=15)

def open_teacher_attendance(assignment):
    att_window = tk.Toplevel(window)
    att_window.title("Mark Attendance")
    att_window.geometry("500x600")
    att_window.configure(bg="darkblue")

    tk.Label(att_window, text=f"ATTENDANCE - {assignment['class_name']}", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

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
    canvas.create_window((0, 0), window=students_frame, anchor="nw")
    students_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    def load_students():
        for widget in students_frame.winfo_children():
            widget.destroy()
        student_entries.clear()

        cursor.execute(
            "SELECT name FROM students WHERE class_name=? AND status='Active'",
            (assignment['class_name'],))
        students = cursor.fetchall()

        if len(students) == 0:
            messagebox.showinfo("Error", "No active students found in this class!")
            return

        for student in students:
            row = tk.Frame(students_frame, bg="darkblue")
            row.pack(pady=3, fill="x", padx=10)
            tk.Label(row, text=student[0], width=20, bg="darkblue", fg="white", anchor="w").pack(side="left")

            status_var = tk.StringVar(value="Present")
            btn = tk.Button(row, text="Present", bg="green", fg="white", width=10)

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

    load_students()

    def save_attendance():
        if len(student_entries) == 0:
            messagebox.showinfo("Error", "No students loaded!")
            return
        today = date_entry.get()
        for student_name, status_var in student_entries:
            cursor.execute(
                "INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)", 
                (student_name, today, status_var.get()))
        conn.commit()
        messagebox.showinfo("Success", "Attendance saved for all students!")
        att_window.destroy()

    tk.Button(att_window, text="Save Attendance", bg="green", fg="white", font=("Arial", 12), command=save_attendance).pack(pady=15)

def open_teacher_grades(assignment):
    grades_window = tk.Toplevel(window)
    grades_window.title("Enter Grades")
    grades_window.geometry("550x600")
    grades_window.configure(bg="darkblue")

    tk.Label(grades_window, text=f"GRADES - {assignment['class_name']} - {assignment['subject']}", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    top_frame = tk.Frame(grades_window, bg="darkblue")
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Term:", bg="darkblue", fg="white").pack(side="left", padx=5)
    term_var = tk.StringVar()
    term_dropdown = tk.OptionMenu(top_frame, term_var, "1", "2", "3")
    term_dropdown.pack(side="left", padx=5)

    tk.Label(top_frame, text="Year:", bg="darkblue", fg="white").pack(side="left", padx=5)
    year_entry = tk.Entry(top_frame, width=6)
    year_entry.insert(0, str(date.today().year))
    year_entry.pack(side="left", padx=5)

    student_entries = []

    canvas = tk.Canvas(grades_window, bg="darkblue", height=300)
    scrollbar = tk.Scrollbar(grades_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    students_frame = tk.Frame(canvas, bg="darkblue")
    canvas.create_window((0, 0), window=students_frame, anchor="nw")
    students_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    def load_students():
        for widget in students_frame.winfo_children():
            widget.destroy()
        student_entries.clear()

        header = tk.Frame(students_frame, bg="darkblue")
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="Student", width=20, bg="darkblue", fg="yellow", anchor="w").pack(side="left")
        tk.Label(header, text="Class Score", width=10, bg="darkblue", fg="yellow").pack(side="left")
        tk.Label(header, text="Exam Score", width=10, bg="darkblue", fg="yellow").pack(side="left")


        cursor.execute(
            "SELECT id, name FROM students WHERE class_name=? AND status='Active'",
            (assignment['class_name'],))
        students = cursor.fetchall()

        if len(students) == 0:
            messagebox.showinfo("Error", "No active students found in this class!")
            return

        for student_id, student_name in students:
            row = tk.Frame(students_frame, bg="darkblue")
            row.pack(pady=3, fill="x", padx=10)
            tk.Label(row, text=student_name, width=20, bg="darkblue", fg="white", anchor="w").pack(side="left")

            class_entry = tk.Entry(row, width=10)
            class_entry.pack(side="left", padx=5)
            exam_entry = tk.Entry(row, width=10)
            exam_entry.pack(side="left", padx=5)

            student_entries.append((student_id, student_name, class_entry, exam_entry))

    load_students()

    def save_grades():
        term = term_var.get()
        year = year_entry.get()

        if not term:
            messagebox.showinfo("Error", "Please select a term!")
            return
        if len(student_entries) == 0:
            messagebox.showinfo("Error", "No students loaded!")
            return

        saved_count = 0
        for student_id, student_name, class_entry, exam_entry in student_entries:
            class_score = class_entry.get().strip()
            exam_score = exam_entry.get().strip()

            if class_score == "" and exam_score == "":
                continue

            try:
                class_score = int(class_score) if class_score else 0
                exam_score = int(exam_score) if exam_score else 0
            except ValueError:
                messagebox.showinfo("Error", f"Invalid score for {student_name}. Use numbers only.")
                return

            total = class_score + exam_score
            grade = get_grade(total)

            cursor.execute("""
                INSERT INTO grades (student_id, student_name, subject, class_score, exam_score, grade, term, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, student_name, assignment['subject'], class_score, exam_score, grade, term, year)) 
            saved_count += 1

        conn.commit()
        messagebox.showinfo("Success", f"Grades saved for {saved_count} student(s)!")
        grades_window.destroy()

    tk.Button(grades_window, text="Save Grades", bg="green", fg="white", font=("Arial", 12), command=save_grades).pack(pady=15)                   
                   
def open_manage_users():
    users_window = tk.Toplevel(window)
    users_window.title("Manage Users")
    users_window.geometry("620x530")
    users_window.configure(bg="darkblue")

    tk.Label(users_window, text="MANAGE USERS", font=("Arial", 16, "bold"), bg="darkblue", fg="white").pack(pady=10)

    # View existing users
    text_box = tk.Text(users_window, width=68, height=8, wrap="none")
    text_box.pack(pady=5)

    cursor.execute("SELECT username, role, full_name FROM users")
    users = cursor.fetchall()
    for user in users:
        text_box.insert(tk.END, f"Username: {user[0]} | Role: {user[1]} | Name: {user[2]}\n")

    # Disable editing so users can't type inside the box
    text_box.configure(state="disabled")    

    tk.Label(users_window, text="--- A New User ---", bg="darkblue", fg="white").pack(pady=5)

    tk.Label(users_window, text="Full Name:", bg="darkblue", fg="white").pack()
    fullname_entry = tk.Entry(users_window, width=30)
    fullname_entry.pack(pady=3)

    tk.Label(users_window, text="Usersname:", bg="darkblue", fg="white").pack()
    username_entry = tk.Entry(users_window, width=30)
    username_entry.pack(pady=3)

    tk.Label(users_window, text="Password:", bg="darkblue", fg="white").pack()
    password_entry = tk.Entry(users_window, width=30, show="*")
    password_entry.pack(pady=3)

    tk.Label(users_window, text="Role:", bg="darkblue", fg="white").pack()
    role_var = tk.StringVar(value="accountant")
    role_dropdown = tk.OptionMenu(users_window, role_var, "admin", "accountant", "teacher")
    role_dropdown.pack(pady=3)

    def add_user():
        full_name = fullname_entry.get()            
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not full_name or not username or not password:
            messagebox.showinfo("Error", "Please fill all fields!")
            return
        try:
            cursor.execute(
                "INSERT INTO users(username, password, role, full_name) VALUES (?, ?, ?, ?)",
                (username, password, role, full_name))
            conn.commit()
            messagebox.showinfo("Success", "User added successfuly")
            users_window.destroy()
            open_manage_users()
        except:
            messagebox.showerror("Error", "Username already exists!")

    tk.Button(users_window, text="Add User", bg="green", fg="white", font=("Arial", 12), command=add_user).pack(pady=10)                
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

# -----------------------------------------
# BUTTON DEFINITIONS & COMMAND
# -----------------------------------------
# DAILY OPERATIONS
btn_register = tk.Button(button_frame, text="Student Registration", font=("Arial", 12), width=25, bg="green", fg="white", command=open_registration)
btn_attendance = tk.Button(button_frame, text="Attendance", font=("Arial", 12), width=25, bg="green", fg="white", command=open_attendance)
btn_grades = tk.Button(button_frame, text="Grades & Results", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_grades)
btn_fees = tk.Button(button_frame, text="Fee Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_fees)
btn_teachers = tk.Button(button_frame, text="Teacher Management", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_teachers)
btn_view_students = tk.Button(button_frame, text="View All Students", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_students)

# ACCOUNTANT / FESS
btn_search = tk.Button(button_frame, text="Search Student", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_search)
btn_attendance_view = tk.Button(button_frame, text="View Attendance", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_attendance)
btn_fees_view = tk.Button(button_frame, text="View Fees", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_fees)
btn_teachers_view = tk.Button(button_frame, text="View Teachers", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_view_teachers)
btn_archive = tk.Button(button_frame, text="Update Student Status", font=("Arial, 12"), width=25, bg="green", fg="white", command=open_update_status)
btn_settings = tk.Button(button_frame, text="Settings", font=("Arial, 12"), width=25, bg="gray", fg="white", command=open_settings)

# ADMIN & MANAGEMENT
btn_report = tk.Button(button_frame, text="Print Report Card", font=("Arial", 12), width=25, bg="purple", fg="white", command=open_report_card)
btn_bulk = tk.Button(button_frame, text="Bulk Print Report Cards", font=("Arial", 12), width=25, bg="purple", fg="white", command=open_bulk_report_card)
btn_backup = tk.Button(button_frame, text="Backup Database", font=("Arial", 12), width=25, bg="teal", fg="white", command=backup_database)
btn_manage_users = tk.Button(button_frame, text="Manage Users", font=("Arial", 12), width=25, bg="navy", fg="white", command=open_manage_users)
btn_assign_teacher = tk.Button(button_frame, text="Assign Class/Subject", font=("Arial", 12), width=25, bg="darkblue", fg="white", command=open_assign_teacher)
btn_teacher_portal = tk.Button(button_frame, text="Teacher Portal", font=("Arial", 12), bg="darkblue", fg="white", command=open_teacher_portal)
btn_term = tk.Button(button_frame, text="Term Reports", font=("Arial", 12), width=25, bg="brown", fg="white", command=open_term_report)

# EIXT
btn_exit = tk.Button(button_frame, text="Exit", font=("Arial, 12"), width=25, bg="red", fg="white", command=window.quit)

# ==========================================
# COLUMN 0: DAILY OPERATIONS
# ==========================================
btn_register.grid(row=0, column=0, pady=3, padx=5)
btn_attendance.grid(row=1, column=0, pady=3, padx=5)
btn_grades.grid(row=2, column=0, pady=3, padx=5)
btn_fees.grid(row=3, column=0, pady=3, padx=5)
btn_teachers.grid(row=4, column=0, pady=3, padx=5)
btn_view_students.grid(row=5, column=0, pady=3, padx=5)

# ==========================================
# COLUMN 1: ACCOUNTANT / FINANCE
# ==========================================
btn_search.grid(row=0, column=1, pady=3, padx=5)
btn_attendance_view.grid(row=1, column=1, pady=3, padx=5)
btn_fees_view.grid(row=2, column=1, pady=3, padx=5)
btn_teachers_view.grid(row=3, column=1, pady=3, padx=5)        
btn_archive.grid(row=4, column=1, pady=3, padx=5)
btn_settings.grid(row=5, column=1, pady=3, padx=5)
        
# ==========================================
# COLUMN 2: ADMIN & MANAGEMENT
# ==========================================
btn_report.grid(row=0, column=2, pady=3, padx=5)
btn_bulk.grid(row=1, column=2, pady=3, padx=5)
btn_backup.grid(row=2, column=2, pady=3, padx=5)
btn_manage_users.grid(row=3, column=2, pady=3, padx=5)
btn_assign_teacher.grid(row=4, column=2, pady=3, padx=5)
btn_teacher_portal.grid(row=5, column=2, pady=3, padx=5)
btn_term.grid(row=6, column=2, pady=3, padx=5)

# ===========================================
# EXIT BUTTON (Centered across all 3 columns)
# ===========================================
btn_exit.grid(row=7, column=0, columnspan=3, pady=3, padx=5)

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