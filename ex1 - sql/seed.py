import sqlite3
from faker import Faker

fake = Faker()

conn = sqlite3.connect('taskboard.db')
cursor = conn.cursor()


def add_users(n):
    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        cursor.execute('INSERT INTO users (fullname, email) VALUES (?, ?)', (fullname, email))


def add_tasks(n):
    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT id FROM status')
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        title = fake.sentence()
        description = fake.text()
        status_id = fake.random.choice(status_ids)
        user_id = fake.random.choice(user_ids)
        cursor.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)',
                       (title, description, status_id, user_id))


add_users(10)
add_tasks(30)

conn.commit()
conn.close()

print("Дані були успішно додані.")
