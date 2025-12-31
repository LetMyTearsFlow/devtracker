from datetime import datetime, timedelta

import readchar
import typer
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.live import Live

from src.manager import Manager, GitStatus
from src.storage import Storage
from src.timer import timer
from src.note import note_from_external

app = typer.Typer()
manager = Manager()
storage = Storage(Path(__file__).parent / 'data' / 'data.json')
console = Console()


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
def show() -> None:
    """
    用表格列表显示所有项目的项目名，最后修改时间，Git状态
    """
    table = Table(title="Projects", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="dim", width=12)
    table.add_column("Path")
    table.add_column("Status", style="purple4", width=12)

    projects = storage.get_projects()
    for name in projects:
        status, _ = manager.check_git_status(projects[name])
        if status == GitStatus.CLEAN:
            status_str = "Clean"
        else:
            status_str = "Not Clean"
        table.add_row(name, projects[name], status_str)

    console.print(table)


@app.command()
def start() -> None:
    """
    开始对某个项目进行专注学习。终端持续显示计时器，按C退出计时，计时结束后提醒用户输入学到什么/完成什么功能
    自动保存项目名，日期，时长，学习内容。
    """
    projects = list(storage.get_projects().keys())
    index = 0

    def render():
        table = Table(show_header=False, box=None)
        for i, project in enumerate(projects):
            if i == index:
                table.add_row(Text(f"> {project}"), style="magenta")
            else:
                table.add_row(f"> {project}", style="blue")
        return table

    with Live(render(), console=console, refresh_per_second=30) as live:
        while True:
            key = readchar.readkey()
            if key == readchar.key.UP:
                index = (index - 1) % len(projects)
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(projects)
            elif key == readchar.key.ENTER:

                break

            live.update(render())

    console.print(f"选择了{projects[index]}")
    project_name = projects[index]
    start_time, duration_time = timer(project_name)

    # user note
    note = note_from_external(project_name)

    # build a session object
    session = {
        "project": project_name,
        "start_time": datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S"),
        "duration_seconds": duration_time,
        "note": note
    }
    storage.add_session(session)


@app.command()
def stats():
    """
    显示本周学习时长（每周从周一开始）
    显示最近5条学习日志。
    """

    def in_current_week(date_str: str):
        # find the current week's Monday
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return monday <= date <= sunday

    sessions_this_week = [session for session in storage.sessions if in_current_week(session["start_time"])]
    total_time = sum(session["duration_seconds"] for session in sessions_this_week)
    print(f"This week's working time:{total_time}s, well done!")
    print(f"past sessions")
    for session in storage.sessions:
        print(session['note'])


if __name__ == "__main__":
    app()
