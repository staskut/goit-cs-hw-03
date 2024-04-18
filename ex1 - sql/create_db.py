import sqlite3

conn = sqlite3.connect('taskboard.db')
cursor = conn.cursor()

with open('tables.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Таблиці були успішно створені.")
