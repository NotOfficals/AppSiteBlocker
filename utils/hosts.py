import os
import logging
import subprocess
from pathlib import Path


logger = logging.getLogger(__name__)


class HostsManager:

    HOSTS_PATH = Path(r"C:\Windows\System32\drivers\etc\hosts")

    def __init__(self, sites: list[str]):
        self.sites = sites

    def block(self):
        try:
            self._ensure_writable()
            domains = self._get_domains()
            lines = self.HOSTS_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
            lines = [l for l in lines if not any(d in l for d in domains)]
            for d in domains:
                lines.append(f"127.0.0.1 {d}\n")
            self.HOSTS_PATH.write_text("".join(lines), encoding="utf-8")
            self._flush_dns()
            logger.info("blocked %d domains", len(domains))
        except OSError as e:
            logger.error("block failed: %s", e)

    def unblock(self):
        try:
            self._ensure_writable()
            domains = self._get_domains()
            lines = self.HOSTS_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
            lines = [l for l in lines if not any(d in l for d in domains)]
            self.HOSTS_PATH.write_text("".join(lines), encoding="utf-8")
            self._flush_dns()
            logger.info("unblocked sites")
        except OSError as e:
            logger.error("unblock failed: %s", e)

    def _get_domains(self) -> list[str]:
        seen = set()
        result = []
        for entry in self.sites:
            d = self._normalize(entry)
            if not d:
                continue
            if d not in seen:
                seen.add(d)
                result.append(d)
            if not d.startswith("www."):
                www = "www." + d
                if www not in seen:
                    seen.add(www)
                    result.append(www)
        return result

    def _normalize(self, domain: str) -> str:
        domain = domain.strip()
        if "://" in domain:
            domain = domain.split("://", 1)[1]
        domain = domain.split("/")[0]
        domain = domain.split(":")[0]
        return domain.lower()

    def _ensure_writable(self):
        path = str(self.HOSTS_PATH)
        subprocess.run(["attrib", "-r", path], capture_output=True)
        user = os.environ.get("USERNAME", "Administrators")
        subprocess.run(["icacls", path, "/grant", f"{user}:(F)", "/grant", "Administrators:(F)"], capture_output=True)

    def _flush_dns(self):
        subprocess.run(["net", "stop", "dnscache"], capture_output=True)
        subprocess.run(["net", "start", "dnscache"], capture_output=True)
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
