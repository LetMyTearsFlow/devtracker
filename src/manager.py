import logging
import subprocess
from enum import Enum
from pathlib import Path

from src.storage import Storage

from rich.console import Console
from rich.table import Table

console = Console()


class GitStatus(Enum):
    CLEAN = "clean"
    NOT_CLEAN = "not_clean"


class Manager:

    def scan_directory(self, root: Path) -> list[Path]:
        """
        scans a directory and its subdirectories.
        directory with . beginning are ignored.
        :param root: root directory
        :return: a list of subdirectories
        """
        path_list = []
        self._scan_directory_recursively(root, path_list)
        path_list = [p for p in path_list if (p / '.git').is_dir()]
        return path_list

    def _scan_directory_recursively(self, root: Path, path_list: list[Path] = None):
        """
        recursively scan a directory and its subdirectories and return a list of directories.
        :param root: root directory
        :param path_list: temporary variable for recursion
        """
        if path_list is None:
            path_list = []

        if not root.exists():
            logging.error(f"Directory {root} does not exist")
            raise FileNotFoundError

        for path_item in root.iterdir():
            # pass the folder begin with .
            if path_item.name.startswith("."):
                continue
            if path_item.is_dir():
                path_list.append(path_item)

                self._scan_directory_recursively(path_item, path_list)

    @staticmethod
    def check_git_status(path: Path):

        result = subprocess.run(['git', 'status', '--porcelain'], cwd=str(path), text=True, capture_output=True,
                                check=True)

        status_output = result.stdout
        if not status_output:
            return GitStatus.CLEAN, ""
        else:
            return GitStatus.NOT_CLEAN, status_output
