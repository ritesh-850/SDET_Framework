from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class FileManagement:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_dashboard_xpath = '//*[@id="nav-drawer"]/nav/ul/li[1]/a'
    
    # Locators for private files
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    private_files_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Private files')]"
    
    # Locators for file management
    file_picker_button_xpath = "//button[contains(@class, 'fp-btn-add')]"
    upload_file_button_xpath = "//span[contains(text(), 'Upload a file')]"
    file_input_xpath = "//input[@type='file']"
    upload_this_file_button_xpath = "//button[contains(text(), 'Upload this file')]"
    save_changes_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
    # Locators for file listing
    file_list_xpath = "//span[contains(@class, 'fp-filename')]"
    file_delete_button_xpath = "//a[contains(@class, 'fp-file-delete')]"
    confirm_delete_button_xpath = "//button[contains(text(), 'OK')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_dashboard(self):
        self.driver.find_element(By.XPATH, self.btn_sidebar_xpath).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_dashboard_xpath)))
        self.driver.find_element(By.XPATH, self.btn_dashboard_xpath).click()
    
    def navigate_to_private_files(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Private files link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.private_files_link_xpath)))
        self.driver.find_element(By.XPATH, self.private_files_link_xpath).click()
    
    def upload_file(self, file_path):
        # Make sure the file exists
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        
        # Click on file picker button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.file_picker_button_xpath)))
        self.driver.find_element(By.XPATH, self.file_picker_button_xpath).click()
        
        # Click on Upload a file button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.upload_file_button_xpath)))
        self.driver.find_element(By.XPATH, self.upload_file_button_xpath).click()
        
        # Upload the file
        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.file_input_xpath)))
        file_input.send_keys(file_path)
        
        # Click on Upload this file button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.upload_this_file_button_xpath)))
        self.driver.find_element(By.XPATH, self.upload_this_file_button_xpath).click()
        
        # Wait for the file to be uploaded
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.upload_this_file_button_xpath)))
    
    def save_changes(self):
        # Click on Save changes button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_changes_button_xpath)))
        self.driver.find_element(By.XPATH, self.save_changes_button_xpath).click()
    
    def get_file_list(self):
        # Get all files in the list
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.file_list_xpath)))
            files = self.driver.find_elements(By.XPATH, self.file_list_xpath)
            return [file.text for file in files]
        except:
            return []
    
    def delete_file(self, file_name):
        # Find the file by name
        try:
            file_xpath = f"//span[contains(@class, 'fp-filename') and text()='{file_name}']"
            file_element = self.driver.find_element(By.XPATH, file_xpath)
            
            # Click on the file to select it
            file_element.click()
            
            # Click on delete button
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.file_delete_button_xpath)))
            self.driver.find_element(By.XPATH, self.file_delete_button_xpath).click()
            
            # Confirm deletion
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.confirm_delete_button_xpath)))
            self.driver.find_element(By.XPATH, self.confirm_delete_button_xpath).click()
            
            return True
        except:
            return False
