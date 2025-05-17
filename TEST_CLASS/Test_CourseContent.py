import pytest
import allure
from POM_CLASS.CourseContent_Page_Object import CourseContent

@allure.epic("BTES LMS Application")
@allure.feature("Course Content Navigation")
@pytest.mark.usefixtures("setup")
class TestCourseContent:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Navigate Course Sections")
    @allure.description("Test to verify course content navigation functionality")
    @allure.title("Course Content Navigation Test")
    def test_course_content_navigation(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course content page object
        course_content = CourseContent(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_content.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            course_content.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                course_content.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Get section count
                with allure.step("Get section count"):
                    section_count = course_content.get_section_count()
                    allure.attach(
                        f"Found {section_count} sections in the course".encode('utf-8'),
                        name="Section_Count",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Get section titles
                with allure.step("Get section titles"):
                    section_titles = course_content.get_section_titles()
                    allure.attach(
                        "\n".join(section_titles).encode('utf-8'),
                        name="Section_Titles",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Navigate through sections if there are multiple sections
                if section_count > 1:
                    with allure.step("Navigate to next section"):
                        course_content.navigate_to_next_section()
                        allure.attach(driver.get_screenshot_as_png(), name="Next_Section", attachment_type=allure.attachment_type.PNG)
                    
                    with allure.step("Navigate to previous section"):
                        course_content.navigate_to_previous_section()
                        allure.attach(driver.get_screenshot_as_png(), name="Previous_Section", attachment_type=allure.attachment_type.PNG)
                
                # Select a section and activity if available
                with allure.step("Select first section"):
                    if course_content.select_section(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Selected_Section", attachment_type=allure.attachment_type.PNG)
                        
                        with allure.step("Get activities in section"):
                            activities = course_content.get_activities_in_section(0)
                            allure.attach(
                                f"Found {len(activities)} activities in the section".encode('utf-8'),
                                name="Activities_Count",
                                attachment_type=allure.attachment_type.TEXT
                            )
                        
                        if len(activities) > 0:
                            with allure.step("Select first activity"):
                                if course_content.select_activity(0, 0):
                                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Activity", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Navigation", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during course content navigation: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Open Course Resources")
    @allure.description("Test to verify opening course resources")
    @allure.title("Course Resources Test")
    def test_open_course_resources(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course content page object
        course_content = CourseContent(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_content.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            course_content.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                course_content.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Try to open a resource (using common resource names)
                resource_names = ["Lecture", "Assignment", "Quiz", "Document", "Video", "Presentation"]
                
                for resource_name in resource_names:
                    with allure.step(f"Try to open resource: {resource_name}"):
                        if course_content.open_resource(resource_name):
                            allure.attach(driver.get_screenshot_as_png(), name=f"Opened_{resource_name}", attachment_type=allure.attachment_type.PNG)
                            # Navigate back to course page
                            driver.back()
                            break
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Opening_Resources", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error opening course resources: {str(e)}")
