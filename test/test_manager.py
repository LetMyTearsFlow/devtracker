from pathlib import Path
from unittest import TestCase
from src.manager import Manager

class TestManager(TestCase):
    def test_scan_directory(self):
        manager = Manager()
        root = (Path(__file__).parent / 'fixture' / 'test_scan_directory')
        result = manager.scan_directory(root)
        expected_result = [Path(__file__).parent / 'fixture' / 'test_scan_directory' / 'folder2',
                           Path(__file__).parent / 'fixture' / 'test_scan_directory' / 'folder2' / 'folder22',
                           Path(__file__).parent / 'fixture' / 'test_scan_directory' / 'folder3']
        self.assertEqual(result, expected_result)
