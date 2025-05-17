from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class Reports:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    site_admin_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Site administration')]"
    
    # Locators for reports
    reports_link_xpath = "//a[contains(@href, 'report') and contains(text(), 'Reports')]"
    
    # Locators for specific reports
    logs_link_xpath = "//a[contains(@href, 'log') and contains(text(), 'Logs')]"
    activity_link_xpath = "//a[contains(@href, 'activity') and contains(text(), 'Activity report')]"
    course_participation_link_xpath = "//a[contains(@href, 'participation') and contains(text(), 'Course participation')]"
    statistics_link_xpath = "//a[contains(@href, 'stats') and contains(text(), 'Statistics')]"
    
    # Locators for logs report
    log_course_select_id = "id_course"
    log_user_select_id = "id_user"
    log_date_select_id = "id_date"
    log_activity_select_id = "id_action"
    log_get_button_xpath = "//input[@type='submit' and @value='Get these logs']"
    log_results_xpath = "//table[contains(@class, 'logtable')]//tr"
    
    # Locators for activity report
    activity_course_select_id = "id_course"
    activity_get_button_xpath = "//input[@type='submit' and @value='Get these logs']"
    activity_results_xpath = "//table[contains(@class, 'generaltable')]//tr"
    
    # Locators for course participation
    participation_course_select_id = "id_course"
    participation_activity_select_id = "id_instanceid"
    participation_get_button_xpath = "//input[@type='submit' and @value='Go']"
    participation_results_xpath = "//table[contains(@class, 'generaltable')]//tr"
    
    # Locators for statistics
    statistics_course_select_id = "id_course"
    statistics_get_button_xpath = "//input[@type='submit' and @value='View']"
    statistics_results_xpath = "//div[contains(@class, 'graph')]"
    
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
    
    def navigate_to_reports(self):
        # Click on Reports link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.reports_link_xpath)))
        self.driver.find_element(By.XPATH, self.reports_link_xpath).click()
    
    def navigate_to_logs(self):
        # Click on Logs link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.logs_link_xpath)))
        self.driver.find_element(By.XPATH, self.logs_link_xpath).click()
    
    def navigate_to_activity_report(self):
        # Click on Activity report link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.activity_link_xpath)))
        self.driver.find_element(By.XPATH, self.activity_link_xpath).click()
    
    def navigate_to_course_participation(self):
        # Click on Course participation link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.course_participation_link_xpath)))
        self.driver.find_element(By.XPATH, self.course_participation_link_xpath).click()
    
    def navigate_to_statistics(self):
        # Click on Statistics link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.statistics_link_xpath)))
        self.driver.find_element(By.XPATH, self.statistics_link_xpath).click()
    
    def generate_logs_report(self, course="All courses", user="All participants", date="Today", activity="All actions"):
        # Select course
        course_select = Select(self.wait.until(EC.visibility_of_element_located((By.ID, self.log_course_select_id))))
        try:
            course_select.select_by_visible_text(course)
        except:
            # If the exact course name is not found, select the first option
            course_select.select_by_index(0)
        
        # Select user
        user_select = Select(self.driver.find_element(By.ID, self.log_user_select_id))
        try:
            user_select.select_by_visible_text(user)
        except:
            # If the exact user name is not found, select the first option
            user_select.select_by_index(0)
        
        # Select date
        date_select = Select(self.driver.find_element(By.ID, self.log_date_select_id))
        try:
            date_select.select_by_visible_text(date)
        except:
            # If the exact date is not found, select the first option
            date_select.select_by_index(0)
        
        # Select activity
        activity_select = Select(self.driver.find_element(By.ID, self.log_activity_select_id))
        try:
            activity_select.select_by_visible_text(activity)
        except:
            # If the exact activity is not found, select the first option
            activity_select.select_by_index(0)
        
        # Click Get these logs button
        self.driver.find_element(By.XPATH, self.log_get_button_xpath).click()
    
    def generate_activity_report(self, course="All courses"):
        # Select course
        course_select = Select(self.wait.until(EC.visibility_of_element_located((By.ID, self.activity_course_select_id))))
        try:
            course_select.select_by_visible_text(course)
        except:
            # If the exact course name is not found, select the first option
            course_select.select_by_index(0)
        
        # Click Get these logs button
        self.driver.find_element(By.XPATH, self.activity_get_button_xpath).click()
    
    def generate_course_participation_report(self, course="All courses", activity="All activities"):
        # Select course
        course_select = Select(self.wait.until(EC.visibility_of_element_located((By.ID, self.participation_course_select_id))))
        try:
            course_select.select_by_visible_text(course)
        except:
            # If the exact course name is not found, select the first option
            course_select.select_by_index(0)
        
        # Wait for activity select to be populated
        time.sleep(2)
        
        # Select activity
        activity_select = Select(self.driver.find_element(By.ID, self.participation_activity_select_id))
        try:
            activity_select.select_by_visible_text(activity)
        except:
            # If the exact activity is not found, select the first option
            activity_select.select_by_index(0)
        
        # Click Go button
        self.driver.find_element(By.XPATH, self.participation_get_button_xpath).click()
    
    def generate_statistics_report(self, course="All courses"):
        # Select course
        course_select = Select(self.wait.until(EC.visibility_of_element_located((By.ID, self.statistics_course_select_id))))
        try:
            course_select.select_by_visible_text(course)
        except:
            # If the exact course name is not found, select the first option
            course_select.select_by_index(0)
        
        # Click View button
        self.driver.find_element(By.XPATH, self.statistics_get_button_xpath).click()
    
    def get_logs_count(self):
        # Get the number of log entries
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.log_results_xpath)))
            logs = self.driver.find_elements(By.XPATH, self.log_results_xpath)
            # Subtract 1 for the header row
            return len(logs) - 1
        except:
            return 0
    
    def get_activity_report_count(self):
        # Get the number of activity report entries
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.activity_results_xpath)))
            activities = self.driver.find_elements(By.XPATH, self.activity_results_xpath)
            # Subtract 1 for the header row
            return len(activities) - 1
        except:
            return 0
    
    def get_participation_report_count(self):
        # Get the number of participation report entries
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.participation_results_xpath)))
            participants = self.driver.find_elements(By.XPATH, self.participation_results_xpath)
            # Subtract 1 for the header row
            return len(participants) - 1
        except:
            return 0
    
    def is_statistics_graph_displayed(self):
        # Check if statistics graph is displayed
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.statistics_results_xpath)))
            return True
        except:
            return False
