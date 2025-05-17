import pytest
import allure
import os
import tempfile
from POM_CLASS.Assignment_Page_Object import Assignment

@allure.epic("BTES LMS Application")
@allure.feature("Assignment Submission")
@pytest.mark.usefixtures("setup")
class TestAssignment:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Submit Assignment with File Upload")
    @allure.description("Test to verify assignment submission with file upload")
    @allure.title("Assignment File Upload Test")
    def test_assignment_file_upload(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create assignment page object
        assignment = Assignment(driver)

        # Login to the application
        with allure.step("Login to the application"):
            assignment.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            assignment.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                assignment.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Open an assignment
                with allure.step("Open the first available assignment"):
                    if assignment.open_assignment(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Assignment_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Click Add submission button
                        with allure.step("Click Add/Edit submission button"):
                            if assignment.click_add_submission():
                                allure.attach(driver.get_screenshot_as_png(), name="Submission_Form", attachment_type=allure.attachment_type.PNG)
                                
                                # Create a temporary file for upload
                                with allure.step("Create a temporary file for upload"):
                                    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
                                        temp.write(b"This is a test submission file created by the automated test.")
                                        temp_file_path = temp.name
                                
                                # Upload the file
                                with allure.step(f"Upload file: {temp_file_path}"):
                                    if assignment.upload_file(temp_file_path):
                                        allure.attach(driver.get_screenshot_as_png(), name="After_File_Upload", attachment_type=allure.attachment_type.PNG)
                                        
                                        # Submit the assignment
                                        with allure.step("Submit the assignment"):
                                            if assignment.submit_assignment():
                                                allure.attach(driver.get_screenshot_as_png(), name="After_Submission", attachment_type=allure.attachment_type.PNG)
                                                
                                                # Get submission status
                                                with allure.step("Get submission status"):
                                                    status = assignment.get_submission_status()
                                                    allure.attach(
                                                        status.encode('utf-8'),
                                                        name="Submission_Status",
                                                        attachment_type=allure.attachment_type.TEXT
                                                    )
                                                    
                                                    # Verify submission was successful
                                                    assert "submitted" in status.lower() or "submission" in status.lower(), "Submission status does not indicate success"
                                            else:
                                                pytest.fail("Failed to submit the assignment")
                                    else:
                                        pytest.fail("Failed to upload file")
                                
                                # Clean up the temporary file
                                os.unlink(temp_file_path)
                            else:
                                pytest.fail("Failed to click Add/Edit submission button")
                    else:
                        pytest.skip("No assignments found in the course")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Submission", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during assignment submission: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Submit Assignment with Online Text")
    @allure.description("Test to verify assignment submission with online text")
    @allure.title("Assignment Online Text Test")
    def test_assignment_online_text(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create assignment page object
        assignment = Assignment(driver)

        # Login to the application
        with allure.step("Login to the application"):
            assignment.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            assignment.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                assignment.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Open an assignment
                with allure.step("Open the first available assignment"):
                    if assignment.open_assignment(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Assignment_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Click Add submission button
                        with allure.step("Click Add/Edit submission button"):
                            if assignment.click_add_submission():
                                allure.attach(driver.get_screenshot_as_png(), name="Submission_Form", attachment_type=allure.attachment_type.PNG)
                                
                                # Enter online text
                                with allure.step("Enter online text"):
                                    online_text = "This is a test submission created by the automated test. It demonstrates the ability to submit assignments with online text."
                                    if assignment.enter_online_text(online_text):
                                        allure.attach(driver.get_screenshot_as_png(), name="After_Text_Entry", attachment_type=allure.attachment_type.PNG)
                                        
                                        # Submit the assignment
                                        with allure.step("Submit the assignment"):
                                            if assignment.submit_assignment():
                                                allure.attach(driver.get_screenshot_as_png(), name="After_Submission", attachment_type=allure.attachment_type.PNG)
                                                
                                                # Get submission status
                                                with allure.step("Get submission status"):
                                                    status = assignment.get_submission_status()
                                                    allure.attach(
                                                        status.encode('utf-8'),
                                                        name="Submission_Status",
                                                        attachment_type=allure.attachment_type.TEXT
                                                    )
                                                    
                                                    # Verify submission was successful
                                                    assert "submitted" in status.lower() or "submission" in status.lower(), "Submission status does not indicate success"
                                            else:
                                                pytest.fail("Failed to submit the assignment")
                                    else:
                                        pytest.fail("Failed to enter online text")
                            else:
                                pytest.fail("Failed to click Add/Edit submission button")
                    else:
                        pytest.skip("No assignments found in the course")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Submission", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during assignment submission: {str(e)}")
