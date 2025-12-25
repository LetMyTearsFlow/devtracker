import time

from rich.live import Live
from rich.console import Console
from rich.text import Text
import datetime
import threading
import keyboard

console = Console()


def timer(project_name):
    start_time = time.time()

    def render():
        elapse_time = time.time() - start_time
        text = Text(f"{project_name}: {str(datetime.timedelta(seconds=elapse_time))}")
        text.stylize("bold magenta")
        return text

    exit_event = threading.Event()
    def listen_exit():
        keyboard.wait('q')
        exit_event.set()

    threading.Thread(target=listen_exit, daemon=True).start()

    with Live(render(), console=console, refresh_per_second=30) as live:
        while not exit_event.is_set():
            live.update(render())
            time.sleep(0.05)

    # return total time
    return int(time.time() - start_time)
