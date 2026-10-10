import pytest
from playwright.sync_api import Page, expect

def test_mock_api_response(page: Page):
    #Intercept the API call and return a mock response
    page.route("https://www.zooplus.se/protected/api/loyalty-management/bonus-points/customer/balance", lambda route: route.fulfill(
        status=404,
        content_type="application/json",
        body='{"users": [{"name": "Test User"}]}'))
    page.goto("https://www.zooplus.se/")
    page.get_by_role(role='button', name='Endast nödvändiga kakor').click()
    drop_down = page.locator('#srh-account').first
    drop_down.hover()
    expect(drop_down).to_have_attribute('aria-expanded', 'true')
    page.get_by_role("menuitem", name="Mitt zooplus").click()
    expect(page.locator('#tab-navigation').get_by_text("Logga in")).to_have_text('Logga in')
    page.locator('#username').fill('neroolj@gmail.com')
    page.locator('#password').fill('Ythjpmrf536539')
    page.get_by_role('button', name='*Logga in*').click()
    page.screenshot(path='screenshot.png')