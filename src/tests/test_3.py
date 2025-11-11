import allure
import pytest
from playwright.sync_api import Page
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage
from src.workflows.checkout import checkout


@pytest.mark.ui
@allure.description("preform login with problematic user and try to add items and checkout")
def test_3(page: Page):
    with allure.step("login with problematic user"):
        login_page = LoginPage(page)
        login_page.login(username="problem_user", password="secret_sauce")

    with allure.step("remove selected products from cart"):
        products_page = ProductsPage(page)
        if not products_page.is_cart_empty():
            # start removing products
            products_page.remove_all_selected_items()

    with allure.step("add products to cart"):
        products = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"]
        products_page.add_items_to_cart(item_names=products)

    with allure.step("perform checkout"):
        # perform checkout flow
        checkout(
            page,
            first_name="dummy",
            last_name="dummy last",
            zip_code="12345678"
        )
