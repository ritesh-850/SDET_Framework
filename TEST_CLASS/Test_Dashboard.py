import pytest
import allure
from POM_CLASS.Dashboard_Page_Object import Dashboard

@allure.epic("BTES LMS Application")
@allure.feature("Dashboard Functionality")
@pytest.mark.usefixtures("setup")
class TestDashboard:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Access Dashboard")
    @allure.description("Test to verify dashboard access functionality")
    @allure.title("Dashboard Access Test")
    def test_dashboard(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")

        # Create dashboard page object
        da = Dashboard(driver)

        # Login steps
        with allure.step("Login to the application"):
            da.setUserName("ritesh@123")
            da.setPassword("Ritesh@123")
            da.setBtn()
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)

        # Click on sidebar
        with allure.step("Click on sidebar"):
            da.sidebar()
            allure.attach(driver.get_screenshot_as_png(), name="After_Sidebar_Click", attachment_type=allure.attachment_type.PNG)

        # Access dashboard
        with allure.step("Access dashboard"):
            da.dahsboard()
            allure.attach(driver.get_screenshot_as_png(), name="Dashboard_Page", attachment_type=allure.attachment_type.PNG)
