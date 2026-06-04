# SchoolPro Ghana 
# School Management Software 
# Developer: Issahak Abdul Halim(Hafiz)
# Version: 1.0

while True:
    print("===================================")
    print("Welcome to SchoolPro Ghana!")
    print("School Management Software")
    print("===================================")
    print("1. Student Registration")
    print("2. Attendance")
    print("3. Grades & Results")
    print("4. Fee Management")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")
    if choice =="1":
        print("================================")
        print("     Student REGISTRATION")
        print("================================")
        name = input("Enter student name: ")
        age = input("Enter student age: ")
        class_name = input("Enter class: ")
        section = input("Enter section (Academic/Islamic): ")
        print("================================")
        print("Student Registered Successfully!")
        print("Name: " + name)
        print("Age: " + age)
        print("Class: " + class_name)
        print("section: " + section)
        print("================================")
    elif choice == "2":
        print("Opening Attendance...")
    elif choice == "3":
        print("Opening Grades & Results...")
    elif choice == "4":
        print("Opening Fee Management...")
    elif choice == "5":
        print("Goodbye! Thank you for using ShcoolPro Ghana!")
        break
    else:
        print("invalid choise! Please enter 1-5")
                       