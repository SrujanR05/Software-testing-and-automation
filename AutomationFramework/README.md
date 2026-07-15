# AutomationFramework

Enterprise-style UI automation framework for Python 3.13.7 using Pytest, Selenium, Chrome, webdriver-manager, pytest-html, and pytest-xdist.

## Project Structure

```text
AutomationFramework/
├── tests/
├── pages/
├── utils/
├── config/
├── data/
├── reports/
├── screenshots/
├── logs/
├── requirements.txt
├── pytest.ini
├── conftest.py
└── README.md
```

## What Is Included

- Page Object Model structure with reusable base page actions
- Driver factory with Chrome, headless support, and webdriver-manager
- Explicit waits only
- Logging to file and console
- Automatic screenshots on failures
- HTML reporting with pytest-html
- Data-driven support for JSON and Excel
- API helper for response validation
- File download verification helper
- Date utilities
- Sample test cases for the requested scenarios

## Installation

Run the commands below from the `AutomationFramework/` folder.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Update `config/settings.ini` with your application values:

- Base URL
- API Base URL
- Username
- Password
- Browser
- Headless mode

The framework also supports environment variable overrides for these settings.

## Running Tests

Run all tests:

```bash
pytest
```

Run a single test:

```bash
pytest tests/test_sample.py
```

Generate HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```

Parallel execution:

```bash
pytest -n 4
```

## Notes

- The sample page objects use template locators. Replace them with your application's real selectors.
- The scenario tests will self-skip until you replace the placeholder URLs in `config/settings.ini` with a real AUT.
- `tests/test_sample.py` is a lightweight framework smoke test and should run without the AUT.

## Key Files

- `conftest.py` handles browser setup, teardown, fixtures, and screenshot capture on failure.
- `utils/driver_factory.py` creates the Chrome WebDriver instance.
- `pages/base_page.py` contains reusable page actions.
- `utils/logger.py` centralizes logging.
- `utils/excel_reader.py` reads data from Excel files.
- `utils/api_helper.py` wraps HTTP requests for API validation.

## Suggested Next Step

Replace the template locators with your application selectors and point `config/settings.ini` at the real application under test.
