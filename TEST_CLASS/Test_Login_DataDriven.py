import pytest
import allure
import os
import time
from UTILITIES.csv_utils import get_csv_data
from POM_CLASS.Login_Page_Object import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Get the absolute path to the CSV file
csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TEST_DATA", "login_test_data.csv")

@allure.epic("BTES LMS Application")
@allure.feature("Authentication")
@pytest.mark.usefixtures("setup")
class TestLoginDataDriven:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Login with Different Credentials")
    @allure.description("Test login functionality with different sets of credentials")
    @pytest.mark.parametrize("username,password,expected_title,expected_result",
                             [(row["username"], row["password"], row["expected_title"], row["expected_result"])
                              for row in get_csv_data(csv_file_path)])
    def test_login_with_different_credentials(self, username, password, expected_title, expected_result):
        # Get the driver from the fixture
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Create a unique test case title for Allure
        test_case_title = f"Login Test - Username: {username}, Password: {'*' * len(password) if password else 'empty'}, Expected: {expected_result}"
        allure.dynamic.title(test_case_title)

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            try:
                # Wait for the login page to load
                wait.until(EC.title_contains("Log in"))
                allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)
            except TimeoutException:
                allure.attach(driver.get_screenshot_as_png(), name="Page_Load_Error", attachment_type=allure.attachment_type.PNG)
                pytest.fail("Login page did not load properly")

        # Create login page object
        login_page = LoginPage(driver)

        # Perform login
        with allure.step(f"Login with username: {username} and password: {'*' * len(password) if password else 'empty'}"):
            try:
                login_page.login(username, password)
                # Wait for page to change or error message to appear
                time.sleep(2)  # Short wait for any redirects or error messages
                allure.attach(driver.get_screenshot_as_png(), name="After_Login_Attempt", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Login_Error", attachment_type=allure.attachment_type.PNG)
                allure.attach(str(e), name="Exception_Details", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Exception occurred during login: {str(e)}")

        # Verify login result
        with allure.step(f"Verify login result - Expected: {expected_result}"):
            actual_title = driver.title
            error_message = login_page.get_error_message()

            # Attach actual results to the report
            allure.attach(f"Actual Page Title: {actual_title}", name="Actual_Title", attachment_type=allure.attachment_type.TEXT)
            if error_message:
                allure.attach(f"Error Message: {error_message}", name="Error_Message", attachment_type=allure.attachment_type.TEXT)

            # For successful login, we expect to be redirected to Dashboard or similar page
            if expected_result.lower() == "pass":
                # Check if we're on the expected page after login
                if expected_title in actual_title:
                    allure.attach("Login successful", name="Login_Result", attachment_type=allure.attachment_type.TEXT)
                    assert True
                else:
                    allure.attach(f"Login failed. Expected title: {expected_title}, Actual title: {actual_title}",
                                 name="Login_Result", attachment_type=allure.attachment_type.TEXT)
                    assert False, f"Login should succeed but failed. Expected title to contain: {expected_title}, Actual title: {actual_title}"

            # For failed login, we expect to stay on the login page with an error message
            else:
                if expected_title in actual_title and error_message:
                    allure.attach("Login correctly failed", name="Login_Result", attachment_type=allure.attachment_type.TEXT)
                    assert True
                else:
                    allure.attach(f"Login should have failed but didn't behave as expected. Title: {actual_title}, Error message present: {bool(error_message)}",
                                 name="Login_Result", attachment_type=allure.attachment_type.TEXT)
                    assert False, f"Login should fail but didn't behave as expected. Expected to stay on login page with error message."
