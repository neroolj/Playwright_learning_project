"""Shared fixtures for all tests"""

import pytest
from playwright.sync_api import Page
from PIL import Image, ImageChops



@pytest.fixture()
def mock_backend_error():
    """Fixture captures API requests and mocks response with specific error code"""
    # list of supported codes
    error_codes = {400: 'Bad request',
                   401: 'Unauthorized',
                   403: 'Forbidden',
                   404: 'Page not found',
                   500: 'Internal server error',
                   503: 'Service unavailable',
                   504: 'Gateway timeout',}
    # nested function where response replacement is implemented
    def _mock(page: Page, api: str, status_code: int):
        page.route(api, lambda route: route.fulfill(
            status=status_code,
            json={"errorMessage": error_codes.get(status_code, 'Unknown error')})
                   )
    return _mock


@pytest.fixture()
def modify_backend_response():
    """Fixture catches real response from backend and modifies it before sending to client"""

    def _mock(page: Page, api: str, modifier_function):
        """Nested function which fetches response, modifies it with provided modifier_function,
        and then sends it to client"""
        def handle_route(route):
            """Handler for route() call"""
            # 1. Perform request and catch response
            response = route.fetch()
            # 2. Try to parse response's json
            try:
                json_data = response.json()
            except Exception:
                # 3.1 If parsing failed send response to client without any modifications and stop handler execution
                print('Could not parse response by built-in .json() method')
                route.continue_()
                return
            # 3.2 If parsing succeeded apply modifier function to it.
            modifier_function(json_data)

            # 4. Send response to client with modified data
            route.fulfill(response=response, json=json_data)

        page.route(api, handle_route)
    return _mock


@pytest.fixture()
def compare_images():
    """Fixture compares two images with specified accuracy"""

    def _compare(img1_path, img2_path, percentage:float|int=95.0) -> bool:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        if img1.size != img2.size:
            raise AssertionError(f"Images have different size: Etalon: {img1.size} vs Current: {img2.size}")

        diff = ImageChops.difference(img1, img2)
        histogram = diff.convert("L").histogram()

        # histogram[0] contains fully matched pixels, so we use this value
        total_pixels = img1.width * img1.height
        identical_pixels = histogram[0]
        diff_pixels = total_pixels - identical_pixels

        diff_percent = (diff_pixels / total_pixels) * 100

        return diff_percent <= (100 - percentage)
    return _compare