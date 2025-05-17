from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CourseEnrollment:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for course enrollment
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    enroll_button_xpath = "//button[contains(text(), 'Enrol me')]"
    continue_button_xpath = "//button[contains(text(), 'Continue')]"
    
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
    
    def enroll_in_course(self):
        try:
            # Try to find and click the enroll button
            enroll_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.enroll_button_xpath)))
            enroll_button.click()
            
            # Click continue if it appears
            try:
                continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.continue_button_xpath)))
                continue_button.click()
            except:
                # Continue button might not appear, which is fine
                pass
                
            return True
        except:
            # Course might already be enrolled or not available for enrollment
            return False
    
    def is_enrolled(self):
        # Check if we're enrolled in the course
        page_source = self.driver.page_source.lower()
        return "you are enrolled in this course" in page_source or "enrolled" in page_source
