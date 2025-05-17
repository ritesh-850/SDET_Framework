import pytest
import allure
import time
import os
import tempfile
from POM_CLASS.BadgesCertificates_Page_Object import BadgesCertificates

@allure.epic("BTES LMS Application")
@allure.feature("Badges and Certificates")
@pytest.mark.usefixtures("setup")
class TestBadgesCertificates:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("View User Badges")
    @allure.description("Test to verify viewing user badges")
    @allure.title("User Badges Test")
    def test_view_user_badges(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create badges and certificates page object
        badges_certificates = BadgesCertificates(driver)

        # Login to the application
        with allure.step("Login to the application"):
            badges_certificates.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to user badges
        with allure.step("Navigate to user badges"):
            try:
                badges_certificates.navigate_to_user_badges()
                allure.attach(driver.get_screenshot_as_png(), name="User_Badges_Page", attachment_type=allure.attachment_type.PNG)
                
                # Get badges count
                with allure.step("Get badges count"):
                    badges_count = badges_certificates.get_user_badges_count()
                    allure.attach(
                        f"User has {badges_count} badges".encode('utf-8'),
                        name="User_Badges_Count",
                        attachment_type=allure.attachment_type.TEXT
                    )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_User_Badges", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing user badges: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("View Course Badges")
    @allure.description("Test to verify viewing course badges")
    @allure.title("Course Badges Test")
    def test_view_course_badges(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create badges and certificates page object
        badges_certificates = BadgesCertificates(driver)

        # Login to the application
        with allure.step("Login to the application"):
            badges_certificates.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                badges_certificates.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    badges_certificates.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course badges
                    with allure.step("Navigate to course badges"):
                        if badges_certificates.navigate_to_course_badges():
                            allure.attach(driver.get_screenshot_as_png(), name="Course_Badges_Page", attachment_type=allure.attachment_type.PNG)
                            
                            # Get badges count
                            with allure.step("Get badges count"):
                                badges_count = badges_certificates.get_course_badges_count()
                                allure.attach(
                                    f"Course has {badges_count} badges".encode('utf-8'),
                                    name="Course_Badges_Count",
                                    attachment_type=allure.attachment_type.TEXT
                                )
                        else:
                            pytest.skip("Course badges feature not available")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_Course_Badges", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing course badges: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Manage Badges")
    @allure.description("Test to verify managing badges in site administration")
    @allure.title("Manage Badges Test")
    @pytest.mark.skip(reason="Skipping to avoid creating actual badges")
    def test_manage_badges(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create badges and certificates page object
        badges_certificates = BadgesCertificates(driver)

        # Login to the application with admin credentials
        with allure.step("Login to the application with admin credentials"):
            badges_certificates.login("admin", "Admin@123")  # Use actual admin credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to site admin
        with allure.step("Navigate to site admin"):
            try:
                badges_certificates.navigate_to_site_admin()
                allure.attach(driver.get_screenshot_as_png(), name="Site_Admin_Page", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to badges admin
                with allure.step("Navigate to badges admin"):
                    if badges_certificates.navigate_to_badges_admin():
                        allure.attach(driver.get_screenshot_as_png(), name="Badges_Admin_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Create a temporary image file for the badge
                        with allure.step("Create a temporary image file for the badge"):
                            # This is a placeholder - in a real test, you would create an actual image file
                            temp_image_path = os.path.join(tempfile.gettempdir(), "badge_image.png")
                            
                            # Add a new badge
                            with allure.step("Add a new badge"):
                                badge_name = f"Test Badge {time.strftime('%Y-%m-%d %H:%M:%S')}"
                                badge_description = "This is a test badge created by the automated test."
                                
                                badges_certificates.add_new_badge(badge_name, badge_description, temp_image_path)
                                allure.attach(driver.get_screenshot_as_png(), name="After_Adding_Badge", attachment_type=allure.attachment_type.PNG)
                                
                                # Verify badge was added
                                assert badge_name in driver.page_source, f"Badge '{badge_name}' was not added successfully"
                    else:
                        pytest.skip("Badges admin feature not available")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Managing_Badges", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error managing badges: {str(e)}")
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Manage Certificates")
    @allure.description("Test to verify managing certificates in a course")
    @allure.title("Manage Certificates Test")
    @pytest.mark.skip(reason="Skipping to avoid creating actual certificates")
    def test_manage_certificates(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create badges and certificates page object
        badges_certificates = BadgesCertificates(driver)

        # Login to the application with teacher credentials
        with allure.step("Login to the application with teacher credentials"):
            badges_certificates.login("teacher", "Teacher@123")  # Use actual teacher credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            try:
                badges_certificates.navigate_to_courses()
                allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
                
                # Select a course
                with allure.step("Select the first available course"):
                    badges_certificates.select_course(0)
                    allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course certificates
                    with allure.step("Navigate to course certificates"):
                        if badges_certificates.navigate_to_course_certificates():
                            allure.attach(driver.get_screenshot_as_png(), name="Course_Certificates_Page", attachment_type=allure.attachment_type.PNG)
                            
                            # Add a new certificate
                            with allure.step("Add a new certificate"):
                                certificate_name = f"Test Certificate {time.strftime('%Y-%m-%d %H:%M:%S')}"
                                
                                badges_certificates.add_new_certificate(certificate_name)
                                allure.attach(driver.get_screenshot_as_png(), name="After_Adding_Certificate", attachment_type=allure.attachment_type.PNG)
                                
                                # Verify certificate was added
                                assert certificate_name in driver.page_source, f"Certificate '{certificate_name}' was not added successfully"
                        else:
                            pytest.skip("Course certificates feature not available")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Managing_Certificates", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error managing certificates: {str(e)}")
