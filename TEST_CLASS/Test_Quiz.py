import pytest
import allure
from POM_CLASS.Quiz_Page_Object import Quiz

@allure.epic("BTES LMS Application")
@allure.feature("Quiz Taking")
@pytest.mark.usefixtures("setup")
class TestQuiz:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Complete Quiz")
    @allure.description("Test to verify quiz taking functionality")
    @allure.title("Quiz Taking Test")
    def test_take_quiz(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create quiz page object
        quiz = Quiz(driver)

        # Login to the application
        with allure.step("Login to the application"):
            quiz.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to courses
        with allure.step("Navigate to courses page"):
            quiz.navigate_to_courses()
            allure.attach(driver.get_screenshot_as_png(), name="Courses_Page", attachment_type=allure.attachment_type.PNG)
        
        # Select a course
        with allure.step("Select the first available course"):
            try:
                quiz.select_course(0)
                allure.attach(driver.get_screenshot_as_png(), name="Selected_Course", attachment_type=allure.attachment_type.PNG)
                
                # Open a quiz
                with allure.step("Open the first available quiz"):
                    if quiz.open_quiz(0):
                        allure.attach(driver.get_screenshot_as_png(), name="Quiz_Page", attachment_type=allure.attachment_type.PNG)
                        
                        # Start quiz attempt
                        with allure.step("Start quiz attempt"):
                            if quiz.start_quiz_attempt():
                                allure.attach(driver.get_screenshot_as_png(), name="Quiz_Started", attachment_type=allure.attachment_type.PNG)
                                
                                # Answer questions
                                with allure.step("Answer multiple choice question"):
                                    quiz.answer_multiple_choice_question(0)
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Multiple_Choice", attachment_type=allure.attachment_type.PNG)
                                
                                with allure.step("Answer checkbox question"):
                                    quiz.answer_checkbox_question([0, 1])
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Checkbox", attachment_type=allure.attachment_type.PNG)
                                
                                with allure.step("Answer text question"):
                                    quiz.answer_text_question("This is a test answer provided by the automated test.")
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Text_Answer", attachment_type=allure.attachment_type.PNG)
                                
                                with allure.step("Answer dropdown question"):
                                    quiz.answer_dropdown_question(1)
                                    allure.attach(driver.get_screenshot_as_png(), name="After_Dropdown", attachment_type=allure.attachment_type.PNG)
                                
                                # Navigate through quiz pages
                                with allure.step("Navigate to next page"):
                                    if quiz.navigate_to_next_page():
                                        allure.attach(driver.get_screenshot_as_png(), name="Next_Page", attachment_type=allure.attachment_type.PNG)
                                        
                                        with allure.step("Navigate to previous page"):
                                            if quiz.navigate_to_previous_page():
                                                allure.attach(driver.get_screenshot_as_png(), name="Previous_Page", attachment_type=allure.attachment_type.PNG)
                                
                                # Finish quiz attempt
                                with allure.step("Finish quiz attempt"):
                                    if quiz.finish_quiz_attempt():
                                        allure.attach(driver.get_screenshot_as_png(), name="Quiz_Finished", attachment_type=allure.attachment_type.PNG)
                                        
                                        # Get quiz results
                                        with allure.step("Get quiz results"):
                                            results = quiz.get_quiz_results()
                                            allure.attach(
                                                results.encode('utf-8'),
                                                name="Quiz_Results",
                                                attachment_type=allure.attachment_type.TEXT
                                            )
                                        
                                        # Get quiz grade
                                        with allure.step("Get quiz grade"):
                                            grade = quiz.get_quiz_grade()
                                            allure.attach(
                                                grade.encode('utf-8'),
                                                name="Quiz_Grade",
                                                attachment_type=allure.attachment_type.TEXT
                                            )
                                    else:
                                        pytest.fail("Failed to finish quiz attempt")
                            else:
                                pytest.skip("Could not start quiz attempt")
                    else:
                        pytest.skip("No quizzes found in the course")
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Quiz", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during quiz taking: {str(e)}")
