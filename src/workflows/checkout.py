from playwright.sync_api import Page
from src.pages.products_page import ProductsPage
from src.pages.shopping_cart_page import ShoppingCartPage


def checkout(page: Page, first_name: str, last_name: str, zip_code: str):
    # global checkout flow
    products_page = ProductsPage(page)
    products_page.enter_shopping_cart()

    shopping_cart_page = ShoppingCartPage(page)
    shopping_cart_page.click_checkout()
    shopping_cart_page.fill_first_name(first_name=first_name)
    shopping_cart_page.fill_last_name(last_name=last_name)
    shopping_cart_page.fill_zip_code(code=zip_code)
    shopping_cart_page.click_continue()
    shopping_cart_page.click_finish()
    shopping_cart_page.validate_order_complete()