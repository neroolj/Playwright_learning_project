from playwright.sync_api import Page, expect


def test_hover(page: Page) -> None:
    """Example of using .hover() method"""
    page.goto("https://the-internet.herokuapp.com/hovers")
    figure = page.locator(".figure").nth(1)
    figure.hover()
    caption = figure.locator(".figcaption h5")
    expect(caption).to_be_visible()
