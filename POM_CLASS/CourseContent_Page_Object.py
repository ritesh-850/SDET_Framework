from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CourseContent:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for course content
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    section_xpath = "//li[contains(@class, 'section')]"
    activity_xpath = "//li[contains(@class, 'activity')]"
    module_title_xpath = "//h3[contains(@class, 'sectionname')]"
    resource_link_xpath = "//span[contains(@class, 'instancename')]"
    next_section_button_xpath = "//a[contains(@class, 'next_section')]"
    previous_section_button_xpath = "//a[contains(@class, 'previous_section')]"
    
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
    
    def get_section_count(self):
        # Get the number of sections in the course
        sections = self.driver.find_elements(By.XPATH, self.section_xpath)
        return len(sections)
    
    def get_section_titles(self):
        # Get the titles of all sections
        titles = self.driver.find_elements(By.XPATH, self.module_title_xpath)
        return [title.text for title in titles]
    
    def select_section(self, section_index=0):
        # Select a section by index
        sections = self.driver.find_elements(By.XPATH, self.section_xpath)
        if len(sections) > section_index:
            sections[section_index].click()
            return True
        return False
    
    def get_activities_in_section(self, section_index=0):
        # Get all activities in a section
        sections = self.driver.find_elements(By.XPATH, self.section_xpath)
        if len(sections) > section_index:
            activities = sections[section_index].find_elements(By.XPATH, f".{self.activity_xpath}")
            return activities
        return []
    
    def select_activity(self, section_index=0, activity_index=0):
        # Select an activity in a section
        activities = self.get_activities_in_section(section_index)
        if len(activities) > activity_index:
            activities[activity_index].click()
            return True
        return False
    
    def navigate_to_next_section(self):
        # Navigate to the next section
        try:
            next_button = self.driver.find_element(By.XPATH, self.next_section_button_xpath)
            next_button.click()
            return True
        except:
            return False
    
    def navigate_to_previous_section(self):
        # Navigate to the previous section
        try:
            prev_button = self.driver.find_element(By.XPATH, self.previous_section_button_xpath)
            prev_button.click()
            return True
        except:
            return False
    
    def open_resource(self, resource_name):
        # Open a resource by name
        try:
            resource = self.driver.find_element(By.XPATH, f"{self.resource_link_xpath}[contains(text(), '{resource_name}')]")
            resource.click()
            return True
        except:
            return False
