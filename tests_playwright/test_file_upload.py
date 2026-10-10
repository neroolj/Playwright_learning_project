from playwright.sync_api import Page, expect

def test_one_file_upload(page) -> Page:
    page.goto('https://the-internet.herokuapp.com/upload')
    screenshot_path = "screenshots/files.png"
    page.screenshot(path=screenshot_path)

    page.locator('#file-upload').set_input_files(screenshot_path)
    page.locator('#file-submit').click()
    page.screenshot(path="screenshots/files.png")
    expect(page.locator('h3')).to_have_text('File Uploaded!')
