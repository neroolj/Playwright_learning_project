import pytest
from playwright.sync_api import Page, expect
import allure


@allure.epic("Basic examples")
@pytest.mark.parametrize('login, password, result',
                         [('User1', 'pwd', 'Welcome, User1!'),
                          ('User2', 'dpw', 'Invalid username/password')]
                         )
def test_auth(page: Page, login: str, password: str, result: str) -> None:
    """Testing authentication example
    plus example of usage .fill() method"""
    page.goto('http://uitestingplayground.com/sampleapp')
    # locate needed elements
    login_field = page.get_by_placeholder('User Name')
    password_field = page.get_by_placeholder('********')
    button = page.locator("#login")
    status = page.locator('#loginstatus')
    #fill in login and pass
    login_field.fill(login)
    password_field.fill(password)
    # press login button
    button.click()
    # verify result of authentification
    expect(status).to_have_text(result)


@allure.epic("Basic examples")
@pytest.mark.parametrize('device',
                         ['iPhone 17 Pro landscape',
                          'Pixel 10 Pro XL',
                          'Pixel 8'])
def test_copy_paste(device: str, browser, playwright) -> None:
    """Testing copy-paste on different devices"""
    # getting device configuration
    current_device = playwright.devices[device]

    # creating new context with device configuration
    context = browser.new_context(**current_device)
    page = context.new_page()

    # test body
    page.goto('http://uitestingplayground.com/textinput')
    input_field = page.locator("#newButtonName")
    input_field.fill("Abc")
    input_field.press('Meta+A')
    input_field.press('Meta+X')
    for a in range(3):
        input_field.press('Meta+V')
    button = page.locator("#updatingButton")
    button.click()
    expect(button).to_have_text("AbcAbcAbc")
    # closing context after testing each configuration
    context.close()