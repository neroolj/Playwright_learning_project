"""This file contains examples of usage API mocking fixtures"""

import allure
import os
from playwright.sync_api import expect, Page


@allure.epic("Mock API fixture examples")
@allure.severity(allure.severity_level.TRIVIAL)
def test_mocked_product_data(zooplus_homepage, modify_backend_response):
    """Example of usage of 'modify_backend_response' fixture"""

    def change_product_data(data):
        """This function modifies data from response"""

        # modify product name, rating, and count of reviews.
        product = data[0]['recommendations'][0]
        product['product']['name'] = 'This is a long name for test purpose.'
        product['product']['feedbackAggregate']['rating'] = 5.1
        product['product']['feedbackAggregate']['reviewCount'] = 10000000000

        # modify discount
        discount = product['articleOffers'][0]['discount']
        discount['label'] = '1%'
        discount['value'] = 1.0

        # modify price
        price = product['articleOffers'][2]['price']
        price['value'] = 99999.99
        price['label'] = '99999.99 kr'
        price['labelFull'] = '99999.99 kr'

        # modify unit price
        unit_price = product['articleOffers'][2]['unitPrice']
        unit_price['value'] = 4999.99
        unit_price['label'] = '4999.99 kr'
        unit_price['labelFull'] = '4999.99 kr'

    with allure.step('Start mock watcher for API **recommendations**'):
        # use 'modify_backend_response' fixture to subscribe on recommendation API
        # once API is executed this fixture will take control on it and apply 'change_product_data' function
        modify_backend_response(zooplus_homepage, '**recommendations**', change_product_data)

    with allure.step('Go to page to trigger API'):
        zooplus_homepage.goto('https://www.zooplus.se/shop/hund/hundmat_torrfoder?filters=brand%3D4vets')
        # wait one second to let the page render data
        zooplus_homepage.wait_for_timeout(1000)

    # locate modified product on the page and take screenshot to verify how data modification is applied
    with allure.step('Locate modified product listing and save screenshot'):
        product = zooplus_homepage.locator(".RecommendationSliderV2_slider__RAoX2").first.locator('.z-carousel-slide-wrap').first
        product.screenshot(path='screenshots/changed_product_example.png')
    with allure.step('Make sure that screenshot was saved correctly'):
        assert os.path.exists('screenshots/changed_product_example.png')


@allure.epic("Mock API fixture examples")
@allure.severity(allure.severity_level.TRIVIAL)
def test_503_api_response(auth_page_zooplus, mock_backend_error):
    """Example of usage 'mock_backend_error' fixture"""

    with allure.step('Start mock watcher for API **recommendations**'):
        # Intercept the API call and return a mock response
        mock_backend_error(auth_page_zooplus, '**recommendations**', 503)
    with allure.step('Go to homepage to trigger API'):
        auth_page_zooplus.goto("https://www.zooplus.se/")
    with allure.step('Check that recommendations are not loaded as API returned 503 error'):
        expect(auth_page_zooplus.locator('.RecommendationSliderV2_slider__RAoX2')).to_have_count(0)


@allure.epic('Mock API fixture examples')
@allure.severity(allure.severity_level.TRIVIAL)
def test_500_api_response(auth_page_zooplus, mock_backend_error):
    """One more xample of usage 'mock_backend_error' fixture"""
    with allure.step('Start mock watcher for API **/customer/balance**'):
        mock_backend_error(auth_page_zooplus, '**/customer/balance', 500)
    with allure.step('Go to homepage to trigger API'):
        auth_page_zooplus.goto("https://www.zooplus.se/")
    with allure.step('Check that customer balance is not loaded'):
        bonus = auth_page_zooplus.get_by_test_id('balance-points-header-component')
        expect(bonus).to_have_count(0)


@allure.epic("Mock API fixture examples")
@allure.severity(allure.severity_level.TRIVIAL)
def test_bonus_widget_delay(auth_page_zooplus, emulate_backend_delay):
    """Example of usage 'emulate_backend_delay' fixture"""
    with allure.step('Start mock watcher for API that shows customer balance'):
        emulate_backend_delay(auth_page_zooplus, '**/customer/balance', 3000)
    with allure.step('Go to the page to trigger API'):
        auth_page_zooplus.goto("https://www.zooplus.se/account/overview")
    with allure.step('Check that right after opening the page bonus widget is not visible'):
        expect(auth_page_zooplus.get_by_test_id('balance-points-header-component')).to_have_count(0)
    with allure.step('Wait 6 seconds and check that element has appeared'):
        auth_page_zooplus.wait_for_timeout(6000)
        expect(auth_page_zooplus.get_by_test_id('balance-points-header-component')).to_have_count(2)


@allure.epic("Mock API fixture examples")
@allure.severity(allure.severity_level.TRIVIAL)
def test_product_list_delay(page: Page, emulate_backend_delay):
    """One more example of usage 'emulate_backend_delay' fixture"""
    with allure.step('Start mock watcher for API that loads list of products'):
        emulate_backend_delay(page, 'https://api.demoblaze.com/entries', 3000)
    with allure.step('Go to the page to trigger API'):
        page.goto('https://demoblaze.com/')
    with allure.step('Make sure that products are not shown right after opening the page'):
        expect(page.locator('.card-block')).to_have_count(0)
    with allure.step('Wait 6 seconds and check that products appeared'):
        page.wait_for_timeout(6000)
        expect(page.locator('.card-block')).to_have_count(9)
