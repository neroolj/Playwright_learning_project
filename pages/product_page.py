from playwright.sync_api import Page, Locator
import re


class ProductPage:
    """Class for Product page. Example of Page Object Model pattern"""
    def __init__(self, page: Page):
        self.page: Page = page
        self.add_to_cart_button = self.page.get_by_text('Add to cart')


    def add_to_cart(self):
        """Method adds to cart current item"""
        self.__is_product_page()
        self.add_to_cart_button.click()


    def navigate_to_item_by_id(self, item_id: int):
        """Navigates to items page by its ID"""
        self.page.goto(f'https://demoblaze.com/prod.html?idp_={item_id}')


    def __is_product_page(self):
        """Verify if we are on the product page"""
        if not re.compile(r'.*\?idp_=[0-9]+').fullmatch(self.page.url):
            raise ValueError('Page is not a product page')
