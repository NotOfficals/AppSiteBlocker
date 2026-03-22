import os
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box


console = Console()

BANNER = [
    "",
    "   █████╗ ██████╗ ██████╗ ",
    "  ██╔══██╗██╔════╝██╔══██╗",
    "  ███████║███████╗██████╔╝",
    "  ██╔══██║╚════██║██╔══██╗",
    "  ██║  ██║███████║██████╔╝",
    "  ╚═╝  ╚═╝╚══════╝╚═════╝ ",
    "  AppSiteBlocker · windows",
    "",
]


def print_ui(protection_active: bool, sites_count: int, apps_count: int, last_killed: Optional[str]):
    os.system("cls")
    _print_banner()

    color = "green" if protection_active else "red"
    status = "ACTIVE" if protection_active else "INACTIVE"

    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column(style="dim", width=16)
    info.add_column()
    info.add_row("status", f"[{color} bold]{status}[/{color} bold]")
    info.add_row("sites", str(sites_count))
    info.add_row("apps", str(apps_count))
    if last_killed:
        info.add_row("last killed", last_killed)
    console.print(info)

    menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    menu.add_column(style="bold cyan", width=4)
    menu.add_column(style="dim")
    menu.add_row("1", "enable protection")
    menu.add_row("2", "disable protection")
    menu.add_row("3", "reload config")
    menu.add_row("4", "minimize to tray")
    menu.add_row("5", "exit")
    console.print(menu)


def _print_banner():
    start = (20, 60, 160)
    end = (80, 160, 255)
    non_empty = [l for l in BANNER if l.strip()]
    total = len(non_empty)
    idx = 0
    for line in BANNER:
        if not line.strip():
            console.print()
            continue
        t = idx / max(total - 1, 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        text = Text(line)
        text.stylize(f"rgb({r},{g},{b})")
        console.print(text)
        idx += 1
