from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Quiz:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for quizzes
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    quiz_link_xpath = "//span[contains(@class, 'instancename') and contains(text(), 'Quiz')]"
    attempt_quiz_button_xpath = "//button[contains(text(), 'Attempt quiz now')]"
    start_attempt_button_xpath = "//button[contains(text(), 'Start attempt')]"
    
    # Locators for quiz questions
    multiple_choice_option_xpath = "//input[@type='radio']"
    checkbox_option_xpath = "//input[@type='checkbox']"
    text_answer_xpath = "//textarea[contains(@class, 'answer')]"
    dropdown_xpath = "//select[contains(@class, 'select')]"
    
    # Locators for navigation within quiz
    next_page_button_xpath = "//input[@value='Next page']"
    previous_page_button_xpath = "//input[@value='Previous page']"
    finish_attempt_button_xpath = "//button[contains(text(), 'Finish attempt')]"
    submit_all_button_xpath = "//button[contains(text(), 'Submit all and finish')]"
    confirm_submit_button_xpath = "//button[contains(text(), 'Submit all and finish')]"
    
    # Locators for quiz results
    quiz_results_xpath = "//div[contains(@class, 'quizreviewsummary')]"
    quiz_grade_xpath = "//th[contains(text(), 'Grade')]/following-sibling::td"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_courses(self):
        self.driver.find_element(By.XPATH, self.btn_sidebar_xpath).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_courses_xpath)))
        self.driver.find_element(By.XPATH, self.btn_courses_xpath).click()
    
    def select_course(self, course_index=0):
        # Select a course by index (0 for the first course)
        courses = self.driver.find_elements(By.XPATH, self.course_card_xpath)
        if len(courses) > course_index:
            courses[course_index].click()
        else:
            raise Exception(f"Course with index {course_index} not found")
    
    def open_quiz(self, quiz_index=0):
        # Open a quiz by index
        quizzes = self.driver.find_elements(By.XPATH, self.quiz_link_xpath)
        if len(quizzes) > quiz_index:
            quizzes[quiz_index].click()
            return True
        return False
    
    def start_quiz_attempt(self):
        # Click on Attempt quiz now button
        try:
            attempt_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.attempt_quiz_button_xpath)))
            attempt_button.click()
            
            # Click on Start attempt button if it appears
            try:
                start_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.start_attempt_button_xpath)))
                start_button.click()
            except:
                # Start attempt button might not appear, which is fine
                pass
                
            return True
        except:
            return False
    
    def answer_multiple_choice_question(self, option_index=0):
        # Select an option in a multiple choice question
        try:
            options = self.driver.find_elements(By.XPATH, self.multiple_choice_option_xpath)
            if len(options) > option_index:
                options[option_index].click()
                return True
            return False
        except:
            return False
    
    def answer_checkbox_question(self, option_indices=[0]):
        # Select options in a checkbox question
        try:
            options = self.driver.find_elements(By.XPATH, self.checkbox_option_xpath)
            for index in option_indices:
                if len(options) > index:
                    options[index].click()
            return True
        except:
            return False
    
    def answer_text_question(self, answer_text):
        # Enter text in a text question
        try:
            text_field = self.driver.find_element(By.XPATH, self.text_answer_xpath)
            text_field.clear()
            text_field.send_keys(answer_text)
            return True
        except:
            return False
    
    def answer_dropdown_question(self, option_index=1):
        # Select an option in a dropdown question
        try:
            dropdown = Select(self.driver.find_element(By.XPATH, self.dropdown_xpath))
            dropdown.select_by_index(option_index)
            return True
        except:
            return False
    
    def navigate_to_next_page(self):
        # Navigate to the next page in the quiz
        try:
            next_button = self.driver.find_element(By.XPATH, self.next_page_button_xpath)
            next_button.click()
            return True
        except:
            return False
    
    def navigate_to_previous_page(self):
        # Navigate to the previous page in the quiz
        try:
            prev_button = self.driver.find_element(By.XPATH, self.previous_page_button_xpath)
            prev_button.click()
            return True
        except:
            return False
    
    def finish_quiz_attempt(self):
        # Finish the quiz attempt
        try:
            finish_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.finish_attempt_button_xpath)))
            finish_button.click()
            
            # Click on Submit all and finish button
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.submit_all_button_xpath)))
            submit_button.click()
            
            # Confirm submission
            confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.confirm_submit_button_xpath)))
            confirm_button.click()
            
            return True
        except Exception as e:
            print(f"Error finishing quiz: {str(e)}")
            return False
    
    def get_quiz_results(self):
        # Get the quiz results
        try:
            results_element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.quiz_results_xpath)))
            return results_element.text
        except:
            return "Results not found"
    
    def get_quiz_grade(self):
        # Get the quiz grade
        try:
            grade_element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.quiz_grade_xpath)))
            return grade_element.text
        except:
            return "Grade not found"
