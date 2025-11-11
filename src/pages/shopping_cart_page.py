import re
from conftest import logger
from playwright.sync_api import Page, expect

CHECKOUT_OVERVIEW_HEADER = "Checkout: Overview"
ORDER_COMPLETE_MESSAGE = "Thank you for your order!"

class ShoppingCartPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_btn = self.page.locator("#checkout")
        self.first_name_field = self.page.locator("#first-name")
        self.last_name_field = self.page.locator("#last-name")
        self.zip_code_field = self.page.locator("#postal-code")
        self.continue_btn = self.page.locator("#continue")
        self.cancel_btn = self.page.locator("#cancel")
        self.checkout_overview_header = self.page.locator("css=span[data-test='title']")
        self.total_price_el = self.page.locator("css=div[data-test='total-label']")
        self.finish_btn = self.page.locator("#finish")
        self.order_complete_el = self.page.locator('css=h2[data-test="complete-header"]')

    def click_checkout(self) -> None:
        logger.info("clicking on checkout btn")
        self.checkout_btn.click()

    def fill_first_name(self, first_name: str) -> None:
        logger.info(f"filling first name with: {first_name}")
        self.first_name_field.fill(first_name)

    def fill_last_name(self, last_name: str) -> None:
        logger.info(f"filling last name with: {last_name}")
        self.last_name_field.fill(last_name)

    def fill_zip_code(self, code: str) -> None:
        logger.info(f"filling zip code with: {code}")
        self.zip_code_field.fill(code)

    def click_continue(self) -> None:
        logger.info("clicking continue")
        self.continue_btn.click()
        # validate overview showed up
        expect(self.checkout_overview_header).to_contain_text(CHECKOUT_OVERVIEW_HEADER)

    def click_cancel(self) -> None:
        logger.info("clicking cancel")
        self.cancel_btn.click()

    def get_total_price(self) -> str:
        price_el_str_value = self.total_price_el.inner_text()
        price_match = re.search(r"\$\d+(?:\.\d+)?", price_el_str_value)
        if price_match:
            price_number = price_match.group()
        else:
            price_number = ""

        logger.info(f"total price is: {price_number}")
        return price_number

    def click_finish(self) -> None:
        logger.info("clicking finish")
        self.finish_btn.click()

    def validate_order_complete(self, complete_message: str = ORDER_COMPLETE_MESSAGE) -> None:
        logger.info("validating order has been completed")
        expect(self.order_complete_el).to_contain_text(complete_message)