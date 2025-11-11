import allure
import pytest
from playwright.sync_api import Page
from src.pages.base_page import BasePage
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage
from src.pages.shopping_cart_page import ShoppingCartPage

TOTAL_PRICE = "$95.01"

@pytest.mark.ui
@allure.description("add items to cart and perform the checkout flow")
def test_2(page: Page):
    with allure.step("login with valid user"):
        login_page = LoginPage(page)
        login_page.login(username="standard_user", password="secret_sauce")

    with allure.step("add products to cart"):
        products_page = ProductsPage(page)
        products = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"]
        products_page.add_items_to_cart(item_names=products)
        products_page.enter_shopping_cart()

    with allure.step("perform checkout"):
        shopping_cart_page = ShoppingCartPage(page)
        shopping_cart_page.click_checkout()
        shopping_cart_page.fill_first_name("dummy")
        shopping_cart_page.fill_last_name("dummy last")
        shopping_cart_page.fill_zip_code("121432345")
        shopping_cart_page.click_continue()

        assert shopping_cart_page.get_total_price() == TOTAL_PRICE
        shopping_cart_page.click_finish()
        shopping_cart_page.validate_order_complete()

    with allure.step("enter menu and reset app"):
        base_page = BasePage(page)
        base_page.click_on_menu()
        base_page.click_on_reset_app_state()