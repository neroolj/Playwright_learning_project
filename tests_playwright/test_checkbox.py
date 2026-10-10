from playwright.sync_api import Page, expect


def test_checkbox(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    # Find all <input> elements inside "checkboxes"
    form = page.locator("#checkboxes input")
    # Link two checkboxes to separate variables
    cb1 = form.nth(0)
    cb2 = form.nth(1)
    # Check first and uncheck second
    cb1.check()
    cb2.uncheck()
    print(page.viewport_size)
    print(page.evaluate("navigator.userAgent"))
    # Verify that checkboxes are in the right state
    expect(cb1).to_be_checked()
    expect(cb2).not_to_be_checked()