# Schoolpro Ghana
# School Management Software
# Developer: Issahak Abdul Halim (Hafiz)
# Version: 1.0

import sqlite3
from datetime import date

# Connect to database 
conn = sqlite3.connect("schoolpro.db")
cursor = conn.cursor()

# Creat tables 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age TEXT,
        gender TEXT,
        class_name TEXT,
        section TEXT,
        parent_name TEXT,
        parent_phone TEXT,
        date_registered TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        gender TEXT,
        class_name TEXT,
        section TEXT,
        parent_name TEXT,
        parent_phone TEXT,
        date_registered TEXT,
        status TEXT DEFAULT 'Active'
    )
""")                          

cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        date TEXT,
        status TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS  grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        subject TEXT,
        score TEXT,
        grade TEXT,
        term TEXT,
        year TEXT 
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT, 
        amount TEXT, 
        date TEXT, 
        term TEXT,
        status TEXT 
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT,
        class_name TEXT,
        phone TEXT,
        section TEXT
    )
""")

conn.commit()

while True:
    print("========================================")
    print("Welcome to SchoolPro Ghana!")
    print(" School Management Software")
    print("========================================")
    print("1. Student Registration")
    print("2. Attendance")
    print("3. Grades & Results")
    print("4. Fee Management")
    print("5. Teacher/Staff Management")
    print("6. View All Students")
    print("7. Search Student")
    print("8. View Attendance")
    print("9. View Fees")
    print("10. View Teachers")
    print("11. UPdate Student Status")
    print("12. Exit")
    print("========================================")

    choice = input("Enter your choice from (1-12): ")

    if choice == "1":
        print("========================================")
        print("     STUDENT REGISTRATION")
        print("========================================")
        name = input("Enter student name: ")
        age = input("Enter student age: ")
        gender = input("Enter gender (Male/Female): ")
        class_name = input("Enter class: ")
        section = input("Enter section (Academic/Islamic): ")
        parent_name = input("Enter parent name: ")
        parent_phone = input("Enter parent phone: ")
        today = str(date.today())
        cursor.execute(
            "INSERT INTO students (name, age, gender, class_name, section, parent_name, parent_phone, date_registered) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, gender, class_name, section, parent_name, parent_phone, today)
        )
        conn.commit()
        print("=========================================")
        print("Student Registerd Successfully!")
        print("=========================================")

    elif choice == "2":
        print("=========================================")
        print("           ATTENDANCE")
        print("=========================================")
        student_name = input("Enter student name: ")
        status = input("Enter status (Present/Absent): ")
        today = str(date.today())
        cursor.execute(
            "INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)",
            (student_name, today, status)
        )
        conn.commit()
        print("==========================================")
        print("Attendance Recorded Successfully!")
        print("==========================================")

    elif choice == "3":
        print("==========================================")
        print("       GRADES & RESULTS")
        print("==========================================")
        student_name = input("Enter student name: ")
        subject = input("Enter subject: ")
        score = input("Enter score: ")
        grade = input("Enter grade(A/B/C/D/F): ")
        term = input("Enter term (1/2/3): ")
        year = input("Enter year: ")
        cursor.execute(
            "INSERT INTO grades (student_name, subject, score, grade, term, year) VALUES (?, ?, ?, ?, ?, ?)",
            (student_name, subject, score, grade, term, year)
        )
        conn.commit()
        print("==========================================")
        print("Grades Recorded Successfully!")
        print("==========================================")
        
    elif choice == "4":
        print("==========================================")
        print("       FEE MANAGEMENT")
        print("==========================================")
        student_name = input("Enter student name: ")
        amount = input("Enter amountpaid (GHS): ")
        term = input("Enter term (1/2/3): ")
        status = input("Enter status (Paid/Partial/Unpaid): ")
        today = str(date.today())
        cursor.execute(
            "INSERT INTO fees (student_name, amount, date, term, status) VALUES (?, ?, ?, ?, ?)",
            (student_name, amount, today, term, status)
        ) 
        conn.commit()
        print("==========================================")
        print("Fee Recorded Successwfully!")
        print("==========================================")

    elif choice == "5":
        print("==========================================")
        print("   TEACHER/STAFF MANAGEMENT")
        print("==========================================")
        name = input("Enter teacher name: ")
        subject = input("Enter subject: ")
        class_name = input("Enter class: ")
        phone = input("Enter phone number: ")
        section = input("Enter section (Academic/Islamic): ")
        cursor.execute(
            "INSERT INTO teachers (name, subject, class_name, phone, section) VALUES (?, ?, ?, ?, ?)",
            (name, subject, class_name, phone, section)
        ) 
        conn.commit()
        print("==========================================")
        print("Teacher Registered Succesfully!")
        print("==========================================")

    elif choice == "6":
        print("==========================================")
        print("       ALL STUDENTS")
        print("==========================================")
        cursor.execute("SELECT * FROM  students")
        students = cursor.fetchall()
        if len(students) == 0:
            print("No students registerd yet!")
        else:
            for student in students:
                print("ID: " + str(student[0]))
                print("Name: " + student[1])
                print("Age: " + student[2])
                print("Gender: " + student[3])
                print("Class: " + student[4])
                print("Section: " + student[5])
                print("parent: " + student[6])
                print("phone: " + student[7])
                print("Date: " + student[8])
                print("----------------")
        print("============================================")

    elif choice == "7":
        print("============================================")
        print("       SEARCH STUDENT")
        print("============================================")
        search_name = input("Enter student name to search: ")
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_name + '%',))
        results = cursor.fetchall()
        if len(results) == 0:
            print("No student found with that name!")
        else:
            for student in results:
                print("ID: " + str(student[0]))
                print("Name: " + student[1])
                print("Age: " + student[2])
                print("Gender: " + student[3])
                print("Class: " + student[4])
                print("Section: " + student[5])
                print("parent: " + student[6])
                print("Phone: " + student[7])
                print("Date: " + student[8])
                print("----------------")
        print("============================================") 

    elif choice == "8":
        print("============================================")
        print("       VIEW ATTENDANCE")
        print("============================================")
        cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()
        if len(records) == 0:
            print("No attendace records yet!")
        else: 
            for record in records:
                print("ID: " + str(record[0]))
                print("Student: " + record[1])
                print("Date: " + record[2])
                print("Status: " + record[3])
                print("----------------")
        print("============================================")  

    elif choice == "9":
        print("============================================")
        print("         VIEW FEES")
        print("============================================")
        cursor.execute("SELECT * FROM fees")
        records = cursor.fetchall()
        if len(records) == 0:
            print("No fee record yet!")
        else:
            for record in records:
                print("ID: " + str(record[0]))
                print("Student: " + record[1])
                print("Amount: " + record[2])
                print("Date: " + record[3])
                print("Term: " + record[4])
                print("Status: " + record[5])
                print("----------------")
        print("=============================================")  

    elif choice == "10":
        print("=============================================")
        print("       VIEW TEACHERS")
        print("=============================================")
        cursor.execute("SELECT * FROM teachers")
        records = cursor.fetchall()
        if len(records) == 0:
            print("No teachers registered yet!")
        else:
            for record in records:
                print("ID: " + str(record[0]))
                print("Name: " + record[1])
                print("Subject: "+ record[2])
                print("Class: " + record[3])
                print("Phone: " + record[4])
                print("Section: " + record[5])
                print("-----------------")
        print("=============================================")   

    elif choice == "11":
        print("=============================================")
        print("     UPDATE STUDENT STATUS")
        print("=============================================")
        search_name = input("Enter student name: ")
        print("Status options:")
        print("1. Active")
        print("2. Graduated")
        print("3. Transferred")
        print("4. Suspended")
        new_status = input("Enter new status: ")
        cursor.execute(
            "UPDATE students SET section = section WHERE name LIKE ?",
            ('%' + search_name + '%',)
        ) 
        cursor.execute(
            "UPDATE students SET status = ? WHERE name LIKE ?",
            (new_status, '%' + search_name + '%')
        ) 
        conn.commit()
        print("==============================================")  
        print("Student Status Updated Successfully!")
        print("==============================================")                                                         

    elif choice == "12":
        print("Goodbye! Thank you for using SchoolPro Ghana!")
        conn.close()
        break
    else:
        print("Invalid choice! Please enter 1-7")
