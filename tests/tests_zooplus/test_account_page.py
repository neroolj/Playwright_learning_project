from playwright.sync_api import Page, expect
import allure

@allure.epic('Zooplus testing')
@allure.severity(allure.severity_level.BLOCKER)
def test_my_account(auth_page_zooplus: Page) -> None:
    """Testing view of my account."""
    with allure.step('Go to my account page'):
        auth_page_zooplus.goto('https://www.zooplus.se/account/overview')

    with allure.step('Check that bonus balance is shown'):
        bonus = auth_page_zooplus.get_by_test_id('balance-points-header-component').first
        link = bonus.get_by_role('link')
        expect(link).to_have_attribute('aria-disabled', 'false')

    with allure.step('Check that greeting is displayed with username in it'):
        expect(auth_page_zooplus.get_by_text('Hej')).to_have_text('Hej Oleh')

    with allure.step('Check that log out link is displayed'):
        link = auth_page_zooplus.get_by_role("link", name="Logga ut")
        expect(link).to_have_attribute('aria-disabled', 'false')
