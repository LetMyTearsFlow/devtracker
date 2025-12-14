from unittest import TestCase
from src.storage import Storage
from pathlib import Path


class Test(TestCase):
    def SetUp(self):
        self.storage = Storage(Path(__file__).parent / 'fixture')
    def test_load_data(self):
        # correct_data_path = r'C:\dev\01_workspace\devtracker\test\fixture\correct_data.json'
        correct_data_path = Path(__file__).parent / 'fixture' / 'correct_data.json'
        storage = Storage(correct_data_path)
        projects = storage.projects
        sessions = storage.sessions
        self.assertIsNotNone(projects)
        self.assertIsNotNone(sessions)
        self.assertIn('my-blog', projects)
        expected_projects = {
            "my-blog": "/Users/student/code/my-blog",
            "cli-demo": "/Users/student/code/cli-demo"
        }
        self.assertEqual(projects, expected_projects)
        expected_sessions = [{
            "project": "my-blog",
            "start_time": "2023-10-27T10:00:00",
            "duration_seconds": 3600,
            "note": "实现了文章列表页的React组件"
        }]
        self.assertEqual(expected_sessions, sessions)

    def test_save_data(self):
        save_data_path = Path(__file__).parent / 'fixture' / 'save_data.json'
        projects = {"cli-demo": "/Users/student/code/cli-demo"}
        sessions = [{"project": "cli-demo", "start_time": "2023-10-27T10:00:00", "duration_seconds": 3600, "note": ""}]
