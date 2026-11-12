import re
from playwright.sync_api import Page, expect, Locator, TimeoutError as PlaywrightTimeoutError

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
        self.prev_page = self.pagination.locator('[data-zta=paginationPrevious]')
        self.next_page = self.pagination.locator('[data-zta=paginationNext]')
        self.min_price = page.get_by_role("textbox", name="Lägsta pris")
        self.max_price = page.get_by_role("textbox", name="Högsta pris")
        self.sorting_selector = page.locator('[data-zta="product-sorting-selector"]')
        self.sorting_button = self.sorting_selector.locator('[data-zta="selectMenuTriggerButton"]')
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


    def wait(self, time: int) -> None:
        """Waits given amount of milliseconds"""
        self.page.wait_for_timeout(time)


    def verify_url(self, text) -> None:
        """Verify that given text exists in the url"""
        expect(self.page).to_have_url(re.compile(re.escape(text)))


    def filter_button(self, name: str) -> Locator:
        """Finds and returns locator for filter button by name
        Clicks the button to expand filter options if it wasn't """
        button = self.page.get_by_role("button", name=name, exact=True)
        if button.get_attribute("aria-expanded") != "true":
            button.click()
        return button


    def searchbox_inside_filter(self, name: str) -> Locator:
        """Returns locator for searchbox inside filter"""
        panel_id = self.filter_button(name).get_attribute('aria-controls')
        area = self.page.locator(f'#{panel_id}')
        searchbox = area.get_by_placeholder('Sök')
        return searchbox


    def options_inside_filter(self, name: str) -> Locator:
        """Finds and returns locator for all options inside filter"""
        panel_id = self.filter_button(name).get_attribute('aria-controls')
        area = self.page.locator(f'#{panel_id}')
        options = area.get_by_role('option')
        return options


    @staticmethod
    def option_name(option: Locator) -> str:
        """Returns options name"""
        return option.locator('[data-zta=checkbox-label]').inner_text().strip()


    @staticmethod
    def option_checkbox(option: Locator) -> Locator:
        """Returns locator for option's checkbox"""
        checkbox = option.get_by_role('checkbox')
        return checkbox


    @staticmethod
    def option_counter(option: Locator) -> int:
        """Returns amount of products which should be shown after applying this particular filter option"""
        match = re.search(r'\d+', option.inner_text())
        if match:
            count = match.group()
        else:
            raise AssertionError(f"Could not find counter near the option. Text was {option.inner_text()}")
        return int(count)


    def all_products(self) -> Locator:
        """Collects and returns all available products"""
        all_products = self.products_grid.locator('.ProductCard_productCard__HRbGU')
        return all_products


    @staticmethod
    def product_price(product: Locator) -> float | int:
        """Returns price of product"""
        price = product.locator('.z-product-price__amount').first.inner_text()
        match = re.search(r'(\d[\d\s]*,\d{2})\s*kr', price)
        if not match:
            raise AssertionError(f"Price was not found")
        normalized_price = re.sub(r'[\sa-z]+', "", match.group(1).replace(",", "."))
        return float(normalized_price)


    @staticmethod
    def product_name(product: Locator) -> str:
        """Returns name of product"""
        name = product.locator('[data-zta=product-link]').inner_text()
        if not name:
            raise AssertionError(f'Product name was not found')
        return name

    @staticmethod
    def product_id(product: Locator) -> str:
        """Returns id of product"""
        product_id = product.get_attribute("id")
        if not product_id:
            raise AssertionError('Product id was not found')
        return product_id


    def _select_sorting_option(self, option_value):
        """Private method used below in sorting methods"""
        self.sorting_button.click()
        self.sorting_selector.locator(
            f'[data-option-value="{option_value}"]'
        ).click()


    def sort_by_price_low_to_high(self):
        """Selects sorting by price from low to high"""
        self._select_sorting_option("lowest-price")


    def sort_by_price_high_to_low(self):
        """Selects sorting by price from high to low"""
        self._select_sorting_option("highest-price")