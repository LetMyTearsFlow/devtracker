import time

from rich.live import Live
from rich.console import Console
from rich.text import Text
import datetime

console = Console()


def timer(project_name):
    start_time = time.time()

    def render():
        elapse_time = time.time() - start_time
        text = Text(f"{project_name}: {str(datetime.timedelta(seconds=elapse_time))}")
        text.stylize("bold magenta")
        return text

    with Live(render(), console=console, refresh_per_second=30) as live:
        while True:
            live.update(render())
