from playwright.sync_api import Page, expect


def test_page_url(page: Page) -> None:
    page.goto("http://dev.topklik.online/")
    expect(page).to_have_url("https://dev.topklik.online/")

def test_page_title(page: Page) -> None:
    page.goto('http://dev.topklik.online/')
    expect(page).to_have_title('ТопКлик')