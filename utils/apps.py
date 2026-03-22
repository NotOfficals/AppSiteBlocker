import time
import logging
import threading

import psutil


logger = logging.getLogger(__name__)


class AppGuard:

    def __init__(self, keywords: list[str]):
        self.keywords = keywords
        self.kill_log: list[str] = []
        self._active = False
        self._thread: threading.Thread | None = None

    def start(self):
        self._active = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._active = False

    def _loop(self):
        while self._active:
            for proc in psutil.process_iter(["name", "pid"]):
                try:
                    name = (proc.info["name"] or "").lower()
                    if any(kw in name for kw in self.keywords):
                        proc.terminate()
                        time.sleep(0.05)
                        try:
                            proc.kill()
                        except psutil.NoSuchProcess:
                            pass
                        entry = f"{proc.info['name']} (PID {proc.info['pid']})"
                        self.kill_log.append(entry)
                        if len(self.kill_log) > 20:
                            self.kill_log.pop(0)
                        logger.info("killed: %s", entry)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(0.8)
