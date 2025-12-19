import logging
import subprocess
from pathlib import Path

from src.storage import Storage

from rich.console import Console
from rich.table import Table

console = Console()


class Manager:
    def __init__(self):
        self.storage = Storage(Path(__file__).parent.parent / 'data' / 'data.json')

    def scan_directory(self, root: Path) -> list[Path]:
        """
        scans a directory and its subdirectories.
        directory with . beginning are ignored.
        :param root: root directory
        :return: a list of subdirectories
        """
        path_list = []
        self._scan_directory_recursively(root, path_list)
        return path_list

    def _scan_directory_recursively(self, root: Path, path_list=None):
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

    def scan_projects(self, root: Path | str):
        if type(root) != Path:
            root = Path(root)

        path_list = self.scan_directory(root)
        project_list = []
        for path in path_list:
            for folder in path.iterdir():
                if folder.name.startswith(".git"):
                    project_list.append(path)
                    break
        # convert path to absolute path str
        absolute_path_list = [str(project.resolve()) for project in project_list]
        self.storage.add_project_list(project_list, absolute_path_list)
        print(f"In folder {root}: found {len(project_list)} projects:")
        for project in project_list:
            print(f"\t{project}")

    def list_projects(self):

        # create table to print
        table = Table(title="Projects", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="dim", width=12)
        table.add_column("Path")

        projects = self.storage.get_projects()
        for name in projects:
            table.add_row(name, projects[name])

        console.print(table)

    def check_git_status(self, path: Path):
        # check this is tracked project
        assert str(path) in self.storage.get_projects().values()
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=str(path), text=True, capture_output=True,
                                check=True)

        status_output = result.stdout
        if not status_output:
            console.print("Working tree is clean.")
        else:
            console.print("Detected changes:")
            console.print(status_output)



