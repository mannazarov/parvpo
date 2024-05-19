from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models import add_task, get_tasks, get_task, delete_task
from app.tasks import send_log_message
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        add_task(title, description)
        send_log_message(f'Task added: {title}')
        return redirect(url_for('routes.index'))
    return render_template('add_task.html')

@bp.route('/api/tasks', methods=['POST'])
def api_add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    task_id = add_task(title, description)
    send_log_message(f'Task added via API: {title}')
    return jsonify({'id': task_id, 'title': title, 'description': description, 'created_at': datetime.utcnow().isoformat()}), 201

@bp.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = get_tasks()
    return jsonify([dict(task) for task in tasks])

@bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    task = get_task(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(dict(task))

@bp.route('/api/tasks/<int:task_id>', methods=['POST'])
def api_delete_task(task_id):
    if request.form.get('_method') == 'DELETE':
        if get_task(task_id) is None:
            return jsonify({'error': 'Task not found'}), 404
        delete_task(task_id)
        send_log_message(f'Task deleted via API: {task_id}')
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'error': 'Method not allowed'}), 405
