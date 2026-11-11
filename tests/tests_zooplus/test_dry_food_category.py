import math
import re
from urllib.parse import urlparse

import allure
from playwright.sync_api import Page, expect


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
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
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.NORMAL)
def test_brand_filter(zooplus_dryfoodpage_pom) -> None:
    """Verify that filtering by brand works properly."""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Find filter button and expand it if needed'):
        page.filter_button('Märke')
    with allure.step('Filter by first brand in the list'):
        first_option = page.options_inside_filter('Märke').first
        brand_name = page.option_name(first_option)
        page.option_checkbox(first_option).check()
        # wait 2 seconds to let the page update list of products
        page.wait(2000)
    with allure.step('Verify that brand filter is applied in URL'):
        page.verify_url('?filters=brand')
    with allure.step('Verify that all products match filter'):
        result = True
        # Check that every product's name contains
        for p in range(page.all_products().count()):
            name = page.product_name(page.all_products().nth(p))
            if not re.match(brand_name, name, re.IGNORECASE):
                print(f'Product {name} does not correspond to brand name: {brand_name}')
                result = False
                break
        assert result

@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.NORMAL)
def test_flavour_filter(zooplus_dryfoodpage_pom) -> None:
    """Verify that filtering by flavor works properly."""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Fill "Fasan" value into searchbox'):
        page.searchbox_inside_filter('Smak').fill('Fasan')
    with allure.step('Apply filter'):
        taste_option = page.options_inside_filter('Smak')
        amount = page.option_counter(taste_option)
        page.option_checkbox(taste_option).check()
        # wait 2 seconds to let the page update list of products
        page.wait(2000)
    with allure.step('Verify that flavour filter is applied in URL'):
        page.verify_url('?filters=flavour')
    with allure.step('Verify that amount of products equal to amount near the filter'):
        assert page.all_products().count() == amount


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.NORMAL)
def test_price_filter(zooplus_dryfoodpage_pom) -> None:
    """Verify that filtering by price works properly."""
    min_price = '590'
    max_price = '600'
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Apply price filter 500-700'):
        page.filter_button('Pris')
        page.min_price.fill(min_price)
        page.max_price.fill(max_price)
        # wait for 2 seconds to let the page update list of products
        page.wait(2000)
    with allure.step('Verify that price filter is applied in URL'):
        page.verify_url('?filters=current_price')
    with allure.step(f'Verify that all products have price in range {min_price} to {max_price}'):
        result = True
        # Check that every product have price in applied range
        for p in range(page.all_products().count()):
            price = page.product_price(page.all_products().nth(p))
            if not float(min_price) <= price <= float(max_price):
                print(f'Price {price} is out of range: {min_price} - {max_price}')
                result = False
                break
        assert result


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.NORMAL)
def test_filters_combination(zooplus_dryfoodpage_pom) -> None:
    """Verify that two filters work properly"""
    min_price = "1000"
    max_price = "1400"
    brand = 'Arion'
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Apply brand filter'):
        page.filter_button('Märke')
        page.searchbox_inside_filter('Märke').fill(brand)
        brand_option = page.options_inside_filter('Märke')
        page.option_checkbox(brand_option).check()
    with allure.step('Apply price filter'):
        page.filter_button('Pris')
        page.min_price.fill(min_price)
        page.max_price.fill(max_price)
        # wait 2 seconds to let the page update products
        page.wait(2000)
    with allure.step('Verify that all products satisfy both filters'):
        result = True
        for id in range(page.all_products().count()):
            current_product = page.all_products().nth(id)
            price = page.product_price(current_product)
            name = page.product_name(current_product)
            if not (float(min_price) <= price <= float(max_price) or re.match('Arion', name, re.IGNORECASE)):
                print(f'This combination failed: {name}: {price}')
                result = False
                break
        assert result



# Below are tests to be rewritten



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