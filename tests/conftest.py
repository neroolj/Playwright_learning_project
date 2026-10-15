import pytest
import allure
import os
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page, BrowserContext, sync_playwright
from pages.product_page import ProductPage


# Load variables from .env
load_dotenv()
ZOOPLUS_USERNAME = os.getenv('USERNAME')
ZOOPLUS_PASSWORD = os.getenv('PASSWORD')

# define location of auth_data
STATE_FILE = "../.auth_states/test_state.json"


@pytest.fixture(scope="session", autouse=True)
def generate_auth_state_demoblaze():
    """Fixture to create test_state.json for demoblaze.com"""
    # Create folder if it doesn't exist
    if not os.path.exists('../.auth_states'):
        os.mkdir('../.auth_states')

    # Create file only if it doesn't exist
    if not os.path.exists(STATE_FILE):
        test_user = os.getenv("TEST_USER")
        test_pass = os.getenv("TEST_PASS")

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


@pytest.fixture(scope="session")
def auth_context_zooplus(browser: Browser):
    """Fixture creates logged in context for zooplus"""
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.zooplus.se/")
    page.get_by_role("button", name="Endast nödvändiga kakor").click()
    page.get_by_role("button", name="Meny för mitt zooplus").click()
    page.get_by_role("textbox", name="E-postadress").fill(ZOOPLUS_USERNAME)
    page.get_by_role("textbox", name="Lösenord").fill(ZOOPLUS_PASSWORD)
    page.get_by_role("button", name="Logga in").click()
    page.get_by_test_id('balance-points-header-component').first.wait_for()
    context.storage_state(path='../.auth_states/zooplus_state.json')
    yield context
    context.close()


@pytest.fixture()
def auth_page_zooplus(auth_context_zooplus : BrowserContext):
    """Fixture creates page based on logged in context"""
    page = auth_context_zooplus.new_page()
    yield page
    page.close()


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
    """Fixture creates ProductPage"""
    item = ProductPage(page)
    return item


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """This hook collects screenshot and attach it to Allure report if test failed"""""

    # save test result which is sent by Pytest via .send() method
    outcome = yield

    # extract result
    report = outcome.get_result()

    # check if we are on executing stage and test failed
    if report.when == "call" and report.failed:

        # save current page element depending on which fixture is used
        page = item.funcargs.get('page') or item.funcargs.get('auth_page_test') or item.funcargs.get('auth_page_zooplus')

        # if page exists collect screenshot and attach it to Allure report
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.fixture()
def mock_backend_error():
    """Fixture captures API requests and mocks response with error code"""
    # list of supported codes
    error_codes = {400: 'Bad request',
                   401: 'Unauthorized',
                   403: 'Forbidden',
                   404: 'Page not found',
                   500: 'Internal server error',
                   503: 'Service unavailable',
                   504: 'Gateway timeout',}
    # nested function where response replacement logig is implemented
    def _mock(page: Page, api: str, status_code: int):
        page.route(api, lambda route: route.fulfill(
            status=status_code,
            json={"errorMessage": error_codes.get(status_code, 'Unknown error')})
                   )
    return _mock