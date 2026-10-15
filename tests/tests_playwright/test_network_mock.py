import allure
from playwright.sync_api import Page, expect


@allure.epic("Basic examples")
def test_mock_api_response(auth_page_zooplus, mock_backend_error):
    """Testing example of mock API response
    """
    #Intercept the API call and return a mock response
    mock_backend_error(auth_page_zooplus, '**/customer/balance', 500)
    mock_backend_error(auth_page_zooplus, '**recommendations**', 503)
    auth_page_zooplus.goto("https://www.zooplus.se/")
    expect(auth_page_zooplus.locator('.RecommendationSliderV2_slider__RAoX2')).to_have_count(0)
