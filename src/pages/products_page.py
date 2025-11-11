from playwright.sync_api import Page, Locator, expect
from conftest import logger

ADD_TO_CART_BTN_MAME = "Add to cart"
REMOVE_FROM_CART_BTN_NAME = "Remove"

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.all_products = self.page.locator("div[data-test='inventory-item']")
        self.add_to_cart_btn = self.page.locator(f"//button[contains(text(), '{ADD_TO_CART_BTN_MAME}')]")
        self.remove_from_cart_btn = self.page.locator(f"//button[contains(text(), '{REMOVE_FROM_CART_BTN_NAME}')]")
        self.selected_products_counter = self.page.locator("css=span[data-test='shopping-cart-badge']")
        self.shopping_cart_btn = self.page.locator('css=a[data-test="shopping-cart-link"]')


    def _get_item_locator_by_name(self, item_name: str) -> Locator:
        selector = (
            f'//div[@data-test="inventory-item-name"]'
            f'[contains(text(), "{item_name}")]//ancestor::div[@data-test="inventory-item"]'
        )
        return self.page.locator(selector)

    def get_num_of_selected_products(self) -> int:
        if not self.selected_products_counter.is_visible():
            return 0

        return int(self.selected_products_counter.inner_text())

    def add_item_to_cart(self, item_name: str) -> None:
        logger.info(f"adding item with name: {item_name} to cart")
        num_of_selected_products_before = self.get_num_of_selected_products()

        curr_product = self._get_item_locator_by_name(item_name)
        curr_product.locator(self.add_to_cart_btn).click()

        # validate product addition to cart
        expect(self.selected_products_counter).to_contain_text(str(num_of_selected_products_before + 1))


    def add_items_to_cart(self, item_names: list[str]) -> None:
        for item in item_names:
            self.add_item_to_cart(item_name=item)

    def enter_shopping_cart(self) -> None:
        logger.info("clicking on shopping cart btn")
        self.shopping_cart_btn.click()

    def remove_all_selected_items(self) -> None:
        for remove_btn in self.remove_from_cart_btn.all():
            logger.info("removed 1 item from cart")
            remove_btn.click()

        expect(self.remove_from_cart_btn).to_have_count(0)

    def is_cart_empty(self) -> bool:
        return self.get_num_of_selected_products() == 0