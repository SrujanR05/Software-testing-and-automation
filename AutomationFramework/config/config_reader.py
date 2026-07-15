from __future__ import annotations

import configparser
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FrameworkConfig:
    base_url: str
    api_base_url: str
    username: str
    password: str
    browser: str = "chrome"
    headless: bool = False
    explicit_wait: int = 20
    implicit_wait: int = 0
    screenshot_dir: str = "screenshots"
    report_dir: str = "reports"
    log_dir: str = "logs"
    download_dir: str = "downloads"


class ConfigReader:
    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path or Path(__file__).with_name("settings.ini"))
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        self._parser = configparser.ConfigParser()
        self._parser.read(self.config_path, encoding="utf-8")

    def _get(self, key: str, default: str = "") -> str:
        value = os.getenv(key.upper())
        if value is not None:
            return value.strip()
        return self._parser["DEFAULT"].get(key, default).strip()

    def _get_bool(self, key: str, default: bool = False) -> bool:
        value = self._get(key, str(default))
        return value.lower() in {"1", "true", "yes", "on"}

    def _get_int(self, key: str, default: int) -> int:
        value = self._get(key, str(default))
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"Invalid integer value for '{key}': {value}") from exc

    def load(self) -> FrameworkConfig:
        return FrameworkConfig(
            base_url=self._get("base_url"),
            api_base_url=self._get("api_base_url"),
            username=self._get("username"),
            password=self._get("password"),
            browser=self._get("browser", "chrome"),
            headless=self._get_bool("headless", False),
            explicit_wait=self._get_int("explicit_wait", 20),
            implicit_wait=self._get_int("implicit_wait", 0),
            screenshot_dir=self._get("screenshot_dir", "screenshots"),
            report_dir=self._get("report_dir", "reports"),
            log_dir=self._get("log_dir", "logs"),
            download_dir=self._get("download_dir", "downloads"),
        )
