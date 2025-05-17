from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class LoginPage:
    # Locators
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    error_message_xpath = "//div[contains(@class, 'alert') and contains(@class, 'alert-danger')]"

    # Constructor
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Actions
    def setUserName(self, username):
        user_txt = self.driver.find_element(By.ID, self.txt_username_id)
        user_txt.clear()  # Clear any existing text
        if username:  # Only send keys if username is not empty
            user_txt.send_keys(username)

    def setPassword(self, password):
        pass_txt = self.driver.find_element(By.ID, self.txt_password_id)
        pass_txt.clear()  # Clear any existing text
        if password:  # Only send keys if password is not empty
            pass_txt.send_keys(password)

    def setBtn(self):
        clck_btn = self.driver.find_element(By.ID, self.btn_signin_id)
        clck_btn.click()

    def login(self, username, password):
        """Perform login with the given credentials"""
        self.setUserName(username)
        self.setPassword(password)
        self.setBtn()

    def is_login_successful(self):
        """Check if login was successful by verifying the page title"""
        try:
            # Wait for page to load after login
            self.wait.until(lambda driver: driver.title != "Log in to the site")
            return True
        except TimeoutException:
            return False

    def get_error_message(self):
        """Get the error message displayed after a failed login attempt"""
        try:
            error_element = self.driver.find_element(By.XPATH, self.error_message_xpath)
            return error_element.text
        except NoSuchElementException:
            return ""

    def verify_login_result(self, expected_title, expected_result):
        """Verify login result based on expected title and result"""
        actual_title = self.driver.title

        if expected_result.lower() == "pass":
            # For successful login, check if title matches expected title
            return actual_title == expected_title
        else:
            # For failed login, check if we're still on the login page or have an error message
            error_message = self.get_error_message()
            return actual_title == expected_title and error_message != ""
