"""Specific fixtures for Playwright tests examples"""
import os

import pytest
from dotenv import load_dotenv
from pages import ProductPage
from playwright.sync_api import sync_playwright, Page, Browser


# load variables from .env
load_dotenv()

# define location of auth_data
STATE_FILE = ".auth_states/test_state.json"
STATE_FOLDER = STATE_FILE.split("/")[0]


@pytest.fixture(scope="session", autouse=True)
def generate_auth_state_demoblaze() -> None:
    """Fixture to create test_state.json for demoblaze.com if it doesn't exist"""
    # Create folder for auth file if it doesn't exist
    if not os.path.exists(STATE_FOLDER):
        os.mkdir(STATE_FOLDER)

    # Create auth file only if it doesn't exist
    if not os.path.exists(STATE_FILE):
        test_user = os.getenv("DEMOBLAZE_USER")
        test_pass = os.getenv("DEMOBLAZE_PASS")

        with sync_playwright() as p:
            # Create browser -> context -> page
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            # Login
            page.goto("https://demoblaze.com/")
            page.get_by_role("link", name="Log in").click()
            page.locator("#loginusername").fill(test_user)
            page.locator("#loginpassword").fill(test_pass)
            page.get_by_role("button", name="Log in").click()

            # Make sure that login is finished
            page.locator("#nameofuser").wait_for()

            # Save data to file
            context.storage_state(path=STATE_FILE)
            browser.close()


@pytest.fixture()
def auth_page_test(browser: Browser):
    """Fixture creates page using logged on state from "test_state.json" file """
    context = browser.new_context(storage_state=".auth_states/test_state.json")
    page = context.new_page()
    page.goto('https://demoblaze.com/')
    yield page
    page.close()


@pytest.fixture()
def product_page(page: Page) -> ProductPage:
    """Fixture creates instance of a ProductPage"""
    item = ProductPage(page)
    return item