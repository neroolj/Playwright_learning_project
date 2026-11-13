from playwright.sync_api import Page, expect
import allure
import dotenv
import os

dotenv.load_dotenv()
login = os.getenv("ZOOPLUS_USERNAME")
password = os.getenv("ZOOPLUS_PASSWORD")
if type(login) != str or type(password) != str:
    raise TypeError("Login or password are not loaded from .env file")


@allure.epic('Zooplus')
@allure.severity(allure.severity_level.CRITICAL)
def test_bonuses_widget_is_visible(zooplus_homepage_pom):
    """Bonuses element is visible on homepage"""
    page = zooplus_homepage_pom
    with allure.step('Navigate to homepage'):
        page.open()
    with allure.step('Check if bonuses widget is shown on homepage'):
        expect(page.bonus_balance).to_be_visible()


@allure.epic('Zooplus')
@allure.severity(allure.severity_level.CRITICAL)
def test_login_flow(zooplus_loginpage_pom, zooplus_homepage_pom):
    """Testing login flow with correct credentials"""
    homepage = zooplus_homepage_pom
    page = zooplus_loginpage_pom
    with allure.step("Navigate to login page"):
        page.open_login_page(homepage)
    with allure.step("Login"):
        page.login(login, password)
    with allure.step("Check URL redirection"):
        page.check_url_redirection()