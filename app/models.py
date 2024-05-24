import json
from datetime import datetime
import sqlite3

from flask import current_app

DATABASE = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def add_task(title, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)',
                   (title, description, datetime.utcnow().isoformat()))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    #current_app.redis.delete('tasks')
    return task_id

def get_tasks():
    tasks = current_app.redis.get('tasks')
    if tasks is None:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        conn.close()
        tasks_json = json.dumps([dict(task) for task in tasks])
        #current_app.redis.set('tasks', tasks_json, ex=1000)  # Кешируем на 600 секунд
    else:
        tasks = json.loads(tasks)
    return tasks

def get_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    #current_app.redis.delete('tasks')


def populate_tasks(n=10000):
    conn = get_db()
    cursor = conn.cursor()
    for i in range(n):
        title = f"Task {i}"
        description = f"Description for task {i}"
        created_at = datetime.utcnow().isoformat()
        cursor.execute('INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)',
                       (title, description, created_at))
    conn.commit()
    conn.close()

