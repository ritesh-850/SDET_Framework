import pytest
import allure
import time
from POM_CLASS.CourseManagement_Page_Object import CourseManagement

@allure.epic("BTES LMS Application")
@allure.feature("Course Management")
@pytest.mark.usefixtures("setup")
class TestCourseManagement:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("View Course Settings")
    @allure.description("Test to verify viewing course settings")
    @allure.title("Course Settings Test")
    def test_view_course_settings(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course management page object
        course_management = CourseManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                course_management.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    course_management.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course settings
                    with allure.step("Navigate to course settings"):
                        course_management.navigate_to_course_settings()
                        allure.attach(driver.get_screenshot_as_png(), name="Course_Settings_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Get course name
                        with allure.step("Get course name"):
                            course_name = course_management.get_course_name()
                            allure.attach(
                                f"Course name: {course_name}".encode('utf-8'),
                                name="Course_Name",
                                attachment_type=allure.attachment_type.TEXT
                            )
                            
                            # Verify course name is not empty
                            assert course_name != "Course name not found", "Failed to get course name"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_Course_Settings", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing course settings: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("View Course Participants")
    @allure.description("Test to verify viewing course participants")
    @allure.title("Course Participants Test")
    def test_view_course_participants(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course management page object
        course_management = CourseManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                course_management.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    course_management.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course participants
                    with allure.step("Navigate to course participants"):
                        course_management.navigate_to_course_participants()
                        allure.attach(driver.get_screenshot_as_png(), name="Course_Participants_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Get participant count
                        with allure.step("Get participant count"):
                            participant_count = course_management.get_participant_count()
                            allure.attach(
                                f"Participant count: {participant_count}".encode('utf-8'),
                                name="Participant_Count",
                                attachment_type=allure.attachment_type.TEXT
                            )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_Participants", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing course participants: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Update Course Settings")
    @allure.description("Test to verify updating course settings")
    @allure.title("Update Course Settings Test")
    @pytest.mark.skip(reason="Skipping to avoid modifying actual course settings")
    def test_update_course_settings(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course management page object
        course_management = CourseManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                course_management.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    course_management.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course settings
                    with allure.step("Navigate to course settings"):
                        course_management.navigate_to_course_settings()
                        allure.attach(driver.get_screenshot_as_png(), name="Course_Settings_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Get current course name
                        current_course_name = course_management.get_course_name()
                        
                        # Update course settings
                        with allure.step("Update course settings"):
                            # Update with the same name (to avoid changing the actual course name)
                            course_management.update_course_settings(course_name=current_course_name)
                            allure.attach(driver.get_screenshot_as_png(), name="After_Updating_Settings", attachment_type=allure.attachment_type.PNG)
                            
                            # Verify settings were updated
                            assert "updated" in driver.page_source.lower(), "Course settings were not updated successfully"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Updating_Course_Settings", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error updating course settings: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Add Course Activity")
    @allure.description("Test to verify adding an activity to a course")
    @allure.title("Add Course Activity Test")
    @pytest.mark.skip(reason="Skipping to avoid adding actual course activities")
    def test_add_course_activity(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course management page object
        course_management = CourseManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                course_management.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    course_management.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Add an activity
                    with allure.step("Add an activity"):
                        activity_name = f"Test Assignment {time.strftime('%Y-%m-%d %H:%M:%S')}"
                        activity_description = "This is a test assignment created by the automated test."
                        
                        course_management.add_activity("Assignment", activity_name, activity_description)
                        allure.attach(driver.get_screenshot_as_png(), name="After_Adding_Activity", attachment_type=allure.attachment_type.PNG)
                        
                        # Verify activity was added
                        assert activity_name in driver.page_source, f"Activity '{activity_name}' was not added successfully"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Adding_Activity", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error adding course activity: {str(e)}")
