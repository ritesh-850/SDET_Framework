import pytest
import allure
from POM_CLASS.Notifications_Page_Object import Notifications

@allure.epic("BTES LMS Application")
@allure.feature("Notifications")
@pytest.mark.usefixtures("setup")
class TestNotifications:

    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Check Notifications")
    @allure.description("Test to verify notifications functionality")
    @allure.title("Notifications Functionality Test")
    def test_notifications(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create notifications page object
        notifications = Notifications(driver)

        # Login to the application
        with allure.step("Login to the application"):
            notifications.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Open notifications
        with allure.step("Open notifications dropdown"):
            try:
                notifications.open_notifications()
                allure.attach(driver.get_screenshot_as_png(), name="Notifications_Dropdown", attachment_type=allure.attachment_type.PNG)
                
                # Verify notifications dropdown is open
                with allure.step("Verify notifications dropdown is open"):
                    is_dropdown_open = notifications.is_notifications_dropdown_open()
                    assert is_dropdown_open, "Notifications dropdown did not open"
                
                # Get notifications count
                with allure.step("Get notifications count"):
                    try:
                        count = notifications.get_notifications_count()
                        allure.attach(
                            f"Found {count} notifications".encode('utf-8'),
                            name="Notifications_Count",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    except Exception as e:
                        allure.attach(
                            f"Could not count notifications: {str(e)}".encode('utf-8'),
                            name="Notifications_Count_Error",
                            attachment_type=allure.attachment_type.TEXT
                        )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Opening_Notifications", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error opening notifications: {str(e)}")
    
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Access Notification Preferences")
    @allure.description("Test to verify access to notification preferences")
    @allure.title("Notification Preferences Test")
    def test_notification_preferences(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create notifications page object
        notifications = Notifications(driver)

        # Login to the application
        with allure.step("Login to the application"):
            notifications.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Open notifications
        with allure.step("Open notifications dropdown"):
            try:
                notifications.open_notifications()
                allure.attach(driver.get_screenshot_as_png(), name="Notifications_Dropdown", attachment_type=allure.attachment_type.PNG)
                
                # Go to notification preferences
                with allure.step("Go to notification preferences"):
                    notifications.go_to_notification_preferences()
                    allure.attach(driver.get_screenshot_as_png(), name="Notification_Preferences", attachment_type=allure.attachment_type.PNG)
                    
                    # Verify we're on the preferences page
                    assert "preferences" in driver.current_url.lower() or "preferences" in driver.title.lower(), "Failed to navigate to notification preferences"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Accessing_Preferences", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error accessing notification preferences: {str(e)}")
