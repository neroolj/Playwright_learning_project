from playwright.sync_api import Page, expect


class ZooplusHomePage:
    def __init__(self, page: Page):
        self.page: Page = page
        self.menu_button = self.page.get_by_role("button", name="Meny för mitt zooplus")
        self.bonus_balance = self.page.get_by_test_id('balance-points-header-component').first

    def decline_cookie(self):
        self.page.get_by_role("button", name="Endast nödvändiga kakor").click()

    def open_home_page(self):
        self.page.goto("https://www.zooplus.se/")
        self.decline_cookie()


class ZooplusLoginPage:
    def __init__(self, page: Page):
        self.page: Page = page
        self.login_field = self.page.get_by_role("textbox", name="E-postadress")
        self.pass_field = self.page.get_by_role("textbox", name="Lösenord")
        self.login_button = self.page.get_by_role("button", name="Logga in")

    def login(self, username: str, password: str):
        self.login_field.fill(username)
        self.pass_field.fill(password)
        self.login_button.click()

    def open_login_page(self, homepage: ZooplusHomePage):
        homepage.open_home_page()
        homepage.menu_button.click()

    def check_url_redicrection(self):
        expect(self.page).to_have_url('https://www.zooplus.se/account/overview')
