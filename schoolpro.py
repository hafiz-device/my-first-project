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
    if choice == "1":
        print("Opening Student Registration...")
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
                       