import sqlite3

conn = sqlite3.connect('schoolpro.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS students ( 
     id INTEGER PRIMARY KEY,
     name TEXT,
     age TEXT,
     class_name TEXT,
     section TEXT
)''')

conn.commit()
conn.close()
print("Database created successfully")                                                                                