from playwright.sync_api import Page
from conftest import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.menu_btn = self.page.locator("#react-burger-menu-btn")
        self.reset_app_state_btn = self.page.locator("#reset_sidebar_link")
        self.logout_btn = self.page.locator("#logout_sidebar_link")
        self.about_btn = self.page.locator("#about_sidebar_link")
        self.all_items_btn = self.page.locator("#inventory_sidebar_link")

    def click_on_menu(self) -> None:
        logger.info("clicking on menu btn")
        self.menu_btn.click()

    def click_on_reset_app_state(self) -> None:
        logger.info("clicking on reset app btn")
        self.reset_app_state_btn.click()