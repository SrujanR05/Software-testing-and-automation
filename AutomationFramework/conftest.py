from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    from pytest_html import extras as html_extras
except Exception:
    html_extras = None

from config.config_reader import ConfigReader, FrameworkConfig
from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from utils.screenshot_helper import ScreenshotHelper

PROJECT_ROOT = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def framework_config() -> FrameworkConfig:
    return ConfigReader().load()


@pytest.fixture(scope="session")
def logger(framework_config: FrameworkConfig):
    return get_logger("automation", framework_config.log_dir)


@pytest.fixture(scope="session")
def base_url(framework_config: FrameworkConfig) -> str:
    return framework_config.base_url


@pytest.fixture(scope="session")
def api_base_url(framework_config: FrameworkConfig) -> str:
    return framework_config.api_base_url


@pytest.fixture(scope="session")
def test_data() -> dict:
    data_file = PROJECT_ROOT / "data" / "test_data.json"
    return json.loads(data_file.read_text(encoding="utf-8"))


@pytest.fixture()
def driver(framework_config: FrameworkConfig, logger):
    if not framework_config.base_url or "your-application-url.example" in framework_config.base_url:
        pytest.skip("Replace config/settings.ini with a real AUT base_url to run UI tests.")

    web_driver = DriverFactory.create_driver(framework_config)
    logger.info("Browser session started")
    yield web_driver
    web_driver.quit()
    logger.info("Browser session closed")


@pytest.fixture()
def api_helper(framework_config: FrameworkConfig):
    from utils.api_helper import APIHelper

    return APIHelper(base_url=framework_config.api_base_url)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    driver_instance = item.funcargs.get("driver")
    config = item.funcargs.get("framework_config")
    if driver_instance is None or config is None:
        return

    screenshot_path = ScreenshotHelper.capture(driver_instance, config.screenshot_dir, item.name)
    if html_extras is not None:
        report.extra = getattr(report, "extra", [])
        report.extra.append(html_extras.image(screenshot_path))
    item.add_report_section("call", "screenshot", screenshot_path)
