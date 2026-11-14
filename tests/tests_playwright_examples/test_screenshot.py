import os.path
import pytest
from playwright.sync_api import Page
import allure


screenshots_dir = 'screenshots/'


@allure.epic("Basic examples")
@allure.feature("Screenshots")
def test_screenshot(page: Page):
    """Example of saving screenshots."""
    with allure.step('Open page'):
        page.goto('http://uitestingplayground.com/sampleapp')

    with allure.step('Save full page screenshot'):
        page.screenshot(path=f"{screenshots_dir}body.png")

    with allure.step('Locate additional elements'):
        login_form, last = page.locator(".container").first, page.locator('.container').last

    with allure.step('Save element screenshot'):
        last.screenshot(path=f"{screenshots_dir}last.png")

    with allure.step('Save element screenshot with masked elements'):
        login_form.screenshot(path=f"{screenshots_dir}container.jpeg", type='jpeg', quality=75,
                          mask=[page.get_by_placeholder('User Name'), page.get_by_placeholder('********')])

    with allure.step('Verify that all files are saved'):
        assert os.path.exists(f"{screenshots_dir}container.jpeg")
        assert os.path.exists(f"{screenshots_dir}body.png")
        assert os.path.exists(f"{screenshots_dir}last.png")


@pytest.mark.visual
@allure.epic("Basic examples")
@allure.feature("Screenshots")
def test_homepage_visual(page: Page, request, compare_images):
    """Example of comparing full page with etalon screenshot."""
    # defining base constants
    etalon_path = f'{screenshots_dir}demoblaze/full_homepage.png'
    current_path = f'{screenshots_dir}demoblaze/full_homepage_current.png'
    gen_mode = request.config.getoption("--gen-screenshots")

    with allure.step('Open page and wait till it is fully loaded'):
        page.goto("https://demoblaze.com/")
        # waiting for page to be fully loaded
        page.wait_for_timeout(2000)

    if gen_mode:
        # Pytest started with --gen-screenshots CLI

        with allure.step('Update etalon screenshot'):
            page.screenshot(path=etalon_path, full_page=True)
            pytest.skip("Test run is in screenshot generation mode")
    else:
        # Pytest started in normal testing mode
        with allure.step('Compare current page screenshot with etalon'):
            if not os.path.exists(etalon_path):
                pytest.fail('Etalon screenshot does not exist. Run pytest with --gen-screenshots option')
            page.screenshot(path=current_path, full_page=True)

            assert compare_images(etalon_path, current_path) is True, "Visual discrepancies detected"


@pytest.mark.visual
@allure.epic("Basic examples")
@allure.feature("Screenshots")
@pytest.mark.parametrize('img_name, locator',
                         [('nav_menu', '#navbarExample'),
                          ('title', '#nava'),
                          ('bottom_info', '#fotcont')])
def test_top_navigation_visual(page: Page, request, compare_images, img_name, locator):
    """Example of comparing one element from the page with etalon screenshot."""
    # defining base constants
    etalon_path = f'{screenshots_dir}demoblaze/{img_name}.png'
    current_path = f'{screenshots_dir}demoblaze/{img_name}_current.png'
    gen_mode = request.config.getoption('--gen-screenshots')

    with allure.step('Open page and find element'):
        page.goto('https://demoblaze.com/')
        element = page.locator(locator)
        # wait 2 seconds to let the page load all images
        page.wait_for_timeout(2000)

    if gen_mode:
        with allure.step('Update etalon screenshot'):
            element.screenshot(path=etalon_path)
            pytest.skip('Test run is in screenshot generation mode')
    else:
        with allure.step('Compare screenshot of current element with etalon'):
            if not os.path.exists(etalon_path):
                pytest.fail('Etalon screenshot does not exist. Run pytest with --gen-screenshots option')
            element.screenshot(path=current_path)

            assert compare_images(etalon_path, current_path, 98)