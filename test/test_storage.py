import json
from unittest import TestCase
from src.storage import Storage
from pathlib import Path


class Test(TestCase):
    def SetUp(self):
        pass

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
        storage = Storage(save_data_path)
        storage.projects = projects
        storage.sessions = sessions
        storage.save_data()
        # check if the file exist
        with open(save_data_path) as f:
            data = json.load(f)
            expected_data = {
                "projects": {
                    "cli-demo": "/Users/student/code/cli-demo"
                },
                "sessions": [
                    {
                        "project": "cli-demo",
                        "start_time": "2023-10-27T10:00:00",
                        "duration_seconds": 3600,
                        "note": ""
                    }
                ]
            }
            self.assertEqual(expected_data, data)

    def test_add_project(self):
        add_project_path = Path(__file__).parent / 'fixture' / 'add_project.json'
        storage = Storage(add_project_path)
        name = "add-project"
        path = "/Users/student/code/add-project"
        storage.add_project(name, path)
        with open(add_project_path) as f:
            data = json.load(f)
            expected_data = {
                "projects": {
                    "add-project": "/Users/student/code/add-project"
                },
                "sessions": []
            }
            self.assertEqual(expected_data, data)

    def test_add_session(self):
        add_session_path = Path(__file__).parent / 'fixture' / 'add_session.json'
        storage = Storage(add_session_path)
        session = {"project": "cli-demo",
                   "start_time": "2023-10-27T10:00:00",
                   "duration_seconds": 3600,
                   "note": "123456"}
        storage.add_session(session)
        with open(add_session_path) as f:
            data = json.load(f)
            expected_data = {
                "projects": {},
                "sessions": [session]
            }
            self.assertEqual(expected_data, data)
