from playwright.sync_api import Page, expect
import re

def test_my_account(auth_page_zooplus: Page) -> None:
    """Testing view of my account."""
    auth_page_zooplus.goto('https://www.zooplus.se/')
    bonus = auth_page_zooplus.get_by_test_id('balance-points-header-component').first
    link = bonus.get_by_role('link')
    expect(link).to_have_attribute('aria-disabled', 'false')
