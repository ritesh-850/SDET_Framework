from selenium.webdriver.common.by import By

class ForgotPassword:
    # Locators
    forgot_password_link_xpath = "//a[contains(text(), 'Forgotten your username or password')]"
    username_id = "id_username"
    email_id = "id_email"
    search_button_id = "id_submitbuttonusername"
    search_by_email_button_id = "id_submitbuttonemail"
    
    def __init__(self, driver):
        self.driver = driver
    
    def click_forgot_password_link(self):
        self.driver.find_element(By.XPATH, self.forgot_password_link_xpath).click()
    
    def search_by_username(self, username):
        self.driver.find_element(By.ID, self.username_id).send_keys(username)
        self.driver.find_element(By.ID, self.search_button_id).click()
    
    def search_by_email(self, email):
        self.driver.find_element(By.ID, self.email_id).send_keys(email)
        self.driver.find_element(By.ID, self.search_by_email_button_id).click()
