import re
from playwright.sync_api import expect, Page


def test_default_button_state(page: Page) -> None:
    """Test default state of button"""
    page.goto('http://uitestingplayground.com/click')
    button = page.locator("#badButton")
    expect(button).to_have_class(re.compile(r".*primary"))


def test_click(page: Page) -> None:
    """Test changing state after click"""
    # go to specified page
    page.goto('http://uitestingplayground.com/click')
    # find element with id="badButton"
    button = page.locator("#badButton")
    # click on the button
    button.click()
    # check if class corresponds to specified regexp
    expect(button).to_have_class(re.compile(r".*success"))

def test_checkbox_and_radio(page):
    """To be added"""
    # go to page
    page.goto('https://jqueryui.com/resources/demos/checkboxradio/default.html')
    # locate elements by 'for' attribute: "[attr_name=]"
    radio_1 = page.locator("[for=radio-1]")
    checkbox_4 = page.locator("[for=checkbox-4]")
    checkbox_nested_3 = page.locator("[for=checkbox-nested-3]")
    checkbox_nested_4 = page.locator("[for=checkbox-nested-4]")
    # click on located elements
    radio_1.click()
    # radio_1.click(button="right", modifiers=["Shift"], position={"x": 23, "y": 32})

    checkbox_4.click()
    checkbox_nested_3.click()
    checkbox_nested_4.click()
    # check that status (inside the class is changed to 'checked'
    expect(radio_1).to_have_class(re.compile(r"checked"))
    expect(checkbox_4).to_have_class(re.compile(r"checked"))
    expect(checkbox_nested_3).to_have_class(re.compile(r"checked"))
    expect(checkbox_nested_4).to_have_class(re.compile(r"checked"))