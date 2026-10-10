from playwright.sync_api import Browser, sync_playwright, expect
from dotenv import load_dotenv
import os

load_dotenv()
TEST_USER = os.getenv('TEST_USER')
TEST_PASS = os.getenv('TEST_PASS')

def generate_test_auth_data(browser: Browser) -> None:
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://demoblaze.com/')
    page.get_by_role("link", name="Log in").click()
    page.locator('#loginusername').fill(TEST_USER)
    page.locator('#loginpassword').fill(TEST_PASS)
    page.get_by_role("button", name="Log in").click()
    name = page.locator("#nameofuser")
    expect(name).to_have_text(f"Welcome {TEST_USER}")
    context.storage_state(path='test_state.json')
    context.close()

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        generate_test_auth_data(browser)
        browser.close()

if __name__ == "__main__":
    main()