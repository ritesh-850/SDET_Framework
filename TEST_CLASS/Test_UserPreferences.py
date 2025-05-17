import pytest
import allure
from POM_CLASS.UserPreferences_Page_Object import UserPreferences

@allure.epic("BTES LMS Application")
@allure.feature("User Preferences")
@pytest.mark.usefixtures("setup")
class TestUserPreferences:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("View and Update Profile")
    @allure.description("Test to verify viewing and updating user profile")
    @allure.title("User Profile Test")
    def test_view_and_update_profile(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create user preferences page object
        user_preferences = UserPreferences(driver)

        # Login to the application
        with allure.step("Login to the application"):
            user_preferences.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to preferences
        with allure.step("Navigate to preferences"):
            user_preferences.navigate_to_preferences()
            allure.attach(driver.get_screenshot_as_png(), name="Preferences_Page", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to edit profile
        with allure.step("Navigate to edit profile"):
            user_preferences.navigate_to_edit_profile()
            allure.attach(driver.get_screenshot_as_png(), name="Edit_Profile_Page", attachment_type=allure.attachment_type.PNG)
        
        # Get current profile info
        with allure.step("Get current profile info"):
            current_profile = user_preferences.get_profile_info()
            profile_str = "\n".join([f"{key}: {value}" for key, value in current_profile.items()])
            allure.attach(
                profile_str.encode('utf-8'),
                name="Current_Profile_Info",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Update profile
        with allure.step("Update profile"):
            try:
                # Get current city and add " (Updated)" to it
                current_city = current_profile.get("city", "Test City")
                updated_city = current_city + " (Updated)"
                
                # Update only the city field
                user_preferences.update_profile(city=updated_city)
                allure.attach(driver.get_screenshot_as_png(), name="After_Profile_Update", attachment_type=allure.attachment_type.PNG)
                
                # Verify profile was updated
                with allure.step("Verify profile was updated"):
                    # Navigate back to edit profile
                    user_preferences.navigate_to_preferences()
                    user_preferences.navigate_to_edit_profile()
                    
                    # Get updated profile info
                    updated_profile = user_preferences.get_profile_info()
                    updated_profile_str = "\n".join([f"{key}: {value}" for key, value in updated_profile.items()])
                    allure.attach(
                        updated_profile_str.encode('utf-8'),
                        name="Updated_Profile_Info",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Verify city was updated
                    assert updated_profile.get("city") == updated_city, f"City was not updated to '{updated_city}'"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Updating_Profile", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error updating profile: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Change Language Preference")
    @allure.description("Test to verify changing language preference")
    @allure.title("Language Preference Test")
    def test_change_language_preference(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create user preferences page object
        user_preferences = UserPreferences(driver)

        # Login to the application
        with allure.step("Login to the application"):
            user_preferences.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to preferences
        with allure.step("Navigate to preferences"):
            user_preferences.navigate_to_preferences()
            allure.attach(driver.get_screenshot_as_png(), name="Preferences_Page", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to preferred language
        with allure.step("Navigate to preferred language"):
            user_preferences.navigate_to_preferred_language()
            allure.attach(driver.get_screenshot_as_png(), name="Language_Preference_Page", attachment_type=allure.attachment_type.PNG)
        
        # Change language
        with allure.step("Change language to English (en)"):
            try:
                user_preferences.change_language("English (en)")
                allure.attach(driver.get_screenshot_as_png(), name="After_Language_Change", attachment_type=allure.attachment_type.PNG)
                
                # Verify language was changed
                assert "changes saved" in driver.page_source.lower(), "Language change was not saved"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Changing_Language", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error changing language: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Manage Notification Preferences")
    @allure.description("Test to verify managing notification preferences")
    @allure.title("Notification Preferences Test")
    def test_manage_notification_preferences(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create user preferences page object
        user_preferences = UserPreferences(driver)

        # Login to the application
        with allure.step("Login to the application"):
            user_preferences.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to preferences
        with allure.step("Navigate to preferences"):
            user_preferences.navigate_to_preferences()
            allure.attach(driver.get_screenshot_as_png(), name="Preferences_Page", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to notification preferences
        with allure.step("Navigate to notification preferences"):
            user_preferences.navigate_to_notification_preferences()
            allure.attach(driver.get_screenshot_as_png(), name="Notification_Preferences_Page", attachment_type=allure.attachment_type.PNG)
        
        # Toggle email notification
        with allure.step("Toggle email notification"):
            try:
                result = user_preferences.toggle_email_notification(0, True)
                allure.attach(driver.get_screenshot_as_png(), name="After_Notification_Toggle", attachment_type=allure.attachment_type.PNG)
                
                if result:
                    # Verify notification preference was changed
                    assert "preferences saved" in driver.page_source.lower(), "Notification preference change was not saved"
                else:
                    pytest.skip("No email notification checkbox found")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Changing_Notification", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error changing notification preference: {str(e)}")
