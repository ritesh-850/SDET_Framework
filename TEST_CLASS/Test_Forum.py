import pytest
import allure
import time
from POM_CLASS.Forum_Page_Object import Forum

@allure.epic("BTES LMS Application")
@allure.feature("Forum Participation")
@pytest.mark.usefixtures("setup")
class TestForum:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Create Discussion")
    @allure.description("Test to verify creating a discussion in a forum")
    @allure.title("Create Discussion Test")
    def test_create_discussion(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create forum page object
        forum = Forum(driver)

        # Login to the application
        with allure.step("Login to the application"):
            forum.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            forum.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                forum.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Open a forum
                with allure.step("Open the first available forum"):
                    if forum.open_forum(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Forum_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Click Add discussion topic button
                        with allure.step("Click Add discussion topic button"):
                            if forum.click_add_discussion():
                                allure.attach(driver.get_screenshot_as_png(), name="Add_Discussion_Form", attachment_type=allure.attachment_type.PNG)
                                
                                # Create a discussion
                                with allure.step("Create a discussion"):
                                    subject = f"Test Discussion {time.strftime('%Y-%m-%d %H:%M:%S')}"
                                    message = "This is a test discussion created by the automated test. It demonstrates the ability to create discussions in forums."
                                    forum.create_discussion(subject, message)
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Creating_Discussion", attachment_type=allure.attachment_type.PNG)
                                    
                                    # Verify the discussion was created
                                    assert subject in driver.page_source, "Discussion was not created successfully"
                            else:
                                pytest.skip("Could not click Add discussion topic button")
                    else:
                        pytest.skip("No forums found in the course")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Creating_Discussion", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error creating discussion: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Reply to Discussion")
    @allure.description("Test to verify replying to a discussion in a forum")
    @allure.title("Reply to Discussion Test")
    def test_reply_to_discussion(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create forum page object
        forum = Forum(driver)

        # Login to the application
        with allure.step("Login to the application"):
            forum.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            forum.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                forum.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Open a forum
                with allure.step("Open the first available forum"):
                    if forum.open_forum(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Forum_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Open a discussion
                        with allure.step("Open the first available discussion"):
                            if forum.open_discussion(0):
                                allure.attach(driver.get_screenshot_as_png(), name="Discussion_Page", attachment_type=allure.attachment_type.PNG)
                                
                                # Get initial post count
                                with allure.step("Get initial post count"):
                                    initial_posts = forum.get_discussion_posts()
                                    initial_count = len(initial_posts)
                                    allure.attach(
                                        f"Initial post count: {initial_count}".encode('utf-8'),
                                        name="Initial_Post_Count",
                                        attachment_type=allure.attachment_type.TEXT
                                    )
                                
                                # Reply to the discussion
                                with allure.step("Reply to the discussion"):
                                    reply_message = f"This is a test reply created by the automated test at {time.strftime('%Y-%m-%d %H:%M:%S')}."
                                    forum.reply_to_discussion(reply_message)
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Replying", attachment_type=allure.attachment_type.PNG)
                                    
                                    # Verify the reply was posted
                                    with allure.step("Verify the reply was posted"):
                                        # Wait for the page to refresh
                                        time.sleep(2)
                                        
                                        # Get updated post count
                                        updated_posts = forum.get_discussion_posts()
                                        updated_count = len(updated_posts)
                                        allure.attach(
                                            f"Updated post count: {updated_count}".encode('utf-8'),
                                            name="Updated_Post_Count",
                                            attachment_type=allure.attachment_type.TEXT
                                        )
                                        
                                        # Get post contents
                                        contents = forum.get_post_contents()
                                        allure.attach(
                                            "\n---\n".join(contents).encode('utf-8'),
                                            name="Post_Contents",
                                            attachment_type=allure.attachment_type.TEXT
                                        )
                                        
                                        # Verify the reply is in the contents
                                        reply_found = any(reply_message in content for content in contents)
                                        assert reply_found, "Reply was not found in the discussion"
                            else:
                                pytest.skip("No discussions found in the forum")
                    else:
                        pytest.skip("No forums found in the course")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Replying_To_Discussion", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error replying to discussion: {str(e)}")
