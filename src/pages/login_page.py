from playwright.sync_api import Page
from conftest import logger

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_field = page.locator("#user-name")
        self.password_field = page.locator("#password")
        self.login_btn = page.locator("#login-button")
        self.error_msg_el = page.locator("css=h3[data-test='error']")

    def login(self, username: str, password: str) -> None:
        logger.info(f"logging in with user: {username}")
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_btn.click()

    def get_error_massage(self) -> str:
        return self.error_msg_el.inner_text()

