import unittest
from app.models import add_task, get_tasks, get_task, delete_task, get_db

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = get_db()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_add_task(self):
        task_id = add_task('Test Task', 'Test Description')
        self.assertIsNotNone(task_id)

    def test_get_tasks(self):
        add_task('Test Task 1', 'Description 1')
        add_task('Test Task 2', 'Description 2')
        tasks = get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task(self):
        task_id = add_task('Task to get', 'Description')
        task = get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task['title'], 'Task to get')

    def test_delete_task(self):
        task_id = add_task('Task to delete', 'Description')
        delete_task(task_id)
        task = get_task(task_id)
        self.assertIsNone(task)

if __name__ == '__main__':
    unittest.main()
