from pages.product_page import ProductPage
from playwright.sync_api import Page, expect
import pytest
from dotenv import load_dotenv
import os

load_dotenv()
user_name = os.getenv('DEMOBLAZE_USER')

def add_to_cart_dialog(dialog):
    assert dialog.message == 'Product added'
    dialog.accept()


def test_add_product_to_cart(page: Page, product_page: ProductPage) -> None:
    product_page.navigate_to_item_by_id(1)
    page.on('dialog', add_to_cart_dialog)
    product_page.add_to_cart()

@pytest.mark.parametrize('item_id', [1, 2, 3, 4, 5])
def test_add_several_products_to_cart(page: Page, product_page: ProductPage, item_id) -> None:
    product_page.navigate_to_item_by_id(item_id)
    page.on('dialog', add_to_cart_dialog)
    product_page.add_to_cart()

def test_username(auth_page_test: Page) -> None:
    name = auth_page_test.locator('#nameofuser')
    expect(name).to_have_text(f'Welcome {user_name}')