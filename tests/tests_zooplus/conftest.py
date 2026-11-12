"""Specific fixtures for zooplus testing"""

import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, Browser, BrowserContext, TimeoutError as PlaywrightTimeoutError
from pages import ZooplusHomePage, ZooplusLoginPage, ZooplusDryFoodPage


# Load variables from .env
load_dotenv()
ZOOPLUS_USERNAME = os.getenv('ZOOPLUS_USERNAME')
ZOOPLUS_PASSWORD = os.getenv('ZOOPLUS_PASSWORD')


@pytest.fixture()
def zooplus_homepage(page: Page):
    """Fixture creates page with accepted cookies"""
    page.goto("https://www.zooplus.se/")
    cookie_button = page.get_by_role("button", name="Endast nödvändiga kakor")
    try:
        # Wait for cookie_button to be visible
        cookie_button.wait_for(state="visible", timeout=3000)
    except PlaywrightTimeoutError:
        pass
    else:
        cookie_button.click()
    return page

@pytest.fixture(scope="session")
def auth_context_zooplus(browser: Browser):
    """Fixture creates logged in context for zooplus"""
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.zooplus.se/")
    cookie_button = page.get_by_role("button", name="Endast nödvändiga kakor")
    try:
        # Wait for cookie_button to be visible
        cookie_button.wait_for(state="visible", timeout=3000)
    except PlaywrightTimeoutError:
        pass
    else:
        cookie_button.click()
    page.get_by_role("button", name="Meny för mitt zooplus").click()
    page.get_by_role("textbox", name="E-postadress").fill(ZOOPLUS_USERNAME)
    page.get_by_role("textbox", name="Lösenord").fill(ZOOPLUS_PASSWORD)
    page.get_by_role("button", name="Logga in").click()
    page.get_by_test_id('balance-points-header-component').first.wait_for()
    yield context
    context.close()


@pytest.fixture()
def auth_page_zooplus(auth_context_zooplus : BrowserContext):
    """Fixture creates page based on logged in context"""
    page = auth_context_zooplus.new_page()
    yield page
    page.close()


@pytest.fixture()
def zooplus_homepage_pom(page: Page) -> ZooplusHomePage:
    """Fixture creates Zooplus HomePage"""
    item = ZooplusHomePage(page)
    return item


@pytest.fixture()
def zooplus_loginpage_pom(page: Page) -> ZooplusLoginPage:
    """Fixture creates Zooplus LoginPage"""
    item = ZooplusLoginPage(page)
    return item


@pytest.fixture()
def zooplus_dryfoodpage_pom(page: Page) -> ZooplusDryFoodPage:
    """Fixture creates Zooplus Dry Food page"""
    item = ZooplusDryFoodPage(page)
    return item