from playwright.sync_api import Page, expect
import allure


@allure.epic("Basic examples")
def test_page_url(page: Page) -> None:
    page.goto("http://dev.topklik.online/")
    expect(page).to_have_url("https://dev.topklik.online/")

@allure.epic("Basic examples")
def test_page_title(page: Page) -> None:
    page.goto('http://dev.topklik.online/')
    expect(page).to_have_title('ТопКлик')