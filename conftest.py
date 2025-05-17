import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
import os
import datetime

@pytest.fixture(scope="function")
def setup(request):
    """
    Fixture to set up the WebDriver for each test function.
    Creates a Chrome driver, maximizes the window, and sets implicit wait.
    Captures screenshot on test failure and quits the driver after test.
    """
    # Create Chrome driver with options
    chrome_options = webdriver.ChromeOptions()
    # Uncomment the line below if you want to run tests in headless mode
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    
    # Make driver available to the test function
    request.cls.driver = driver
    
    # Yield the driver to the test
    yield driver
    
    # Teardown: quit the driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure and attach to Allure report.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Get the fixture driver if it exists
        fixture_driver = getattr(item.instance, "driver", None)
        
        if report.failed and fixture_driver:
            # Take screenshot if test fails
            try:
                allure.attach(
                    fixture_driver.get_screenshot_as_png(),
                    name=f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}",
                    attachment_type=AttachmentType.PNG
                )
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
