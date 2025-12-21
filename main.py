import typer
from pathlib import Path

from src.manager import Manager
from src.storage import Storage

app = typer.Typer()
manager = Manager()
storage = Storage(Path(__file__).parent / 'data' / 'data.json')


@app.command()
def scan(path: str) -> None:
    """
    扫描路径下的全部git项目并添加至存储

    :param path:文件夹路径
    """
    print(path)
    projects = manager.scan_directory(Path(path))
    print(f"{len(projects)} project(s) found:")
    for project in projects:
        print(project)
    names = [project.name for project in projects]
    storage.add_project_list(names, projects)


@app.command()
def list() -> None:
    """
    用表格列表显示所有项目的项目名，最后修改时间，Git状态
    """
    manager.list_projects()


@app.command()
def start(project_name: str) -> None:
    """
    开始对某个项目进行专注学习。终端持续显示计时器，按C退出计时，计时结束后提醒用户输入学到什么/完成什么功能
    自动保存项目名，日期，时长，学习内容。
    :param project_name:
    """
    pass


@app.command()
def stats():
    """
    显示本周学习时长（每周从周一开始）
    显示最近5条学习日志。
    """
    pass


if __name__ == "__main__":
    app()
