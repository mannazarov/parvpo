import requests

url = 'http://localhost:5000/api/tasks'
headers = {'Content-Type': 'application/json'}

for i in range(1, 101):
    task = {
        'title': f'Task {i}',
        'description': f'Description for task {i}'
    }
    response = requests.post(url, json=task, headers=headers)
    if response.status_code == 201:
        print(f'Successfully added task {i}')
    else:
        print(f'Failed to add task {i}: {response.text}')