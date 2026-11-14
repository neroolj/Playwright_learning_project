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


@allure.epic('Zooplus')
@allure.feature('Zooplus login page')
@allure.severity(allure.severity_level.BLOCKER)
def test_navigation_between_tabs(zooplus_opened_loginpage) -> None:
    """Verify that user can switch to register tab and back to log in tab"""
    page = zooplus_opened_loginpage
    with allure.step('Switch to register tab'):
        page.register_tab.click()
    with allure.step('Verify that register tab is opened'):
        expect(page.register_tab).to_have_attribute('class', 'tab-item-active')
    with allure.step('Switch back to login tab'):
        page.login_tab.click()
    with allure.step('Verify that login tab is opened'):
        expect(page.login_tab).to_have_attribute('class', 'tab-item-active')


@allure.epic('Zooplus')
@allure.feature('Zooplus login page')
@allure.severity(allure.severity_level.BLOCKER)
def test_important_elements_on_login_tab(zooplus_opened_loginpage) -> None:
    """Verify that important elements are displayed on login tab"""
    page = zooplus_opened_loginpage
    with allure.step('Verify that important elements are displayed on login tab'):
        expect(page.header).to_have_text('Existerande kund')
        expect(page.email_field).to_be_visible()
        expect(page.pass_field).to_be_visible()
        expect(page.login_button).to_be_visible()
        expect(page.forgot_pass).to_be_visible()


@allure.epic('Zooplus')
@allure.feature('Zooplus login page')
@allure.severity(allure.severity_level.BLOCKER)
def test_important_elements_on_register_tab(zooplus_opened_loginpage) -> None:
    """Verify that important elements are displayed on register tab"""
    page = zooplus_opened_loginpage
    with allure.step('Switch to register tab'):
        page.register_tab.click()
    with allure.step('Verify that important elements are displayed on register tab'):
        expect(page.header).to_have_text('Ny kund')
        expect(page.name_field).to_be_visible()
        expect(page.surname_field).to_be_visible()
        expect(page.email_field).to_be_visible()
        expect(page.pass_field).to_be_visible()
        expect(page.register_button).to_be_visible()


@allure.epic('Zooplus')
@allure.feature('Zooplus login page')
@allure.severity(allure.severity_level.CRITICAL)
def test_forgot_pass_button(zooplus_opened_loginpage) -> None:
    """Verify that [Forgot password] redirects to password restore page"""
    page = zooplus_opened_loginpage
    with allure.step('Click on forgot password button'):
        page.forgot_pass.click()
    with allure.step('Verify redirection'):
        page.verify_url('/login-actions/reset-credentials')