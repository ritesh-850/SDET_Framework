from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Messages:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for messages
    messages_icon_xpath = "//div[contains(@class, 'popover-region-messages')]"
    messages_dropdown_xpath = "//div[contains(@class, 'popover-region-container')]"
    messages_items_xpath = "//div[contains(@class, 'message')]"
    messages_page_link_xpath = "//a[contains(@class, 'see-all-link')]"
    
    # Locators for sending messages
    new_message_button_xpath = "//button[contains(@data-action, 'send-message')]"
    search_contacts_input_xpath = "//input[contains(@placeholder, 'Search')]"
    contact_item_xpath = "//div[contains(@class, 'contact')]"
    message_text_area_xpath = "//textarea[contains(@data-region, 'send-message-txt')]"
    send_message_button_xpath = "//button[contains(@data-action, 'send-message')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def open_messages(self):
        # Click on messages icon
        self.driver.find_element(By.XPATH, self.messages_icon_xpath).click()
        
        # Wait for messages dropdown to be visible
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.messages_dropdown_xpath)))
    
    def get_messages_count(self):
        # Get all message items
        messages = self.driver.find_elements(By.XPATH, self.messages_items_xpath)
        return len(messages)
    
    def go_to_messages_page(self):
        # Click on see all messages link
        self.driver.find_element(By.XPATH, self.messages_page_link_xpath).click()
    
    def is_messages_dropdown_open(self):
        # Check if messages dropdown is open
        try:
            dropdown = self.driver.find_element(By.XPATH, self.messages_dropdown_xpath)
            return dropdown.is_displayed()
        except:
            return False
    
    def start_new_message(self):
        # Click on new message button
        self.driver.find_element(By.XPATH, self.new_message_button_xpath).click()
    
    def search_contact(self, contact_name):
        # Enter contact name in search input
        search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.search_contacts_input_xpath)))
        search_input.clear()
        search_input.send_keys(contact_name)
        
        # Wait for search results
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.contact_item_xpath)))
    
    def select_first_contact(self):
        # Click on first contact in search results
        contacts = self.driver.find_elements(By.XPATH, self.contact_item_xpath)
        if len(contacts) > 0:
            contacts[0].click()
            return True
        return False
    
    def send_message(self, message_text):
        # Enter message text
        message_area = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.message_text_area_xpath)))
        message_area.clear()
        message_area.send_keys(message_text)
        
        # Click send button
        self.driver.find_element(By.XPATH, self.send_message_button_xpath).click()
