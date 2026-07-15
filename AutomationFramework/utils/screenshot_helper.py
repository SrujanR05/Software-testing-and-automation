from __future__ import annotations

from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver


class ScreenshotHelper:
    @staticmethod
    def capture(driver: WebDriver, screenshot_dir: str | Path, name: str = "screenshot") -> str:
        directory = Path(screenshot_dir)
        directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = directory / f"{name}_{timestamp}.png"
        driver.save_screenshot(str(file_path))
        return str(file_path)
