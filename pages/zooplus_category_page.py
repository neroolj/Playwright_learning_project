"""Page object for the Zooplus dog dry-food category listing."""

import re
from typing import List, Optional

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError, expect


class ZooplusDryFoodCategoryPage:
    """Interact with and read the Zooplus dog dry-food category page."""

    URL = "https://www.zooplus.se/shop/hund/hundmat_torrfoder"
    PRODUCT_LINK_SELECTOR = 'main a[href*="/shop/hund/hundmat_torrfoder/"]:has(h2)'
    # This shared design-system class distinguishes active item amounts from
    # reference prices and per-unit prices in the observed product cards.
    ITEM_PRICE_SELECTOR = 'span[class*="z-product-price__amount"]'

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Hundfoder: torrfoder för hundar", level=1)
        self.result_summary = page.locator('[data-zta="total-products-count-desktop"]')
        self.product_links = page.locator(self.PRODUCT_LINK_SELECTOR)
        self.pagination = page.get_by_role("navigation", name=re.compile("Sida"))

    def open(self) -> None:
        self.page.goto(self.URL)
        cookie_button = self.page.get_by_role("button", name="Endast nödvändiga kakor")
        try:
            # The consent dialog is injected after navigation; waiting avoids
            # racing its appearance while still allowing an existing consent.
            cookie_button.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            pass
        else:
            cookie_button.click()
        expect(self.heading).to_be_visible()

    def filter_button(self, name: str) -> Locator:
        button = self.page.get_by_role("button", name=name, exact=True)
        if button.get_attribute("aria-expanded") != "true":
            button.click()
        return button

    @staticmethod
    def product_card(product_link: Locator) -> Locator:
        """Find the nearest product card containing its add-to-cart control."""
        return product_link.locator(
            "xpath=ancestor::div[.//button[contains(., 'Lägg till i varukorg')]][1]"
        )

    def product_card_text(self, product_link: Locator) -> str:
        return self.product_card(product_link).inner_text()

    def product_price(self, product_link: Locator) -> float:
        """Read the active listing amount, not a reference or per-unit price."""
        amount = self.product_card(product_link).locator(self.ITEM_PRICE_SELECTOR).first.inner_text()
        match = re.search(r"(\d[\d\s]*,\d{2})\s*kr", amount)
        if not match:
            raise AssertionError(f"No active product price found: {amount!r}")
        normalized_price = re.sub(r"\s+", "", match.group(1)).replace(",", ".")
        return float(normalized_price)

    def product_prices(self, limit: Optional[int] = None, exclude_free: bool = False) -> List[float]:
        """Return visible item prices, optionally skipping free sample listings."""
        prices = []
        for index in range(self.product_links.count()):
            price = self.product_price(self.product_links.nth(index))
            if not exclude_free or price > 0:
                prices.append(price)
                if limit is not None and len(prices) >= limit:
                    break
        return prices



# <div data-zta="selectMenuProxySelect" class="z-text-input z-select z-form-field-proxy__container"
# aria-disabled="false">
# <button id="uic_id-_R_4n3qb5lj9slubtb___trigger" aria-haspopup="listbox"
# aria-controls="uic_id-_R_4n3qb5lj9slubtb_" aria-expanded="false"
# class="z-dropdown-menu__trigger" data-zta="selectMenuTriggerButton" type="button">
# Toppsäljare</button></div>