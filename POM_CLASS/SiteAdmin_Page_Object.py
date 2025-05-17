from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class SiteAdmin:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    site_admin_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Site administration')]"
    
    # Locators for admin sections
    users_link_xpath = "//a[contains(@href, 'user') and contains(text(), 'Users')]"
    courses_link_xpath = "//a[contains(@href, 'course') and contains(text(), 'Courses')]"
    grades_link_xpath = "//a[contains(@href, 'grade') and contains(text(), 'Grades')]"
    plugins_link_xpath = "//a[contains(@href, 'plugins') and contains(text(), 'Plugins')]"
    appearance_link_xpath = "//a[contains(@href, 'appearance') and contains(text(), 'Appearance')]"
    server_link_xpath = "//a[contains(@href, 'server') and contains(text(), 'Server')]"
    reports_link_xpath = "//a[contains(@href, 'report') and contains(text(), 'Reports')]"
    
    # Locators for user management
    browse_users_link_xpath = "//a[contains(@href, 'browse') and contains(text(), 'Browse list of users')]"
    add_user_link_xpath = "//a[contains(@href, 'newuser') and contains(text(), 'Add a new user')]"
    user_search_field_id = "id_search"
    user_search_button_xpath = "//input[@type='submit' and @value='Search']"
    user_table_xpath = "//table[contains(@class, 'user-list')]"
    user_row_xpath = "//tr[contains(@class, 'user')]"
    
    # Locators for course management
    manage_courses_link_xpath = "//a[contains(@href, 'management') and contains(text(), 'Manage courses and categories')]"
    add_course_button_xpath = "//button[contains(@class, 'add-course')]"
    course_name_field_id = "id_fullname"
    course_shortname_field_id = "id_shortname"
    course_category_select_id = "id_category"
    save_course_button_xpath = "//input[@type='submit' and @value='Save and display']"
    
    # Locators for site settings
    site_settings_link_xpath = "//a[contains(@href, 'settings') and contains(text(), 'Site settings')]"
    site_name_field_id = "id_s__fullname"
    site_shortname_field_id = "id_s__shortname"
    save_settings_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_site_admin(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Site administration link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.site_admin_link_xpath)))
        self.driver.find_element(By.XPATH, self.site_admin_link_xpath).click()
    
    def navigate_to_users_section(self):
        # Click on Users link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.users_link_xpath)))
        self.driver.find_element(By.XPATH, self.users_link_xpath).click()
    
    def navigate_to_courses_section(self):
        # Click on Courses link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.courses_link_xpath)))
        self.driver.find_element(By.XPATH, self.courses_link_xpath).click()
    
    def navigate_to_site_settings(self):
        # Click on Server link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.server_link_xpath)))
        self.driver.find_element(By.XPATH, self.server_link_xpath).click()
        
        # Click on Site settings link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.site_settings_link_xpath)))
        self.driver.find_element(By.XPATH, self.site_settings_link_xpath).click()
    
    def browse_users(self):
        # Navigate to Users section
        self.navigate_to_users_section()
        
        # Click on Browse list of users link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.browse_users_link_xpath)))
        self.driver.find_element(By.XPATH, self.browse_users_link_xpath).click()
    
    def search_user(self, search_term):
        # Enter search term
        search_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.user_search_field_id)))
        search_field.clear()
        search_field.send_keys(search_term)
        
        # Click search button
        self.driver.find_element(By.XPATH, self.user_search_button_xpath).click()
    
    def get_user_count(self):
        # Get all user rows
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.user_table_xpath)))
            users = self.driver.find_elements(By.XPATH, self.user_row_xpath)
            return len(users)
        except:
            return 0
    
    def navigate_to_manage_courses(self):
        # Navigate to Courses section
        self.navigate_to_courses_section()
        
        # Click on Manage courses and categories link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.manage_courses_link_xpath)))
        self.driver.find_element(By.XPATH, self.manage_courses_link_xpath).click()
    
    def add_new_course(self, fullname, shortname, category="Miscellaneous"):
        # Click on Add course button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_course_button_xpath)))
        self.driver.find_element(By.XPATH, self.add_course_button_xpath).click()
        
        # Enter course details
        fullname_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.course_name_field_id)))
        fullname_field.clear()
        fullname_field.send_keys(fullname)
        
        shortname_field = self.driver.find_element(By.ID, self.course_shortname_field_id)
        shortname_field.clear()
        shortname_field.send_keys(shortname)
        
        # Select category
        category_select = Select(self.driver.find_element(By.ID, self.course_category_select_id))
        category_select.select_by_visible_text(category)
        
        # Save course
        self.driver.find_element(By.XPATH, self.save_course_button_xpath).click()
    
    def update_site_settings(self, site_name=None, site_shortname=None):
        # Navigate to Site settings
        self.navigate_to_site_settings()
        
        # Update site name if provided
        if site_name:
            site_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.site_name_field_id)))
            site_name_field.clear()
            site_name_field.send_keys(site_name)
        
        # Update site shortname if provided
        if site_shortname:
            site_shortname_field = self.driver.find_element(By.ID, self.site_shortname_field_id)
            site_shortname_field.clear()
            site_shortname_field.send_keys(site_shortname)
        
        # Save settings
        self.driver.find_element(By.XPATH, self.save_settings_button_xpath).click()
    
    def is_admin_page_accessible(self):
        # Check if the admin page is accessible
        try:
            self.navigate_to_site_admin()
            return "administration" in self.driver.current_url.lower()
        except:
            return False
