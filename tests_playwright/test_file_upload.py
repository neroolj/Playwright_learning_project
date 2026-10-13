from playwright.sync_api import Page, expect
import allure


@allure.epic("Basic examples")
def test_one_file_upload(page) -> Page:
    page.goto('https://the-internet.herokuapp.com/upload')
    screenshot_path = "test-results/screenshots/files_before.png"
    page.screenshot(path=screenshot_path)

    page.locator('#file-upload').set_input_files(screenshot_path)
    page.locator('#file-submit').click()
    page.screenshot(path="test-results/screenshots/files_after.png")
    expect(page.locator('h3')).to_have_text('File Uploaded!')
