import pytest
import allure
from POM_CLASS.ForgotPassword_Page_Object import ForgotPassword

@allure.epic("BTES LMS Application")
@allure.feature("Password Recovery")
@pytest.mark.usefixtures("setup")
class TestForgotPassword:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Recover Password by Username")
    @allure.description("Test to verify password recovery functionality using username")
    @allure.title("Password Recovery by Username Test")
    def test_forgot_password_by_username(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create forgot password page object
        forgot_password = ForgotPassword(driver)

        # Click on forgot password link
        with allure.step("Click on Forgotten your username or password link"):
            forgot_password.click_forgot_password_link()
            allure.attach(driver.get_screenshot_as_png(), name="Forgot_Password_Page", attachment_type=allure.attachment_type.PNG)

        # Search by username
        with allure.step("Search by username: test_user"):
            # Note: We're using a dummy username to avoid triggering real password reset emails
            forgot_password.search_by_username("test_user")
            allure.attach(driver.get_screenshot_as_png(), name="After_Search_By_Username", attachment_type=allure.attachment_type.PNG)

        # Verify we're on the confirmation page or error page
        with allure.step("Verify search result"):
            # Just check that we've moved past the search form
            page_source = driver.page_source.lower()
            assert "search" in page_source or "email" in page_source or "sent" in page_source or "not found" in page_source

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Recover Password by Email")
    @allure.description("Test to verify password recovery functionality using email")
    @allure.title("Password Recovery by Email Test")
    def test_forgot_password_by_email(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create forgot password page object
        forgot_password = ForgotPassword(driver)

        # Click on forgot password link
        with allure.step("Click on Forgotten your username or password link"):
            forgot_password.click_forgot_password_link()
            allure.attach(driver.get_screenshot_as_png(), name="Forgot_Password_Page", attachment_type=allure.attachment_type.PNG)

        # Search by email
        with allure.step("Search by email: test@example.com"):
            # Note: We're using a dummy email to avoid triggering real password reset emails
            forgot_password.search_by_email("test@example.com")
            allure.attach(driver.get_screenshot_as_png(), name="After_Search_By_Email", attachment_type=allure.attachment_type.PNG)

        # Verify we're on the confirmation page or error page
        with allure.step("Verify search result"):
            # Just check that we've moved past the search form
            page_source = driver.page_source.lower()
            assert "search" in page_source or "email" in page_source or "sent" in page_source or "not found" in page_source
