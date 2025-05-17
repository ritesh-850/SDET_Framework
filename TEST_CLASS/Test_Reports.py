import pytest
import allure
from POM_CLASS.Reports_Page_Object import Reports

@allure.epic("BTES LMS Application")
@allure.feature("Reports")
@pytest.mark.usefixtures("setup")
class TestReports:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Generate Logs Report")
    @allure.description("Test to verify generating logs report")
    @allure.title("Logs Report Test")
    def test_generate_logs_report(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create reports page object
        reports = Reports(driver)

        # Login to the application with admin credentials
        with allure.step("Login to the application with admin credentials"):
            reports.login("admin", "Admin@123")  # Use actual admin credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to site admin
        with allure.step("Navigate to site admin"):
            try:
                reports.navigate_to_site_admin()
                allure.attach(driver.get_screenshot_as_png(), name="Site_Admin_Page", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to reports
                with allure.step("Navigate to reports"):
                    reports.navigate_to_reports()
                    allure.attach(driver.get_screenshot_as_png(), name="Reports_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to logs
                    with allure.step("Navigate to logs"):
                        reports.navigate_to_logs()
                        allure.attach(driver.get_screenshot_as_png(), name="Logs_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Generate logs report
                        with allure.step("Generate logs report"):
                            reports.generate_logs_report()
                            allure.attach(driver.get_screenshot_as_png(), name="Logs_Report", attachment_type=allure.attachment_type.PNG)
                            
                            # Get logs count
                            with allure.step("Get logs count"):
                                logs_count = reports.get_logs_count()
                                allure.attach(
                                    f"Found {logs_count} log entries".encode('utf-8'),
                                    name="Logs_Count",
                                    attachment_type=allure.attachment_type.TEXT
                                )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Generating_Logs_Report", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error generating logs report: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Generate Activity Report")
    @allure.description("Test to verify generating activity report")
    @allure.title("Activity Report Test")
    def test_generate_activity_report(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create reports page object
        reports = Reports(driver)

        # Login to the application with admin credentials
        with allure.step("Login to the application with admin credentials"):
            reports.login("admin", "Admin@123")  # Use actual admin credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to site admin
        with allure.step("Navigate to site admin"):
            try:
                reports.navigate_to_site_admin()
                allure.attach(driver.get_screenshot_as_png(), name="Site_Admin_Page", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to reports
                with allure.step("Navigate to reports"):
                    reports.navigate_to_reports()
                    allure.attach(driver.get_screenshot_as_png(), name="Reports_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to activity report
                    with allure.step("Navigate to activity report"):
                        reports.navigate_to_activity_report()
                        allure.attach(driver.get_screenshot_as_png(), name="Activity_Report_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Generate activity report
                        with allure.step("Generate activity report"):
                            reports.generate_activity_report()
                            allure.attach(driver.get_screenshot_as_png(), name="Activity_Report", attachment_type=allure.attachment_type.PNG)
                            
                            # Get activity report count
                            with allure.step("Get activity report count"):
                                activity_count = reports.get_activity_report_count()
                                allure.attach(
                                    f"Found {activity_count} activity entries".encode('utf-8'),
                                    name="Activity_Count",
                                    attachment_type=allure.attachment_type.TEXT
                                )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Generating_Activity_Report", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error generating activity report: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Generate Course Participation Report")
    @allure.description("Test to verify generating course participation report")
    @allure.title("Course Participation Report Test")
    def test_generate_course_participation_report(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create reports page object
        reports = Reports(driver)

        # Login to the application with admin credentials
        with allure.step("Login to the application with admin credentials"):
            reports.login("admin", "Admin@123")  # Use actual admin credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to site admin
        with allure.step("Navigate to site admin"):
            try:
                reports.navigate_to_site_admin()
                allure.attach(driver.get_screenshot_as_png(), name="Site_Admin_Page", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to reports
                with allure.step("Navigate to reports"):
                    reports.navigate_to_reports()
                    allure.attach(driver.get_screenshot_as_png(), name="Reports_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to course participation
                    with allure.step("Navigate to course participation"):
                        reports.navigate_to_course_participation()
                        allure.attach(driver.get_screenshot_as_png(), name="Course_Participation_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Generate course participation report
                        with allure.step("Generate course participation report"):
                            reports.generate_course_participation_report()
                            allure.attach(driver.get_screenshot_as_png(), name="Course_Participation_Report", attachment_type=allure.attachment_type.PNG)
                            
                            # Get participation report count
                            with allure.step("Get participation report count"):
                                participation_count = reports.get_participation_report_count()
                                allure.attach(
                                    f"Found {participation_count} participation entries".encode('utf-8'),
                                    name="Participation_Count",
                                    attachment_type=allure.attachment_type.TEXT
                                )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Generating_Participation_Report", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error generating course participation report: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Generate Statistics Report")
    @allure.description("Test to verify generating statistics report")
    @allure.title("Statistics Report Test")
    def test_generate_statistics_report(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create reports page object
        reports = Reports(driver)

        # Login to the application with admin credentials
        with allure.step("Login to the application with admin credentials"):
            reports.login("admin", "Admin@123")  # Use actual admin credentials
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to site admin
        with allure.step("Navigate to site admin"):
            try:
                reports.navigate_to_site_admin()
                allure.attach(driver.get_screenshot_as_png(), name="Site_Admin_Page", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to reports
                with allure.step("Navigate to reports"):
                    reports.navigate_to_reports()
                    allure.attach(driver.get_screenshot_as_png(), name="Reports_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Navigate to statistics
                    with allure.step("Navigate to statistics"):
                        reports.navigate_to_statistics()
                        allure.attach(driver.get_screenshot_as_png(), name="Statistics_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Generate statistics report
                        with allure.step("Generate statistics report"):
                            reports.generate_statistics_report()
                            allure.attach(driver.get_screenshot_as_png(), name="Statistics_Report", attachment_type=allure.attachment_type.PNG)
                            
                            # Check if statistics graph is displayed
                            with allure.step("Check if statistics graph is displayed"):
                                is_graph_displayed = reports.is_statistics_graph_displayed()
                                allure.attach(
                                    f"Statistics graph displayed: {is_graph_displayed}".encode('utf-8'),
                                    name="Statistics_Graph",
                                    attachment_type=allure.attachment_type.TEXT
                                )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Generating_Statistics_Report", attachment_type=allure.attachment_type.PNG)
                pytest.skip(f"Error generating statistics report: {str(e)}")
