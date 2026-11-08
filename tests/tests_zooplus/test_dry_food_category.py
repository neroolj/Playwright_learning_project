import math
import re
from urllib.parse import urlparse

import allure
from playwright.sync_api import Page, expect
from pages.zooplus_pages import ZooplusDryFoodPage


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.CRITICAL)
def test_dry_food_category_displays_important_elements(page: Page):
    """Verify that the category page displays its key navigation and product elements."""
    category = ZooplusDryFoodCategoryPage(page)
    with allure.step("Open the dry-food category page"):
        category.open()
    with allure.step("Check the category navigation, filters, results and products"):
        expect(page).to_have_title(re.compile("Hundmat.*torrfoder", re.IGNORECASE))
        breadcrumbs = page.get_by_role("navigation", name="breadcrumbs")
        expect(breadcrumbs.get_by_role("link", name="zooplus.se")).to_be_visible()
        expect(breadcrumbs.get_by_role("link", name="Hund", exact=True)).to_be_visible()
        expect(breadcrumbs).to_contain_text("Hundfoder (torrfoder)")
        expect(page.get_by_role("searchbox", name="Sök efter produkter")).to_be_visible()
        expect(page.get_by_role("link", name="Varukorg")).to_be_visible()
        for facet in ("Märke", "Smak", "Pris"):
            expect(category.filter_button(facet)).to_be_visible()
        expect(category.result_summary).to_be_visible()
        for index in (0, 1):
            product_link = category.product_links.nth(index)
            expect(product_link).to_be_visible()
            product_title = product_link.get_by_role("heading", level=2)
            expect(product_title).to_be_visible()
            expect(product_title).to_contain_text(re.compile(r"\d+(?:[.,]\d+)?\s?(?:kg|g)\b", re.IGNORECASE))
            card = category.product_card(product_link)
            expect(card).to_contain_text(re.compile(r"\d[\d\s.,]*\s*kr"))
            rating = card.get_by_role("link", name=re.compile(r"Rating:|Not Rated", re.IGNORECASE))
            if rating.count():
                expect(rating.first).to_be_visible()
        expect(category.pagination.get_by_role("link", name="Nästa")).to_be_visible()


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_brand_filter_only_displays_products_from_selected_brand(page: Page):
    """Verify that selecting a brand limits the listing to products from that brand."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Choose an available brand from the Märke filter"):
        category.filter_button("Märke")
        old_summary = category.result_summary.inner_text()
        brand = page.get_by_role("region", name="Märke").get_by_role("checkbox").first
        brand_name = brand.get_attribute("aria-label") or brand.get_attribute("name")
        if not brand_name:
            brand_name = brand.locator("xpath=ancestor::*[@role='option'][1]").inner_text().split("(")[0].strip()
        brand.check()
        expect(brand).to_be_checked()
    with allure.step("Verify the brand selection narrows the listing to that brand"):
        expect(page).to_have_url(re.compile(r"[?&]filters=.*brand"))
        expect(page.get_by_role("button", name=re.compile(rf"delete: {re.escape(brand_name)}", re.IGNORECASE))).to_be_visible()
        expect(category.result_summary).not_to_have_text(old_summary)
        expect(category.product_links.first).to_be_visible()
        brand_slug = re.sub(r"[^a-z0-9]+", "_", brand_name.lower()).strip("_")
        for index in range(category.product_links.count()):
            link = category.product_links.nth(index)
            href = (link.get_attribute("href") or "").lower()
            assert brand_name.lower() in (link.inner_text() + " " + href).lower() or brand_slug in href
    with allure.step("Clear the selected brand filter"):
        brand.uncheck()
        expect(brand).not_to_be_checked()


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_flavor_filter_changes_the_product_listing(page: Page):
    """Verify that selecting a flavor updates the active filter and product listing."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Choose an available flavor from the Smak filter"):
        category.filter_button("Smak")
        old_summary = category.result_summary.inner_text()
        flavor = page.get_by_role("region", name="Smak").get_by_role("checkbox").first
        flavor_name = flavor.get_attribute("aria-label") or flavor.get_attribute("name")
        if not flavor_name:
            flavor_name = flavor.locator("xpath=ancestor::*[@role='option'][1]").inner_text().split("(")[0].strip()
        flavor.check()
        expect(flavor).to_be_checked()
    with allure.step("Verify the active flavor filter and updated results"):
        expect(page).to_have_url(re.compile(r"[?&]filters=.*flavour"))
        expect(page.get_by_role("button", name=re.compile(rf"delete: {re.escape(flavor_name)}", re.IGNORECASE))).to_be_visible()
        expect(category.result_summary).not_to_have_text(old_summary)
        expect(category.product_links.first).to_be_visible()
    with allure.step("Clear the selected flavor filter"):
        flavor.uncheck()
        expect(flavor).not_to_be_checked()


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_price_filter_keeps_listed_item_prices_within_range(page: Page):
    """Verify that the price filter limits listed product prices to the selected range."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Set a bounded price range based on a currently listed item"):
        category.filter_button("Pris")
        minimum = page.get_by_role("textbox", name="Lägsta pris")
        maximum = page.get_by_role("textbox", name="Högsta pris")
        starting_prices = category.product_prices(limit=1, exclude_free=True)
        assert starting_prices, "The category should contain at least one paid product"
        max_price = math.ceil(starting_prices[0])
        old_summary = category.result_summary.inner_text()
        minimum.fill("0")
        maximum.fill(str(max_price))
        expect(minimum).to_have_value("0")
        expect(maximum).to_have_value(str(max_price))
        maximum.press("Enter")
        expect(page).to_have_url(re.compile(rf"filters=current_price%3D0%3B{max_price}"))
        expect(page.get_by_role("button", name=re.compile(rf"delete: 0 till {max_price} kr"))).to_be_visible()
        expect(category.result_summary).not_to_have_text(old_summary)
    with allure.step("Check visible active item prices are within the selected range"):
        expect(category.product_links.first).to_be_visible()
        for price in category.product_prices(limit=12):
            assert 0 <= price <= max_price, f"Listed item price {price} is outside 0–{max_price} kr"
    with allure.step("Restore the default price range"):
        minimum.fill("0")
        maximum.fill("9999")


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_brand_and_price_filters_can_be_combined(page: Page):
    """Verify that brand and price filters apply together to the product listing."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Select an available brand and set a price range"):
        category.filter_button("Märke")
        old_summary = category.result_summary.inner_text()
        brand = page.get_by_role("region", name="Märke").get_by_role("checkbox").first
        brand_name = brand.get_attribute("aria-label") or brand.get_attribute("name")
        if not brand_name:
            brand_name = brand.locator("xpath=ancestor::*[@role='option'][1]").inner_text().split("(")[0].strip()
        brand.check()
        expect(brand).to_be_checked()
        expect(category.result_summary).not_to_have_text(old_summary)
        expect(category.product_links.first).to_be_visible()
        category.filter_button("Pris")
        minimum = page.get_by_role("textbox", name="Lägsta pris")
        maximum = page.get_by_role("textbox", name="Högsta pris")
        starting_prices = sorted(category.product_prices(exclude_free=True))
        assert len(starting_prices) > 1, "The selected brand should contain multiple paid products"
        old_price_filtered_summary = category.result_summary.inner_text()
        max_price = math.floor(starting_prices[(len(starting_prices) - 1) // 2])
        minimum.fill("0")
        maximum.fill(str(max_price))
        maximum.press("Enter")
        expect(maximum).to_have_value(str(max_price))
        expect(category.result_summary).not_to_have_text(old_price_filtered_summary)
    with allure.step("Confirm the resulting cards satisfy both active filters"):
        expect(brand).to_be_checked()
        expect(page.get_by_role("button", name=re.compile(rf"delete: {re.escape(brand_name)}", re.IGNORECASE))).to_be_visible()
        expect(category.product_links.first).to_be_visible()
        min_price = float(minimum.input_value())
        for index in range(category.product_links.count()):
            link = category.product_links.nth(index)
            brand_slug = re.sub(r"[^a-z0-9]+", "_", brand_name.lower()).strip("_")
            href = (link.get_attribute("href") or "").lower()
            assert brand_name.lower() in (link.inner_text() + " " + href).lower() or brand_slug in href
            price = category.product_price(link)
            assert min_price <= price <= max_price
    with allure.step("Remove the filters"):
        brand.uncheck()
        minimum.fill("0")
        maximum.fill("9999")


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.CRITICAL)
def test_products_sort_by_price_low_to_high(page: Page):
    """Verify that products are sorted from the lowest price to the highest price."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Choose Lägsta pris sorting"):
        page.get_by_role("button", name="Toppsäljare").click()
        page.get_by_role("option", name="Lägsta pris", exact=True).click()
        expect(page).to_have_url(re.compile(r"sorting=lowest-price"))
        expect(page.get_by_role("button", name="Lägsta pris", exact=True)).to_be_visible()
    with allure.step("Compare the first two paid product prices in ascending order"):
        expect(category.product_links.nth(1)).to_be_visible()
        prices = category.product_prices(limit=2, exclude_free=True)
        assert len(prices) == 2, "At least two paid product listings are required for sorting"
        assert prices[0] <= prices[1], f"Expected ascending prices, got {prices[0]} then {prices[1]}"


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.CRITICAL)
def test_products_sort_by_price_high_to_low(page: Page):
    """Verify that products are sorted from the highest price to the lowest price."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Choose Högsta pris sorting"):
        page.get_by_role("button", name="Toppsäljare").click()
        page.get_by_role("option", name="Högsta pris", exact=True).click()
        expect(page).to_have_url(re.compile(r"sorting=highest-price"))
        expect(page.get_by_role("button", name="Högsta pris", exact=True)).to_be_visible()
    with allure.step("Compare the first two paid product prices in descending order"):
        expect(category.product_links.nth(1)).to_be_visible()
        prices = category.product_prices(limit=2, exclude_free=True)
        assert len(prices) == 2, "At least two paid product listings are required for sorting"
        assert prices[0] >= prices[1], f"Expected descending prices, got {prices[0]} then {prices[1]}"


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.CRITICAL)
def test_category_pagination_moves_to_next_page_and_back(page: Page):
    """Verify that category pagination advances to the next page and returns to page one."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Record the first product and check first-page controls"):
        first_page_first_product = category.product_links.first.get_attribute("href")
        expect(category.pagination.get_by_role("button", name="Föregående")).to_be_disabled()
        next_page = category.pagination.get_by_role("link", name="Nästa")
    with allure.step("Navigate to page 2 and verify the listing changes"):
        next_page.click()
        expect(page).to_have_url(re.compile(r"[?&]p=2(?:&|$)"))
        expect(category.product_links.first).to_be_visible()
        expect(category.product_links.first).not_to_have_attribute("href", first_page_first_product)
    with allure.step("Return to the first page"):
        category.pagination.get_by_role("link", name="1", exact=True).click()
        expect(page).not_to_have_url(re.compile(r"[?&]p=2(?:&|$)"))
        expect(category.product_links.first).to_have_attribute("href", first_page_first_product)


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_product_listing_link_opens_matching_product_detail(page: Page):
    """Verify that a product listing link opens the matching product detail page."""
    category = ZooplusDryFoodCategoryPage(page)
    category.open()
    with allure.step("Open the first product detail page from the listing"):
        product_link = category.product_links.first
        product_name = product_link.get_by_role("heading", level=2).inner_text()
        product_url = product_link.get_attribute("href")
        product_link.click()
    with allure.step("Verify product detail matches the selected listing"):
        expect(page).to_have_url(re.compile(re.escape(urlparse(product_url).path)))
        heading_name = re.compile(re.escape(product_name.split("\n")[0]), re.IGNORECASE)
        expect(page.get_by_role("heading", name=heading_name).first).to_be_visible()
    with allure.step("Return to the category listing"):
        page.go_back()
        expect(category.heading).to_be_visible()


# Below will be tests rewritten by me

@allure.epic("Zooplus")
@allure.severity(allure.severity_level.CRITICAL)
def test_products_page_important_elements(zooplus_dryfoodpage_pom) -> None:
    """Verify that products page important elements are visible."""
    page = zooplus_dryfoodpage_pom
    with allure.step("Open the dry-food category page"):
        page.open()
    with allure.step('Verify page title'):
        print('TITLE = ', page.title)
        assert re.search(r'Hundmat.*torrfoder', page.title, re.IGNORECASE) is not None
    with allure.step('Verify breadcrumbs'):
        breadcrumbs = page.breadcrumbs
        expect(breadcrumbs.get_by_role("link", name="zooplus.se")).to_be_visible()
        expect(breadcrumbs.get_by_role("link", name="Hund", exact=True)).to_be_visible()
        expect(breadcrumbs).to_contain_text("Hundfoder (torrfoder)")
    with allure.step("Verify that search box is visible"):
        expect(page.searchbox).to_be_visible()
    with allure.step("Verify that the most important filters are visible"):
        for f in page.FILTERS:
            expect(page.filter_button(f)).to_be_visible()
    with allure.step("Verify that widget with product cards is visible"):
        expect(page.products_grid).to_be_visible()
    with allure.step("Verify that pagination is visible"):
        expect(page.pagination).to_be_visible()


@allure.epic("Zooplus")
@allure.severity(allure.severity_level.NORMAL)
def test_brand_filter(zooplus_dryfoodpage_pom) -> None:
    """Verify that filtering by brand works properly."""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Find filter button and expand it if needed'):
        page.filter_button('Märke')
    with allure.step('Select first brand in the list'):
        first_checkbox = page.filter_area('Märke').g.first
        brand_name = page.option_name(first_checkbox)
        print(f'\n\nBrand name = {brand_name}\n')
        first_checkbox.check()

    with allure.step('Verify that filter applied properly'):
        result = True
        for p in range(page.all_products.count()):
            name = page.product_name(page.all_products.nth(p))
            if not re.match(brand_name, name):
                result = False
        assert result


def test_brand_filter2(zooplus_dryfoodpage_pom) -> None:
    """Verify that products match the selected brand filter."""
    page = zooplus_dryfoodpage_pom
    page.open()

    # Find and expand the brand filter.
    brand_filter = page.filter_button("Märke")

    # The filter options are in the panel controlled by the button.
    panel_id = brand_filter.get_attribute("aria-controls")
    assert panel_id, "Märke filter button has no associated options panel"
    options_panel = page.page.locator(f"#{panel_id}")

    # Save the first option's name before selecting its checkbox.
    first_option = options_panel.get_by_role("checkbox").first
    brand_name = page.option_name(first_option).strip()
    first_option.check()

    # Collect product cards, then verify each product name contains the brand.
    products = page.all_products
    assert products.count() > 0, "No products were found after applying the brand filter"

    for index in range(products.count()):
        product_name = page.product_name(products.nth(index))
        assert brand_name.casefold() in product_name.casefold(), (
            f"Expected product name {product_name!r} to contain brand {brand_name!r}"
        )


