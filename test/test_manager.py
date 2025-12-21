from pathlib import Path
from unittest import TestCase
from src.manager import Manager

class TestManager(TestCase):

    def test_scan_directory(self):
        manager = Manager()
        root = (Path(__file__).parent / 'fixture' / 'test_scan_directory')
        manager.scan_directory(root)
        self.assertIn("folder2", manager.storage.projects)
        self.assertIn("folder3", manager.storage.projects)

    def test_check_git_status(self):
        manager = Manager()
        path = Path(__file__).parent / 'fixture' / 'test_scan_directory' / 'folder3'
        manager.check_git_status(path)
