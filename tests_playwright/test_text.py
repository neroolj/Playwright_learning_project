from playwright.sync_api import Page, expect
import allure


@allure.epic("Basic examples")
def test_get_test(page: Page) -> None:
    """Example of usage 'get_text' method"""
    page.goto('https://inzhenerka.tech/playwright_stand')
    text = page.locator('.tn-atom__button-text').nth(0).text_content()
    assert text == "Выбрать курс"

@allure.epic("Basic examples")
def test_contain_text(page: Page) -> None:
    """Example of usage 'to_contain_text' method"""
    page.goto('https://dev.topklik.online/')
    e = page.locator('h2')
    expect(e).to_contain_text('Войдите в личный кабинет')