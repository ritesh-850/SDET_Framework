import pytest
import allure
from POM_CLASS.Calender_Page_Object import Calender

@allure.epic("BTES LMS Application")
@allure.feature("Calendar Functionality")
@pytest.mark.usefixtures("setup")
class TestCalender:

    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Access Calendar")
    @allure.description("Test to verify calendar access functionality")
    @allure.title("Calendar Access Test")
    @pytest.mark.parametrize("username,password", [("ritesh@123", "Ritesh@123")])
    def test_calender(self, username, password):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create calendar page object
        ca = Calender(driver)

        # Login steps
        with allure.step(f"Login with username: {username} and password: {password}"):
            ca.setUserName(username)
            ca.setPassword(password)
            ca.setBtn()
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)

        # Click on sidebar
        with allure.step("Click on sidebar"):
            ca.sidebar()
            allure.attach(driver.get_screenshot_as_png(), name="After_Sidebar_Click", attachment_type=allure.attachment_type.PNG)

        # Access calendar
        with allure.step("Access calendar"):
            ca.calender()
            allure.attach(driver.get_screenshot_as_png(), name="Calendar_Page", attachment_type=allure.attachment_type.PNG)

            # Add an assertion to verify we're on the calendar page
            assert "Calendar" in driver.title or "calendar" in driver.current_url.lower(), "Calendar page not loaded correctly"