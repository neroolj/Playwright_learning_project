from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError, Locator
import re


class ZooplusHomePage:
    """Zooplus home page"""
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
        self.page.goto("https://www.zooplus.se/")
        self.decline_cookie()


class ZooplusLoginPage:
    """Zooplus login page"""
    def __init__(self, page: Page):
        self.page: Page = page
        self.login_field = self.page.get_by_role("textbox", name="E-postadress")
        self.pass_field = self.page.get_by_role("textbox", name="Lösenord")
        self.login_button = self.page.get_by_role("button", name="Logga in")

    def login(self, username: str, password: str):
        self.login_field.fill(username)
        self.pass_field.fill(password)
        self.login_button.click()

    @staticmethod
    def open_login_page(homepage: ZooplusHomePage):
        homepage.open_home_page()
        homepage.menu_button.click()

    def check_url_redirection(self):
        expect(self.page).to_have_url('https://www.zooplus.se/account/overview')


class ZooplusDryFoodPage:
    """Zooplus dogs dry food page"""
    URL = "https://www.zooplus.se/shop/hund/hundmat_torrfoder"
    FILTERS = ['Märke', 'Hundstorlek', 'Smak', 'Pris', 'Hundens ålder', 'Specialfoder för hund']

    def __init__(self, page: Page):
        self.page = page
        self.heading = self.page.get_by_text("Hundfoder: torrfoder för hundar")
        self.products_grid = self.page.locator('[data-zta=product-grid-wrapper]')
        self.breadcrumbs = self.page.get_by_role("navigation", name="breadcrumbs")
        self.searchbox = self.page.get_by_role("searchbox", name="Sök efter produkter")
        self.pagination = self.page.locator(".z-pagination")
        self.title = ''


    def open(self):
        """Opens the page and accepts cookies if needed"""
        self.page.goto(self.URL)
        cookie_button = self.page.get_by_role("button", name="Endast nödvändiga kakor")
        try:
            # Wait for cookie_button to be visible
            cookie_button.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            pass
        else:
            cookie_button.click()
        # update title attribute when page is opened
        self.title = self.page.title()
        expect(self.heading).to_be_visible()

    def filter_button(self, name: str) -> Locator:
        """Finds and returns locator for filter button by name"""
        button = self.page.get_by_role("button", name=name, exact=True)
        if button.get_attribute("aria-expanded") != "true":
            button.click()
        return button

    def all_products(self):
        """Collects all available products"""
        all_products = self.products_grid.locator('.ProductCard_productCard__HRbGU')
        return all_products

    @staticmethod
    def product_price(product: Locator) -> float | int:
        """Returns the price of product"""
        price = product.locator('.z-product-price__amount').inner_text()
        match = re.search(r'(\d[\d\s]*,\d{2})\s*kr', price)
        if not match:
            raise AssertionError(f"Price was not found")
        normalized_price = re.sub(r'[\sa-z]+', "", match.group(1).replace(",", "."))
        return float(normalized_price)

    def all_products_prices(self, all_products: Locator) -> list[float | int]:
        """Returns list of prices of all available products"""
        pass