import allure
import pytest
from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage

INVALID_LOGIN_MSG = "user has been locked out"

@pytest.mark.ui
@allure.description("preform login with invalid user and get error message")
def test_1(page: Page):
    with allure.step("login with invalid user"):
        login_page = LoginPage(page)
        login_page.login(username="locked_out_user", password="secret_sauce")
        assert INVALID_LOGIN_MSG in login_page.get_error_massage()