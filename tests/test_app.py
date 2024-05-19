import unittest
from app import create_app, init_db
from app.models import add_task, get_task, delete_task

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        init_db()

    def test_add_task(self):
        response = self.client.post('/api/tasks', json={'title': 'Test Task', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Test Task')

    def test_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_task(self):
        task_id = add_task('Task to get', 'Description')
        response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Task to get')

    def test_delete_task(self):
        task_id = add_task('Task to delete', 'Description')
        response = self.client.post(f'/api/tasks/{task_id}', data={'_method': 'DELETE'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Task deleted successfully')
        self.assertIsNone(get_task(task_id))

if __name__ == '__main__':
    unittest.main()
