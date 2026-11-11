import re
import allure
from playwright.sync_api import expect


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.CRITICAL)
def test_products_page_important_elements(zooplus_dryfoodpage_pom) -> None:
    """Verify that products page important elements are visible."""
    page = zooplus_dryfoodpage_pom
    with allure.step("Open the dry-food category page"):
        page.open()
    with allure.step('Verify page title'):
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


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.NORMAL)
def test_sorting_by_price(zooplus_dryfoodpage_pom) -> None:
    """Verify that sorting by price (low-to-high and high-to-low) works properly"""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Apply low-to-high price filter'):
        page.sort_by_price_low_to_high()
        # wait 2 seconds to let the page update products
        page.wait(2000)
    with allure.step('Verify that sorting is applied in URL'):
        page.verify_url('?sorting=lowest-price')
    with allure.step('Verify that products are sorted by price from the lowest to the highest'):
        result = True
        for p in range(page.all_products().count() -1):
            current_price = page.product_price(page.all_products().nth(p))
            next_price = page.product_price(page.all_products().nth(p + 1))
            if current_price > next_price:
                print(f'Price of the current product {current_price} is bigger than price of the next one {next_price}')
                result = False
                break
        assert result
    with allure.step('Apply high-to-low price filter'):
        page.sort_by_price_high_to_low()
        # wait 2 seconds to let the page update products
        page.wait(2000)
    with allure.step('Verify that sorting is applied in URL'):
        page.verify_url('?sorting=highest-price')
    with allure.step('Verify that products are sorted by price from the highest to the lowest'):
        result = True
        for p in range(page.all_products().count() -1):
            current_price = page.product_price(page.all_products().nth(p))
            next_price = page.product_price(page.all_products().nth(p + 1))
            if current_price < next_price:
                print(f'Price of the current product {current_price} is smaller than price of the next one {next_price}')
                result = False
                break
        assert result


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.CRITICAL)
def test_pagination(zooplus_dryfoodpage_pom) -> None:
    """Verify that pagination works properly"""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Make sure that pagination element is visible on the page'):
        expect(page.pagination).to_be_visible()
    with allure.step('Record the first product ID'):
        first_product_1st_page = page.product_id(page.all_products().first)
    with allure.step('Check that [Previous page] button is disabled as we are on the first page'):
        expect(page.prev_page).to_be_disabled()
    with allure.step('Open the next page'):
        page.next_page.click()
    with allure.step('Verify that current page is in URL'):
        page.verify_url('?p=2')
    with allure.step('Verify that [Previous page] button is enabled now'):
        expect(page.prev_page).to_be_enabled()
    with allure.step('Verify that first product on the second page is different'):
        first_product_2nd_page = page.product_id(page.all_products().first)
        assert first_product_1st_page != first_product_2nd_page
    with allure.step('Go back to the first page'):
        page.prev_page.click()
    with allure.step('Verify that first product on the page remained the same'):
        assert first_product_1st_page == page.product_id(page.all_products().first)


@allure.epic("Zooplus")
@allure.feature('Zooplus dry food page')
@allure.severity(allure.severity_level.BLOCKER)
def test_product_listning_opens_matching_product(zooplus_dryfoodpage_pom):
    """Verify that click on product opens matching product detail page."""
    page = zooplus_dryfoodpage_pom
    with allure.step('Open the dry-food category page'):
        page.open()
    with allure.step('Save details of the first product on the page'):
        product = page.all_products().first
        product_name = page.product_name(product)
        product_price = page.product_price(product)
        product_id = page.product_id(product)
    with allure.step('Click on the first product on the page'):
        # print(f'Product html: {product.inner_html()}')
        product.locator('[data-zta=product-link]').click()
        # wait 2 seconds to let the page udpate
        page.wait(2000)
    with (allure.step('Verify that right product is opened')):
        page.verify_url(product_id)
        expect(page.page).to_have_title(re.compile(rf'{product_name}'))
        assert product_price == page.product_price(page.page.locator('[data-zta=SelectedArticleBox]'))


