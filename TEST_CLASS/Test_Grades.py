import pytest
import allure
from POM_CLASS.Grades_Page_Object import Grades

@allure.epic("BTES LMS Application")
@allure.feature("Grade Viewing")
@pytest.mark.usefixtures("setup")
class TestGrades:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("View Course Grades")
    @allure.description("Test to verify grade viewing functionality")
    @allure.title("Grade Viewing Test")
    def test_view_grades(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create grades page object
        grades = Grades(driver)

        # Login to the application
        with allure.step("Login to the application"):
            grades.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to grades
        with allure.step("Navigate to grades page"):
            try:
                grades.navigate_to_grades()
                allure.attach(driver.get_screenshot_as_png(), name="Grades_Page", attachment_type=allure.attachment_type.PNG)
                
                # Get grade items
                with allure.step("Get grade items"):
                    grade_items = grades.get_grade_items()
                    allure.attach(
                        f"Found {len(grade_items)} grade items".encode('utf-8'),
                        name="Grade_Items_Count",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Get grade item names
                with allure.step("Get grade item names"):
                    names = grades.get_grade_item_names()
                    allure.attach(
                        "\n".join(names).encode('utf-8'),
                        name="Grade_Item_Names",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Get grade item values
                with allure.step("Get grade item values"):
                    values = grades.get_grade_item_values()
                    allure.attach(
                        "\n".join(values).encode('utf-8'),
                        name="Grade_Item_Values",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Get grades as dictionary
                with allure.step("Get grades as dictionary"):
                    grades_dict = grades.get_grades_as_dict()
                    grades_str = "\n".join([f"{key}: {value}" for key, value in grades_dict.items()])
                    allure.attach(
                        grades_str.encode('utf-8'),
                        name="Grades_Dictionary",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Get course total grade
                with allure.step("Get course total grade"):
                    total_grade = grades.get_course_total_grade()
                    allure.attach(
                        f"Course Total Grade: {total_grade}".encode('utf-8'),
                        name="Course_Total_Grade",
                        attachment_type=allure.attachment_type.TEXT
                    )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_Grades", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing grades: {str(e)}")
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("View Course Specific Grades")
    @allure.description("Test to verify course specific grade viewing")
    @allure.title("Course Specific Grade Test")
    def test_view_course_specific_grades(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create grades page object
        grades = Grades(driver)

        # Login to the application
        with allure.step("Login to the application"):
            grades.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            grades.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                grades.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Navigate to grades
                with allure.step("Navigate to grades page"):
                    grades.navigate_to_grades()
                    allure.attach(driver.get_screenshot_as_png(), name="Course_Grades_Page", attachment_type=allure.attachment_type.PNG)
                    
                    # Get grade items
                    with allure.step("Get grade items for the course"):
                        grade_items = grades.get_grade_items()
                        allure.attach(
                            f"Found {len(grade_items)} grade items for the course".encode('utf-8'),
                            name="Course_Grade_Items_Count",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    
                    # Get grades as dictionary
                    with allure.step("Get grades as dictionary for the course"):
                        grades_dict = grades.get_grades_as_dict()
                        grades_str = "\n".join([f"{key}: {value}" for key, value in grades_dict.items()])
                        allure.attach(
                            grades_str.encode('utf-8'),
                            name="Course_Grades_Dictionary",
                            attachment_type=allure.attachment_type.TEXT
                        )
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Viewing_Course_Grades", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error viewing course grades: {str(e)}")
