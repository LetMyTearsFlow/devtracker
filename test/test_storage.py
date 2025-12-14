from unittest import TestCase
from src.storage import load_data
from pathlib import Path


class Test(TestCase):
    def test_load_data(self):
        # correct_data_path = r'C:\dev\01_workspace\devtracker\test\fixture\correct_data.json'
        correct_data_path = Path(__file__).parent / 'fixture' / 'correct_data.json'
        projects, sessions = load_data(correct_data_path)
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
