import json
import logging
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class Config:
    blocked_sites: list[str]
    blocked_apps: list[str]

    @classmethod
    def load(cls, path: Path) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        config = cls(
            blocked_sites=data.get("blocked_sites", []),
            blocked_apps=[a.lower() for a in data.get("blocked_apps", [])],
        )
        logger.info("config loaded: %d sites, %d apps", len(config.blocked_sites), len(config.blocked_apps))
        return config
