from mdurl import URL
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError, Locator
import re


class ZooplusHomePage:
    """Zooplus home page"""
    URL = 'https://www.zooplus.se/'
    def __init__(self, page: Page):
        self.page: Page = page
        self.menu_button = self.page.get_by_role("button", name="Meny för mitt zooplus")
        self.bonus_balance = self.page.get_by_test_id('balance-points-header-component').first

    def decline_cookie(self):
        """Declines cookie"""
        cookie_button = self.page.get_by_role("button", name="Endast nödvändiga kakor")
        try:
            cookie_button.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            pass
        else:
            cookie_button.click()

    def open_home_page(self):
        """Opens home page"""
        self.page.goto(self.URL)
        self.decline_cookie()


class ZooplusLoginPage:
    """Zooplus login page"""
    def __init__(self, page: Page):
        self.page: Page = page
        self.login_field = self.page.get_by_role("textbox", name="E-postadress")
        self.pass_field = self.page.get_by_role("textbox", name="Lösenord")
        self.login_button = self.page.get_by_role("button", name="Logga in")

    def login(self, username: str, password: str):
        """Login by provided username and password"""
        self.login_field.fill(username)
        self.pass_field.fill(password)
        self.login_button.click()

    @staticmethod
    def open_login_page(homepage: ZooplusHomePage):
        """Navigates to login page"""
        homepage.open_home_page()
        homepage.menu_button.click()

    def check_url_redirection(self):
        """Verifies that user is redirected to right URL after login"""
        expect(self.page).to_have_url('https://www.zooplus.se/account/overview')

