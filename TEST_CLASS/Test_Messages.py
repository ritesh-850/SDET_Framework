import pytest
import allure
from POM_CLASS.Messages_Page_Object import Messages

@allure.epic("BTES LMS Application")
@allure.feature("Messaging")
@pytest.mark.usefixtures("setup")
class TestMessages:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Check Messages")
    @allure.description("Test to verify messages functionality")
    @allure.title("Messages Functionality Test")
    def test_messages(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create messages page object
        messages = Messages(driver)

        # Login to the application
        with allure.step("Login to the application"):
            messages.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Open messages
        with allure.step("Open messages dropdown"):
            try:
                messages.open_messages()
                allure.attach(driver.get_screenshot_as_png(), name="Messages_Dropdown", attachment_type=allure.attachment_type.PNG)
                
                # Verify messages dropdown is open
                with allure.step("Verify messages dropdown is open"):
                    is_dropdown_open = messages.is_messages_dropdown_open()
                    assert is_dropdown_open, "Messages dropdown did not open"
                
                # Get messages count
                with allure.step("Get messages count"):
                    try:
                        count = messages.get_messages_count()
                        allure.attach(
                            f"Found {count} messages".encode('utf-8'),
                            name="Messages_Count",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    except Exception as e:
                        allure.attach(
                            f"Could not count messages: {str(e)}".encode('utf-8'),
                            name="Messages_Count_Error",
                            attachment_type=allure.attachment_type.TEXT
                        )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Opening_Messages", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error opening messages: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Navigate to Messages Page")
    @allure.description("Test to verify navigation to messages page")
    @allure.title("Messages Page Navigation Test")
    def test_navigate_to_messages_page(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create messages page object
        messages = Messages(driver)

        # Login to the application
        with allure.step("Login to the application"):
            messages.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Open messages
        with allure.step("Open messages dropdown"):
            try:
                messages.open_messages()
                allure.attach(driver.get_screenshot_as_png(), name="Messages_Dropdown", attachment_type=allure.attachment_type.PNG)
                
                # Go to messages page
                with allure.step("Go to messages page"):
                    messages.go_to_messages_page()
                    allure.attach(driver.get_screenshot_as_png(), name="Messages_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Verify we're on the messages page
                    assert "message" in driver.current_url.lower() or "message" in driver.title.lower(), "Failed to navigate to messages page"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Navigating_To_Messages", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error navigating to messages page: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Send New Message")
    @allure.description("Test to verify sending a new message")
    @allure.title("Send Message Test")
    @pytest.mark.skip(reason="Skipping to avoid sending actual messages")
    def test_send_message(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create messages page object
        messages = Messages(driver)

        # Login to the application
        with allure.step("Login to the application"):
            messages.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Open messages
        with allure.step("Open messages dropdown"):
            try:
                messages.open_messages()
                allure.attach(driver.get_screenshot_as_png(), name="Messages_Dropdown", attachment_type=allure.attachment_type.PNG)
                
                # Go to messages page
                with allure.step("Go to messages page"):
                    messages.go_to_messages_page()
                    allure.attach(driver.get_screenshot_as_png(), name="Messages_Page", attachment_type=allure.attachment_type.PNG)
                
                # Start new message
                with allure.step("Start new message"):
                    messages.start_new_message()
                    allure.attach(driver.get_screenshot_as_png(), name="New_Message_Dialog", attachment_type=allure.attachment_type.PNG)
                
                # Search for a contact
                with allure.step("Search for a contact"):
                    messages.search_contact("admin")
                    allure.attach(driver.get_screenshot_as_png(), name="Contact_Search_Results", attachment_type=allure.attachment_type.PNG)
                
                # Select first contact
                with allure.step("Select first contact"):
                    contact_selected = messages.select_first_contact()
                    allure.attach(driver.get_screenshot_as_png(), name="Contact_Selected", attachment_type=allure.attachment_type.PNG)
                    
                    if contact_selected:
                        # Send a test message
                        with allure.step("Send a test message"):
                            messages.send_message("This is an automated test message. Please ignore.")
                            allure.attach(driver.get_screenshot_as_png(), name="Message_Sent", attachment_type=allure.attachment_type.PNG)
                    else:
                        pytest.skip("No contacts found to message")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Sending_Message", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error sending message: {str(e)}")
