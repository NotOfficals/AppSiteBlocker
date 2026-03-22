import sys
import time
import ctypes
import socket
import logging
import threading
from pathlib import Path

from utils.config import Config
from utils.hosts import HostsManager
from utils.apps import AppGuard
from utils.tray import TrayManager
from utils.ui import print_ui


CONFIG_PATH = Path(__file__).parent / "config.json"
LOG_PATH = Path(__file__).parent / "appsiteblocker.log"

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class AppSiteBlocker:

    APP_NAME = "AppSiteBlocker"

    def __init__(self):
        self.config = Config.load(CONFIG_PATH)
        self.guard = AppGuard(self.config.blocked_apps)
        self.hosts = HostsManager(self.config.blocked_sites)
        self.tray = TrayManager(self.APP_NAME)
        self.protection_active = False
        self.window_visible = True
        self._stop = False

    def enable(self):
        self.hosts.block()
        self.guard.start()
        self.protection_active = True
        logger.info("protection enabled")

    def disable(self):
        self.protection_active = False
        self.guard.stop()
        self.hosts.unblock()
        logger.info("protection disabled")

    def reload_config(self):
        self.config = Config.load(CONFIG_PATH)
        self.guard.keywords = self.config.blocked_apps
        self.hosts = HostsManager(self.config.blocked_sites)

    def run(self):
        logger.info("started on %s", socket.gethostname())
        threading.Thread(target=self._title_loop, daemon=True).start()

        try:
            while not self._stop:
                if not self.window_visible:
                    time.sleep(0.1)
                    continue
                last_killed = self.guard.kill_log[-1] if self.guard.kill_log else None
                print_ui(self.protection_active, len(self.config.blocked_sites), len(self.config.blocked_apps), last_killed)
                try:
                    choice = input("  > ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                self._handle(choice)
        finally:
            if self.protection_active:
                self.disable()
            self._stop = True

    def _handle(self, choice: str):
        if choice == "1":
            self.enable()
        elif choice == "2":
            self.disable()
        elif choice == "3":
            self.reload_config()
        elif choice == "4":
            self._minimize()
        elif choice == "5":
            self._stop = True

    def _minimize(self):
        self.window_visible = False
        self.tray.show(
            is_active=self.protection_active,
            on_open=self._on_tray_open,
            on_enable=self.enable,
            on_exit=self._on_tray_exit,
        )

    def _on_tray_open(self):
        self.window_visible = True

    def _on_tray_exit(self):
        if self.protection_active:
            self.disable()
        self._stop = True

    def _title_loop(self):
        while not self._stop:
            status = "ACTIVE" if self.protection_active else "INACTIVE"
            ctypes.windll.kernel32.SetConsoleTitleW(f"{self.APP_NAME} [{status}]")
            time.sleep(1)


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    AppSiteBlocker().run()



def print_ui():
    os.system("cls")
    print_banner()

    status_color = "green" if protection_active else "red"
    status_text = "ACTIVE" if protection_active else "INACTIVE"

    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column(style="dim", width=16)
    info.add_column()
    info.add_row("status", f"[{status_color} bold]{status_text}[/{status_color} bold]")
    info.add_row("sites", str(len(blocked_sites)))
    info.add_row("apps", str(len(blocked_apps)))
    if kill_log:
        info.add_row("last killed", kill_log[-1])
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


def run():
    global stop_flag
    load_config()
    logging.info("Started on %s", socket.gethostname())
    threading.Thread(target=guard_loop, daemon=True).start()
    threading.Thread(target=title_loop, daemon=True).start()

    try:
        while not stop_flag:
            if not window_visible:
                time.sleep(0.1)
                continue
            print_ui()
            try:
                choice = input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if choice == "1":
                enable_protection()
            elif choice == "2":
                disable_protection()
            elif choice == "3":
                load_config()
            elif choice == "4":
                hide_to_tray()
            elif choice == "5":
                break
    finally:
        if protection_active:
            disable_protection()
        stop_flag = True


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    run()