import sqlite3

# Connect to database
conn = sqlite3.connect("/home/hafiz/my-first-project/schoolpro.db")
cursor = conn.cursor()

# Student table
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
        date_registered TEXT,
        status TEXT DEFAULT 'Active'       
    )
""")

# Create student archive table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        name TEXT,        
        age TEXT,
        gender TEXT,
        class_name TEXT,
        section TEXT,
        parent_name TEXT,
        parent_phone TEXT,
        date_registerd TEXT,
        status TEXT,
        archive_date TEXT,
        reason TEXT
    )
""")                          

# Attendace table
cursor.execute("""
    CREATE TABLE IF NOT EXIsTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        student_name TEXT,
        date TEXT,
        status TEXT
    )
""")

# Grades table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        student_name TEXT,
        subject TEXT,
        class_score TEXT,
        exam_score TEXT,       
        grade TEXT,
        term TEXT,
        year TEXT
    )
""")       

# Fees table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        student_name TEXT,
        amount TEXT,
        date TEXT,
        term TEXT,
        status TEXT
    )
""")

# Teachers table                 
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )           
''')

# Default values
defaults = [
    ('school_name', 'SCHOOL NAME'),
    ('school_address', ''),
    ('logo_path', ''),
    ('currency', 'GHS'),
    ('house_name', 'Red,Blue,Green,Yellow'),
    ('grade_A', '80'),
    ('grade_B', '70'),
    ('grade_C', '60'),
    ('grade_D', '50'),
    ('password', 'schoolpro123'),
    ('theme', 'dark'),
]                     
for key, val in defaults:
    cursor.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",(key, val))


conn.commit()
print("Schoolpro Ghana Database Created Successfully!")
print("Tables: students, student_archive, attendace, grades, fees, teachers")                                              