from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from config.config_reader import FrameworkConfig


class DriverFactory:
    @staticmethod
    def create_driver(config: FrameworkConfig) -> WebDriver:
        browser_name = config.browser.lower().strip()
        if browser_name != "chrome":
            raise NotImplementedError(f"Browser '{config.browser}' is not implemented yet. Add support in DriverFactory.")

        options = DriverFactory._build_chrome_options(config)
        driver_version = DriverFactory._detect_chrome_version()
        manager = ChromeDriverManager(driver_version=driver_version) if driver_version else ChromeDriverManager()
        service = ChromeService(manager.install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        if config.implicit_wait:
            driver.implicitly_wait(config.implicit_wait)
        return driver

    @staticmethod
    def _build_chrome_options(config: FrameworkConfig) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--start-maximized")

        if config.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        download_directory = Path(config.download_dir).resolve()
        download_directory.mkdir(parents=True, exist_ok=True)
        preferences = {
            "download.default_directory": str(download_directory),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", preferences)
        return options

    @staticmethod
    def _detect_chrome_version() -> str | None:
        if platform.system().lower() != "windows":
            chrome_binary = shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium")
            if chrome_binary:
                return DriverFactory._read_browser_version([chrome_binary, "--version"])
            return None

        candidate_paths = [
            Path(os.environ.get("PROGRAMFILES", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        ]

        for browser_path in candidate_paths:
            if browser_path.exists():
                version = DriverFactory._read_browser_version([str(browser_path), "--version"])
                if version:
                    return version
        return None

    @staticmethod
    def _read_browser_version(command: list[str]) -> str | None:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except (OSError, subprocess.CalledProcessError):
            return None

        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout)
        return match.group(1) if match else None
