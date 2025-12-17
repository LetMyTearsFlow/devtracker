import typer
from pathlib import Path

from manager import Manager

app = typer.Typer()
manager = Manager()

@app.command()
def scan(path: str) -> None:
    """
    扫描路径下的全部git项目并添加至存储

    :param path:文件夹路径
    """
    print(path)
    manager.scan_projects(path)

@app.command()
def list() -> None:
    """
    用表格列表显示所有项目的项目名，最后修改时间，Git状态
    """
    pass

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