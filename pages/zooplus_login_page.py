from playwright.sync_api import Page, expect
from pages import ZooplusHomePage
from config import zooplus_config


class ZooplusLoginPage:
    """POM class for zooplus login page"""
    def __init__(self, page: Page):
        self.page: Page = page
        self.login_field = self.page.get_by_role("textbox", name="E-postadress")
        self.pass_field = self.page.get_by_role("textbox", name="Lösenord")
        self.name_field = self.page.get_by_role('textbox', name="Förnamn")
        self.surname_field = self.page.get_by_role('textbox', name="Efternamn")
        self.login_button = self.page.get_by_role("button", name="Logga in")
        self.register_button = self.page.get_by_role("button", name="Registrera")
        self.login_tab = self.page.locator("#tab-navigation").get_by_text("Logga in")
        self.register_tab = self.page.locator("#tab-navigation").get_by_text('Registrera')
        self.forgot_pass = self.page.get_by_role("link", name="Glömt ditt lösenord?")
        self.header = self.page.get_by_role('heading')


    @staticmethod
    def open(homepage: ZooplusHomePage):
        """Navigates to login page"""
        homepage.open()
        homepage.menu_button.click()


    def open_login_tab(self):
        """Switches to login tab"""
        self.login_tab.click()


    def open_register_tab(self):
        """Switches to register tab"""
        self.register_tab.click()


    def login(self, username: str, password: str):
        """Login by provided username and password"""
        self.login_field.fill(username)
        self.pass_field.fill(password)
        self.login_button.click()


    def register(self, name: str, surname: str, email: str, password: str):
        pass


    def check_url_redirection(self):
        """Verifies that user is redirected to right URL after login"""
        expect(self.page).to_have_url(f'{zooplus_config.current_url}account/overview')
