from __future__ import annotations

from typing import Any

import requests


class APIHelper:
    def __init__(self, base_url: str = "", headers: dict[str, str] | None = None, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        url = self._build_url(endpoint)
        response = self.session.request(method=method.upper(), url=url, **kwargs)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    @staticmethod
    def parse_json(response: requests.Response) -> Any:
        response.raise_for_status()
        return response.json()

    @staticmethod
    def assert_status_code(response: requests.Response, expected_status: int) -> None:
        actual_status = response.status_code
        assert actual_status == expected_status, f"Expected HTTP {expected_status}, got HTTP {actual_status}"
