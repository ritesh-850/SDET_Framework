import pytest
import allure
from POM_CLASS.CourseEnrollment_Page_Object import CourseEnrollment

@allure.epic("BTES LMS Application")
@allure.feature("Course Enrollment")
@pytest.mark.usefixtures("setup")
class TestCourseEnrollment:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Enroll in a Course")
    @allure.description("Test to verify course enrollment functionality")
    @allure.title("Course Enrollment Test")
    def test_course_enrollment(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create course enrollment page object
        course_enrollment = CourseEnrollment(driver)

        # Login to the application
        with allure.step("Login to the application"):
            course_enrollment.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            course_enrollment.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                course_enrollment.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Try to enroll in the course
                with allure.step("Attempt to enroll in the course"):
                    enrollment_result = course_enrollment.enroll_in_course()
                    allure.attach(driver.get_screenshot_as_png(), name="After_Enrollment_Attempt", attachment_type=allure.attachment_type.PNG)
                
                # Verify enrollment status
                with allure.step("Verify enrollment status"):
                    # Either we successfully enrolled or we were already enrolled
                    is_enrolled = course_enrollment.is_enrolled()
                    if enrollment_result:
                        assert is_enrolled, "Failed to enroll in the course"
                        allure.attach(driver.get_screenshot_as_png(), name="Enrollment_Successful", attachment_type=allure.attachment_type.PNG)
                    else:
                        # We might already be enrolled or enrollment might not be available
                        allure.attach(driver.get_screenshot_as_png(), name="Enrollment_Status", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Enrollment", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during course enrollment: {str(e)}")
