import pytest
import os
import re

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckOutPage

# capture test results
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# Setup tracing automatically on the browser context
@pytest.fixture(autouse=True)
def manage_traces_and_screenshots(page, request):
    # Start tracing before the test runs
    browser_context = page.context

    browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield # The test runs here

    # Checks if the core test run ('call') failed
    failed = getattr(request.node, "rep_call", None)
    if failed and failed.failed:
        # 1. Sanitize the filename to protect CI runners
        safe_name = re.sub(r'[^\w\-_]', '_', request.node.name)
        
        # 2. Save a Full-Page Screenshot
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{safe_name}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        
        # 3. Stop tracing and explicitly export the ZIP file
        trace_dir = "test-results"
        os.makedirs(trace_dir, exist_ok=True)
        trace_path = os.path.join(trace_dir, f"{safe_name}_trace.zip")
        browser_context.tracing.stop(path=trace_path)
    else:
        # If the test passes, silently discard the trace data to save disk space
        browser_context.tracing.stop()

# Page Object Fixtures

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)

@pytest.fixture
def checkout_page(page):
    return CheckOutPage(page)