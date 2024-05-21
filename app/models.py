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
    current_app.redis.delete('tasks')
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
        current_app.redis.set('tasks', tasks_json, ex=60)  # Кешируем на 60 секунд
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
    current_app.redis.delete('tasks')


