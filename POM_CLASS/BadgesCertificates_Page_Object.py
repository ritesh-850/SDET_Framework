from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os

class BadgesCertificates:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for badges
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    badges_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Badges')]"
    
    # Locators for course badges
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    course_badges_link_xpath = "//a[contains(@href, 'badges') and contains(text(), 'Badges')]"
    
    # Locators for site administration badges
    site_admin_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Site administration')]"
    badges_admin_link_xpath = "//a[contains(@href, 'badges') and contains(text(), 'Badges')]"
    manage_badges_link_xpath = "//a[contains(@href, 'badges') and contains(text(), 'Manage badges')]"
    add_badge_button_xpath = "//a[contains(@href, 'newbadge') and contains(text(), 'Add a new badge')]"
    
    # Locators for adding a badge
    badge_name_field_id = "id_name"
    badge_description_iframe_xpath = "//iframe[contains(@id, 'id_description')]"
    badge_image_field_xpath = "//input[@type='file' and @name='imagefile']"
    badge_criteria_link_xpath = "//a[contains(@href, 'criteria')]"
    badge_criteria_role_checkbox_xpath = "//input[@type='checkbox' and @name='criteria_role[]']"
    badge_criteria_save_button_xpath = "//input[@type='submit' and @value='Save']"
    badge_enable_button_xpath = "//input[@type='submit' and @value='Enable access']"
    
    # Locators for certificates
    course_certificates_link_xpath = "//a[contains(@href, 'certificate') and contains(text(), 'Certificate')]"
    add_certificate_button_xpath = "//a[contains(@href, 'editcertificate') and contains(text(), 'Add a new certificate')]"
    certificate_name_field_id = "id_name"
    certificate_save_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
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
    
    def navigate_to_user_badges(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Badges link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.badges_link_xpath)))
        self.driver.find_element(By.XPATH, self.badges_link_xpath).click()
    
    def select_course(self, course_index=0):
        # Select a course by index (0 for the first course)
        courses = self.driver.find_elements(By.XPATH, self.course_card_xpath)
        if len(courses) > course_index:
            courses[course_index].click()
        else:
            raise Exception(f"Course with index {course_index} not found")
    
    def navigate_to_course_badges(self):
        # Click on Badges link in course
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_badges_link_xpath)))
            self.driver.find_element(By.XPATH, self.course_badges_link_xpath).click()
            return True
        except:
            return False
    
    def navigate_to_site_admin(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Site administration link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.site_admin_link_xpath)))
        self.driver.find_element(By.XPATH, self.site_admin_link_xpath).click()
    
    def navigate_to_badges_admin(self):
        # Click on Badges link in admin
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.badges_admin_link_xpath)))
            self.driver.find_element(By.XPATH, self.badges_admin_link_xpath).click()
            
            # Click on Manage badges link
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.manage_badges_link_xpath)))
            self.driver.find_element(By.XPATH, self.manage_badges_link_xpath).click()
            return True
        except:
            return False
    
    def add_new_badge(self, badge_name, badge_description, image_path):
        # Click on Add a new badge button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_badge_button_xpath)))
        self.driver.find_element(By.XPATH, self.add_badge_button_xpath).click()
        
        # Enter badge name
        badge_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.badge_name_field_id)))
        badge_name_field.clear()
        badge_name_field.send_keys(badge_name)
        
        # Enter badge description
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.badge_description_iframe_xpath)))
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        body.send_keys(badge_description)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
        
        # Upload badge image
        if os.path.exists(image_path):
            self.driver.find_element(By.XPATH, self.badge_image_field_xpath).send_keys(image_path)
        
        # Save badge details
        self.driver.find_element(By.XPATH, self.badge_criteria_save_button_xpath).click()
        
        # Set badge criteria
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.badge_criteria_link_xpath)))
        self.driver.find_element(By.XPATH, self.badge_criteria_link_xpath).click()
        
        # Select a role criteria
        checkboxes = self.driver.find_elements(By.XPATH, self.badge_criteria_role_checkbox_xpath)
        if len(checkboxes) > 0:
            checkboxes[0].click()
        
        # Save criteria
        self.driver.find_element(By.XPATH, self.badge_criteria_save_button_xpath).click()
        
        # Enable badge
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.badge_enable_button_xpath)))
        self.driver.find_element(By.XPATH, self.badge_enable_button_xpath).click()
    
    def navigate_to_course_certificates(self):
        # Click on Certificate link in course
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_certificates_link_xpath)))
            self.driver.find_element(By.XPATH, self.course_certificates_link_xpath).click()
            return True
        except:
            return False
    
    def add_new_certificate(self, certificate_name):
        # Click on Add a new certificate button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_certificate_button_xpath)))
        self.driver.find_element(By.XPATH, self.add_certificate_button_xpath).click()
        
        # Enter certificate name
        certificate_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.certificate_name_field_id)))
        certificate_name_field.clear()
        certificate_name_field.send_keys(certificate_name)
        
        # Save certificate
        self.driver.find_element(By.XPATH, self.certificate_save_button_xpath).click()
    
    def get_user_badges_count(self):
        # Get the number of badges for the user
        try:
            self.navigate_to_user_badges()
            # Wait for badges to load
            time.sleep(2)
            # Count badge elements
            badges = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'badge')]")
            return len(badges)
        except:
            return 0
    
    def get_course_badges_count(self):
        # Get the number of badges for the course
        try:
            if self.navigate_to_course_badges():
                # Wait for badges to load
                time.sleep(2)
                # Count badge elements
                badges = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'badge')]")
                return len(badges)
            return 0
        except:
            return 0
