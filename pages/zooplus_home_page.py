from config import zooplus_config
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

class ZooplusHomePage:
    """POM class for zooplus home page"""
    def __init__(self, page: Page):
        self.page = page
        self.url = zooplus_config.current_url
        self.menu_button = self.page.get_by_role("button", name="Meny för mitt zooplus")
        self.bonus_balance = self.page.get_by_test_id('balance-points-header-component').first

    def open(self):
        """Opens the page and accepts cookies if needed"""
        self.page.goto(self.url)
        cookie_button = self.page.get_by_role("button", name="Endast nödvändiga kakor")
        try:
            # Wait for cookie_button to be visible
            cookie_button.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            pass
        else:
            cookie_button.click()
        # update title attribute when page is opened
        expect(self.bonus_balance).to_be_visible()