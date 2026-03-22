import ctypes
import logging
import threading
from typing import Callable

from pystray import Icon, MenuItem
from PIL import Image, ImageDraw


logger = logging.getLogger(__name__)


class TrayManager:

    def __init__(self, app_name: str):
        self.app_name = app_name

    def show(self, is_active: bool, on_open: Callable, on_enable: Callable, on_exit: Callable):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.ShowWindow(hwnd, 0)

        def open_window(icon):
            icon.stop()
            ctypes.windll.user32.ShowWindow(hwnd, 1)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            on_open()

        def enable(icon):
            on_enable()

        def exit_app(icon):
            icon.stop()
            on_exit()
            ctypes.windll.user32.ShowWindow(hwnd, 1)

        label = f"{self.app_name} [{'ACTIVE' if is_active else 'INACTIVE'}]"
        icon = Icon(self.app_name, self._make_icon(), label, menu=(
            MenuItem("Open", open_window),
            MenuItem("Enable protection", enable),
            MenuItem("Exit", exit_app),
        ))
        threading.Thread(target=icon.run, daemon=True).start()

    def _make_icon(self) -> Image.Image:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        outer = [(32, 4), (60, 16), (60, 38), (32, 60), (4, 38), (4, 16)]
        inner = [(32, 14), (50, 22), (50, 36), (32, 50), (14, 36), (14, 22)]
        draw.polygon(outer, fill=(30, 60, 140))
        draw.polygon(outer, outline=(80, 140, 255), width=2)
        draw.polygon(inner, outline=(120, 180, 255), width=1)
        return img
