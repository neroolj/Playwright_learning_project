import os.path
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip('Just an example')
def test_screenshot(page: Page):
    """Example of saving screenshots."""
    page.goto('http://uitestingplayground.com/sampleapp')
    page.screenshot(path="screenshots/body.png")
    login_form, last = page.locator(".container").first, page.locator('.container').last
    login_form.screenshot(path="screenshots/container.jpeg", type='jpeg', quality=75,
                          mask=[page.get_by_placeholder('User Name'), page.get_by_placeholder('********')])
    last.screenshot(path="screenshots/last.png")

    assert os.path.exists("screenshots/container.jpeg")
    assert os.path.exists("screenshots/body.png")
    assert os.path.exists("screenshots/last.png")


def test_homepage_visual(page: Page, assert_snapshot) -> None:
    path = 'screenshots/demoblaze/homepage.png'

    page.goto("https://demoblaze.com/")

    if not os.path.exists(path):
        page.screenshot(path=path)

    # Сравнение всего экрана с эталонным снимком
    screenshot = page.screenshot()
    assert_snapshot(screenshot, path)


def test_cart_button_visual(page: Page) -> None:
    path = 'screenshots/demoblaze/cart_button.png'

    page.goto("https://demoblaze.com/")
    cart_button = page.locator("#cartur")

    if not os.path.exists(path):
        cart_button.screenshot(path=path)
    # Сравнение конкретного элемента
    screenshot = cart_button.screenshot()
    with open(path, "r") as f:
        assert f.read() == screenshot