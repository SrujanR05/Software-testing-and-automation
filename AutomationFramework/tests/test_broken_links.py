from __future__ import annotations

import pytest
import requests

from pages.links_page import LinksPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.broken_links
def test_broken_link_validation(driver, framework_config):
    ensure_real_aut(framework_config.base_url)

    links_page = LinksPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    links_page.open(framework_config.base_url)
    links = links_page.collect_links()

    assert links, "At least one hyperlink should be present on the page"

    broken_links: list[str] = []
    for link in links:
        try:
            response = requests.get(link, timeout=15, allow_redirects=True)
            if response.status_code >= 400:
                broken_links.append(f"{link} -> {response.status_code}")
        except requests.RequestException as exc:
            broken_links.append(f"{link} -> {exc}")

    assert not broken_links, f"Broken links detected: {broken_links}"
