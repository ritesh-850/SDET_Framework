from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class UserPreferences:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    preferences_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Preferences')]"
    
    # Locators for preferences sections
    edit_profile_link_xpath = "//a[contains(text(), 'Edit profile')]"
    change_password_link_xpath = "//a[contains(text(), 'Change password')]"
    preferred_language_link_xpath = "//a[contains(text(), 'Preferred language')]"
    notification_preferences_link_xpath = "//a[contains(text(), 'Notification preferences')]"
    
    # Locators for edit profile
    first_name_id = "id_firstname"
    last_name_id = "id_lastname"
    email_id = "id_email"
    city_id = "id_city"
    country_id = "id_country"
    timezone_id = "id_timezone"
    description_iframe_xpath = "//iframe[contains(@id, 'id_description')]"
    update_profile_button_xpath = "//input[@type='submit' and @value='Update profile']"
    
    # Locators for change password
    current_password_id = "id_password"
    new_password_id = "id_newpassword1"
    new_password_again_id = "id_newpassword2"
    save_changes_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
    # Locators for preferred language
    language_select_id = "id_lang"
    save_language_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
    # Locators for notification preferences
    email_notification_checkbox_xpath = "//input[@type='checkbox' and contains(@name, 'email')]"
    save_notification_button_xpath = "//input[@type='submit' and @value='Save changes']"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_preferences(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Preferences link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.preferences_link_xpath)))
        self.driver.find_element(By.XPATH, self.preferences_link_xpath).click()
    
    def navigate_to_edit_profile(self):
        # Click on Edit profile link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.edit_profile_link_xpath)))
        self.driver.find_element(By.XPATH, self.edit_profile_link_xpath).click()
    
    def navigate_to_change_password(self):
        # Click on Change password link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.change_password_link_xpath)))
        self.driver.find_element(By.XPATH, self.change_password_link_xpath).click()
    
    def navigate_to_preferred_language(self):
        # Click on Preferred language link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.preferred_language_link_xpath)))
        self.driver.find_element(By.XPATH, self.preferred_language_link_xpath).click()
    
    def navigate_to_notification_preferences(self):
        # Click on Notification preferences link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.notification_preferences_link_xpath)))
        self.driver.find_element(By.XPATH, self.notification_preferences_link_xpath).click()
    
    def update_profile(self, first_name=None, last_name=None, email=None, city=None, country=None, timezone=None, description=None):
        # Update profile fields if provided
        if first_name:
            first_name_field = self.driver.find_element(By.ID, self.first_name_id)
            first_name_field.clear()
            first_name_field.send_keys(first_name)
        
        if last_name:
            last_name_field = self.driver.find_element(By.ID, self.last_name_id)
            last_name_field.clear()
            last_name_field.send_keys(last_name)
        
        if email:
            email_field = self.driver.find_element(By.ID, self.email_id)
            email_field.clear()
            email_field.send_keys(email)
        
        if city:
            city_field = self.driver.find_element(By.ID, self.city_id)
            city_field.clear()
            city_field.send_keys(city)
        
        if country:
            country_select = Select(self.driver.find_element(By.ID, self.country_id))
            country_select.select_by_visible_text(country)
        
        if timezone:
            timezone_select = Select(self.driver.find_element(By.ID, self.timezone_id))
            timezone_select.select_by_visible_text(timezone)
        
        if description:
            # Switch to the description iframe
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.description_iframe_xpath)))
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.clear()
            body.send_keys(description)
            
            # Switch back to the main content
            self.driver.switch_to.default_content()
        
        # Click Update profile button
        update_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.update_profile_button_xpath)))
        update_button.click()
    
    def change_password(self, current_password, new_password):
        # Enter current password
        current_password_field = self.driver.find_element(By.ID, self.current_password_id)
        current_password_field.clear()
        current_password_field.send_keys(current_password)
        
        # Enter new password
        new_password_field = self.driver.find_element(By.ID, self.new_password_id)
        new_password_field.clear()
        new_password_field.send_keys(new_password)
        
        # Enter new password again
        new_password_again_field = self.driver.find_element(By.ID, self.new_password_again_id)
        new_password_again_field.clear()
        new_password_again_field.send_keys(new_password)
        
        # Click Save changes button
        save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_changes_button_xpath)))
        save_button.click()
    
    def change_language(self, language):
        # Select language
        language_select = Select(self.driver.find_element(By.ID, self.language_select_id))
        language_select.select_by_visible_text(language)
        
        # Click Save changes button
        save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_language_button_xpath)))
        save_button.click()
    
    def toggle_email_notification(self, index=0, enable=True):
        # Get all email notification checkboxes
        checkboxes = self.driver.find_elements(By.XPATH, self.email_notification_checkbox_xpath)
        
        if len(checkboxes) > index:
            checkbox = checkboxes[index]
            
            # Check or uncheck the checkbox
            if (enable and not checkbox.is_selected()) or (not enable and checkbox.is_selected()):
                checkbox.click()
            
            # Click Save changes button
            save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_notification_button_xpath)))
            save_button.click()
            return True
        
        return False
    
    def get_profile_info(self):
        # Get profile information
        profile_info = {}
        
        try:
            profile_info["first_name"] = self.driver.find_element(By.ID, self.first_name_id).get_attribute("value")
            profile_info["last_name"] = self.driver.find_element(By.ID, self.last_name_id).get_attribute("value")
            profile_info["email"] = self.driver.find_element(By.ID, self.email_id).get_attribute("value")
            profile_info["city"] = self.driver.find_element(By.ID, self.city_id).get_attribute("value")
            
            # Get selected country
            country_select = Select(self.driver.find_element(By.ID, self.country_id))
            profile_info["country"] = country_select.first_selected_option.text
            
            # Get selected timezone
            timezone_select = Select(self.driver.find_element(By.ID, self.timezone_id))
            profile_info["timezone"] = timezone_select.first_selected_option.text
        except:
            pass
        
        return profile_info
