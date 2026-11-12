import allure
from playwright.sync_api import expect


@allure.epic('Zooplus testing')
@allure.feature("Zooplus API testing")
@allure.severity(allure.severity_level.TRIVIAL)
def test_503_api_response(auth_page_zooplus, mock_backend_error):
    """Verify 503 API response code is handled correctly"""
    #Intercept the API call and return a mock response
    with allure.step('Start mock watcher for API **recommendations**'):
        mock_backend_error(auth_page_zooplus, '**recommendations**', 503)
    # go to page to trigger api
    with allure.step('Go to homepage to trigger API'):
        auth_page_zooplus.goto("https://www.zooplus.se/")
    with allure.step('Check that recoomendations are not loaded'):
        expect(auth_page_zooplus.locator('.RecommendationSliderV2_slider__RAoX2')).to_have_count(0)


@allure.epic('Zooplus testing')
@allure.feature("Zooplus API testing")
@allure.severity(allure.severity_level.TRIVIAL)
def test_500_api_response(auth_page_zooplus, mock_backend_error):
    """Verify 500 API response code is handled correctly"""
    with allure.step('Start mock watcher for API **/customer/balance**'):
        mock_backend_error(auth_page_zooplus, '**/customer/balance', 500)
    with allure.step('Go to homepage to trigger API'):
        auth_page_zooplus.goto("https://www.zooplus.se/")
    with allure.step('Check that customer balance is not loaded'):
        bonus = auth_page_zooplus.get_by_test_id('balance-points-header-component')
        expect(bonus).to_have_count(0)