from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Notifications:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for notifications
    notifications_icon_xpath = "//div[contains(@class, 'popover-region-notifications')]"
    notifications_dropdown_xpath = "//div[contains(@class, 'popover-region-container')]"
    notifications_items_xpath = "//div[contains(@class, 'notification-message')]"
    notifications_preferences_xpath = "//a[contains(@class, 'preferences-link')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def open_notifications(self):
        # Click on notifications icon
        self.driver.find_element(By.XPATH, self.notifications_icon_xpath).click()
        
        # Wait for notifications dropdown to be visible
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.notifications_dropdown_xpath)))
    
    def get_notifications_count(self):
        # Get all notification items
        notifications = self.driver.find_elements(By.XPATH, self.notifications_items_xpath)
        return len(notifications)
    
    def go_to_notification_preferences(self):
        # Click on notification preferences link
        self.driver.find_element(By.XPATH, self.notifications_preferences_xpath).click()
    
    def is_notifications_dropdown_open(self):
        # Check if notifications dropdown is open
        try:
            dropdown = self.driver.find_element(By.XPATH, self.notifications_dropdown_xpath)
            return dropdown.is_displayed()
        except:
            return False
