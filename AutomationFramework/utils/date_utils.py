from __future__ import annotations

from datetime import date, datetime, timedelta


class DateUtils:
    @staticmethod
    def today(date_format: str = "%Y-%m-%d") -> str:
        return date.today().strftime(date_format)

    @staticmethod
    def future_date(days_ahead: int = 1, date_format: str = "%Y-%m-%d") -> str:
        return (date.today() + timedelta(days=days_ahead)).strftime(date_format)

    @staticmethod
    def past_date(days_behind: int = 1, date_format: str = "%Y-%m-%d") -> str:
        return (date.today() - timedelta(days=days_behind)).strftime(date_format)

    @staticmethod
    def format_date(value: date | datetime, date_format: str = "%Y-%m-%d") -> str:
        return value.strftime(date_format)

    @staticmethod
    def parse_date(value: str, date_format: str = "%Y-%m-%d") -> date:
        return datetime.strptime(value, date_format).date()

    @staticmethod
    def is_future_date(value: str, date_format: str = "%Y-%m-%d") -> bool:
        return DateUtils.parse_date(value, date_format) > date.today()
