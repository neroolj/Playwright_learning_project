from playwright.sync_api import Page, expect
import re

def test_my_account(auth_page_zooplus: Page) -> None:
    """Testing view of my account."""
    auth_page_zooplus.goto('https://www.zooplus.se/')
    bonus = auth_page_zooplus.get_by_test_id('balance-points-header-component').first
    print('\nElements in bonus:', bonus.count())
    print('Bonus inner text', bonus.all_inner_texts())
    print('\nBonus inner HTML\n', bonus.inner_html())
    print('\nVisible?:', bonus.is_visible(), '\nEnabled?:', bonus.is_enabled())

    link = bonus.get_by_role('link')
    expect(link).to_have_attribute('aria-disabled', 'false')
