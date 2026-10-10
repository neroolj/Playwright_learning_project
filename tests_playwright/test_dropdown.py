from playwright.sync_api import Page, expect
import re


def test_dropdown(page: Page) -> None:
    """Example of using .select_option() method"""
    page.goto('https://the-internet.herokuapp.com/dropdown')
    selector = page.locator('#dropdown')
    options = page.get_by_text(re.compile(r'Option.[1-2]'))
    expect(options.first).not_to_have_attribute('selected')
    expect(options.last).not_to_have_attribute('selected')
    selector.select_option('Option 1')
    expect(options.first).to_have_attribute('selected', 'selected')

    page.locator("#dropdown").select_option("2")
    expect(page.locator("#dropdown")).to_have_value("2")