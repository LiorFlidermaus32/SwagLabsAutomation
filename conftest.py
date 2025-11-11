import os
import allure
import pytest
import logging
from typing import Union
from pathlib import Path
from datetime import datetime
from playwright.sync_api import BrowserContext, sync_playwright, Page


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]: %(message)s",
)
logger = logging.getLogger(__name__)

SAUCE_LABS_URL = "https://www.saucedemo.com/"


def get_project_path() -> Path:
    return Path(__file__).parent.resolve()


# List of browsers to run tests with
BROWSERS = ["chromium", "firefox", "webkit"]

# Parametrize the browser type for all tests
@pytest.fixture(params=BROWSERS)
def browser_type(request) -> str:
    return request.param

# Generic browser context fixture
@pytest.fixture(scope="function")
def browser_context(browser_type: str) -> BrowserContext:
    with sync_playwright() as playwright:
        if browser_type == "chromium":
            browser = playwright.chromium.launch(
                headless=False,
                args=["--start-maximized"],
            )
        elif browser_type == "firefox":
            browser = playwright.firefox.launch(
                headless=False,
            )
        elif browser_type == "webkit":
            browser = playwright.webkit.launch(
                headless=False,
            )
        else:
            raise ValueError(f"Unknown browser type: {browser_type}")

        context = browser.new_context(no_viewport=True)

        yield context
        context.close()
        browser.close()

# Generic page fixture
@pytest.fixture(scope="function")
def page(browser_context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    logger.info(f"Running test: [{request.node.name}]")
    page = browser_context.new_page()
    page.goto(SAUCE_LABS_URL)
    yield page
    page.close()

# hook to capture screenshots automatically
@pytest.hookimpl
def pytest_exception_interact(node: Union[pytest.Item, pytest.Collector], call: pytest.CallInfo):
    """ take screenshot in case of exception and save it to screenshots folder and attach to allure"""
    if call.when == "call":
        if not isinstance(call.excinfo.type, KeyboardInterrupt):
            if "chromium_page" in node.funcargs:
                page: Page = node.funcargs.get("chromium_page", None)

                os.makedirs(get_project_path() / "screenshots", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                test_name = node.name
                screenshot_path = f"{get_project_path().as_posix()}/screenshots/{test_name}_{timestamp}.png"

                # Take the screenshot
                page.screenshot(path=screenshot_path, full_page=True)
                allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)
                logger.info(f"Screenshot saved to: {screenshot_path}")
