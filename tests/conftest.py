"""Shader fixtures for all tests"""

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

        return True if diff_percent <= 100 - percentage else False
    return _compare