import pytest
import allure
from playwright.sync_api import expect

@allure.epic('Zooplus')
@allure.feature('Zooplus login page')
@allure.severity(allure.severity_level.CRITICAL)
def test_login_tab_opens_by_default(zooplus_loginpage_pom, zooplus_homepage_pom) -> None:
    """Verify that login tab opens by default when navigating from home page"""
    homepage = zooplus_homepage_pom
    page = zooplus_loginpage_pom
    with allure.step('Open login page'):
        page.open(homepage)
    with allure.step('Verify that login tab is opened'):
        expect(page.login_tab).to_have_attribute('class', 'tab-item-active')
        expect(page.register_tab).to_have_attribute('class', 'tab-item')



