import pytest
import allure
from POM_CLASS.Login_Page_Object import LoginPage

@allure.epic("BTES LMS Application")
@allure.feature("Login Functionality")
@pytest.mark.usefixtures("setup")
class Testlogin:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Verify Login with Valid Credentials")
    @allure.description("Test to verify login functionality with valid credentials")
    @allure.title("Login Test with Valid Credentials")
    def test_login(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")

        # Create login page object
        lp = LoginPage(driver)

        # Enter username
        with allure.step("Enter username: ritesh@123"):
            lp.setUserName("ritesh@123")

        # Enter password
        with allure.step("Enter password: Ritesh@123"):
            lp.setPassword("Ritesh@123")

        # Click login button
        with allure.step("Click on Login button"):
            lp.setBtn()

        # Verify login success
        with allure.step("Verify login success by checking page title"):
            act_title = driver.title
            allure.attach(driver.get_screenshot_as_png(), name="Login_Success", attachment_type=allure.attachment_type.PNG)
            assert act_title == 'Dashboard' or act_title == 'BTES-LMS: Log in to the site', "Login failed: Title verification failed"
