from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class CourseManagement:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for course management
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    course_settings_link_xpath = "//a[contains(@href, 'edit') and contains(text(), 'Edit settings')]"
    course_participants_link_xpath = "//a[contains(@href, 'participants') and contains(text(), 'Participants')]"
    course_grades_link_xpath = "//a[contains(@href, 'grade') and contains(text(), 'Grades')]"
    course_completion_link_xpath = "//a[contains(@href, 'completion') and contains(text(), 'Course completion')]"
    
    # Locators for course settings
    course_name_field_id = "id_fullname"
    course_shortname_field_id = "id_shortname"
    course_visibility_select_id = "id_visible"
    save_course_button_xpath = "//input[@type='submit' and @value='Save and display']"
    
    # Locators for course content
    add_activity_button_xpath = "//button[contains(@class, 'activity-add')]"
    activity_type_xpath = "//div[contains(@class, 'option') and contains(text(), '{0}')]"  # Format with activity type
    activity_name_field_id = "id_name"
    activity_description_iframe_xpath = "//iframe[contains(@id, 'id_introeditor')]"
    save_activity_button_xpath = "//input[@type='submit' and @value='Save and return to course']"
    
    # Locators for participants
    enrol_users_button_xpath = "//button[contains(@class, 'enrol-users-button')]"
    user_search_field_xpath = "//input[contains(@class, 'user-search')]"
    user_checkbox_xpath = "//input[@type='checkbox' and @name='userids[]']"
    enrol_users_submit_button_xpath = "//input[@type='submit' and @value='Enrol users']"
    
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
    
    def navigate_to_course_settings(self):
        # Click on Edit settings link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_settings_link_xpath)))
        self.driver.find_element(By.XPATH, self.course_settings_link_xpath).click()
    
    def navigate_to_course_participants(self):
        # Click on Participants link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_participants_link_xpath)))
        self.driver.find_element(By.XPATH, self.course_participants_link_xpath).click()
    
    def navigate_to_course_grades(self):
        # Click on Grades link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_grades_link_xpath)))
        self.driver.find_element(By.XPATH, self.course_grades_link_xpath).click()
    
    def navigate_to_course_completion(self):
        # Click on Course completion link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_completion_link_xpath)))
        self.driver.find_element(By.XPATH, self.course_completion_link_xpath).click()
    
    def update_course_settings(self, course_name=None, course_shortname=None, course_visibility=None):
        # Update course name if provided
        if course_name:
            course_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.course_name_field_id)))
            course_name_field.clear()
            course_name_field.send_keys(course_name)
        
        # Update course shortname if provided
        if course_shortname:
            course_shortname_field = self.driver.find_element(By.ID, self.course_shortname_field_id)
            course_shortname_field.clear()
            course_shortname_field.send_keys(course_shortname)
        
        # Update course visibility if provided
        if course_visibility:
            visibility_select = Select(self.driver.find_element(By.ID, self.course_visibility_select_id))
            visibility_select.select_by_visible_text(course_visibility)
        
        # Save course settings
        self.driver.find_element(By.XPATH, self.save_course_button_xpath).click()
    
    def add_activity(self, activity_type, activity_name, activity_description):
        # Click on Add activity button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_activity_button_xpath)))
        self.driver.find_element(By.XPATH, self.add_activity_button_xpath).click()
        
        # Select activity type
        activity_type_xpath = self.activity_type_xpath.format(activity_type)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, activity_type_xpath)))
        self.driver.find_element(By.XPATH, activity_type_xpath).click()
        
        # Enter activity name
        activity_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.activity_name_field_id)))
        activity_name_field.clear()
        activity_name_field.send_keys(activity_name)
        
        # Enter activity description
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.activity_description_iframe_xpath)))
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        body.send_keys(activity_description)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
        
        # Save activity
        self.driver.find_element(By.XPATH, self.save_activity_button_xpath).click()
    
    def enrol_users(self, search_term):
        # Click on Enrol users button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.enrol_users_button_xpath)))
        self.driver.find_element(By.XPATH, self.enrol_users_button_xpath).click()
        
        # Search for users
        search_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.user_search_field_xpath)))
        search_field.clear()
        search_field.send_keys(search_term)
        
        # Wait for search results
        time.sleep(2)
        
        # Select the first user
        checkboxes = self.driver.find_elements(By.XPATH, self.user_checkbox_xpath)
        if len(checkboxes) > 0:
            checkboxes[0].click()
            
            # Click Enrol users button
            self.driver.find_element(By.XPATH, self.enrol_users_submit_button_xpath).click()
            return True
        
        return False
    
    def get_course_name(self):
        # Get the current course name
        try:
            self.navigate_to_course_settings()
            course_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.course_name_field_id)))
            return course_name_field.get_attribute("value")
        except:
            return "Course name not found"
    
    def get_participant_count(self):
        # Get the number of participants in the course
        try:
            self.navigate_to_course_participants()
            # Wait for participants table to load
            time.sleep(2)
            # Count participant rows
            participant_rows = self.driver.find_elements(By.XPATH, "//table[contains(@class, 'participants')]//tr")
            # Subtract 1 for the header row
            return len(participant_rows) - 1
        except:
            return 0
