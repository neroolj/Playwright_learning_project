import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.skip_browser('firefox')
def test_header(page: Page, browser_name, browser_channel):
    """Example of usage 'to_have_title' method"""
    page.goto("https://playwright.dev/")
    print('\nBROWSER =', browser_name)
    print('\nBROWSER CHANNEL =', browser_channel)
    expect(page).to_have_title(re.compile("Playwright"))

@pytest.mark.only_browser('chromium')
def test_get_started_link_is_present(page: Page):
    """Example of usage 'to_be_visible' method"""
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    heading = page.get_by_role("heading", name="Installation")
    expect(heading).to_be_visible()
