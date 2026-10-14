import allure
from playwright.sync_api import Page, expect

@allure.epic('Zooplus testing')
@allure.severity(allure.severity_level.NORMAL)
def test_empty_cart(page: Page) -> None:
    with allure.step('Go to home page'):
        page.goto('https://www.zooplus.se/')
        page.get_by_role("button", name="Endast nödvändiga kakor").click()
    with allure.step('Click on shopping cart button'):
        page.locator('#header-cart-nav-anchor').click()
        #page.get_by_role("link", name="Varukorg").click()
    with allure.step('Check empty cart page'):
        expect(page.get_by_role("heading", name="Varukorgen är tom")).to_be_visible()
        expect(page.get_by_text("Lägg till något i varukorgen!")).to_be_visible()
        expect(page.get_by_test_id("empty-box")).to_be_visible()
        expect(page.get_by_test_id('continue-shopping-btn')).to_be_visible()
    with allure.step('Click on continue shopping button moves to homepage'):
        page.get_by_test_id("continue-shopping-btn").click()
        expect(page).to_have_url("https://www.zooplus.se/")


@allure.epic('Zooplus testing')
@allure.severity(allure.severity_level.BLOCKER)
def test_add_item_to_cart(page: Page) -> None:
    """Testing adding item to cart"""
    with allure.step('Go to home page'):
        page.goto('https://www.zooplus.se/')
        page.get_by_role("button", name="Endast nödvändiga kakor").click()
    with allure.step('Select first item from suggestions'):
        # select first item from recommendations
        recommendations = page.locator('.RecommendationSliderV2_slider__RAoX2').first
        recommendations.locator('.z-carousel-slide-wrap-inner').first.click()
        # save item name and price to use it later in cart tests
        item_name = page.locator('[data-zta=ProductTitle__Title]').inner_text()
        item_price = page.locator('.z-product-price__amount').first.inner_text()
    with allure.step('Add item to cart'):
        # Check that API request is sent and accepted by backend (status 200)
        with page.expect_response("**checkout/api/cart-api/v2/cart/**/set-article-quantity-command") as response_info:
            page.get_by_text("Lägg till i varukorgLägg till").click()
            response = response_info.value
            assert response.status == 200
    with allure.step('Go to cart page'):
        page.get_by_role("link", name="Gå till varukorgen").click()
    with allure.step('Check that right item is in the cart'):
        expect(page.get_by_test_id('product-name')).to_have_text(item_name)
        expect(page.get_by_test_id('overview-sub-total-value')).to_have_text(item_price)




