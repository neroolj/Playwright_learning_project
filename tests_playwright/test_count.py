from playwright.sync_api import Page, expect
import pytest

def url(c: int) -> str:
    return f"https://www.ebay.com/sch/i.html?_nkw=nike&_ipg={c}"


@pytest.mark.skip(reason='Work normally only in headed mode')
def test_check_elements_count(page: Page):
    # Первая проверка для 120 элементов
    page.goto(url(120))
    expect(page.locator("li.su-media-carousel")).to_have_count(120)

    # Вторая проверка для 240 элементов
    page.goto(url(240))
    expect(page.locator("li.su-media-carousel")).to_have_count(240)

def test_count2(page: Page) -> None:
    login = 'tester@inzhenerka.tech'
    password = 'LetsTest!'

    page.goto('https://dev.topklik.online/')
    page.get_by_placeholder('логин').fill(login)
    page.get_by_placeholder('пароль').fill(password)
    page.get_by_text('Войти').click()
    page.screenshot(path="screenshots/count2.png")
    expect(page.locator('[data-testid="product-item"]')).to_have_count(2)
