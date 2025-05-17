from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Search:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for search
    search_icon_xpath = "//div[contains(@class, 'search-input-wrapper')]"
    search_input_id = "form-autocomplete-input-1"  # This might change, need to inspect
    search_button_xpath = "//button[@type='submit' and contains(@class, 'search-icon')]"
    search_results_xpath = "//div[contains(@class, 'search-results')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def click_search_icon(self):
        self.driver.find_element(By.XPATH, self.search_icon_xpath).click()
    
    def perform_search(self, search_term):
        # Click on search icon to open search box
        self.click_search_icon()
        
        # Wait for search input to be visible and enter search term
        search_input = self.wait.until(EC.visibility_of_element_located((By.ID, self.search_input_id)))
        search_input.clear()
        search_input.send_keys(search_term)
        
        # Click search button
        self.driver.find_element(By.XPATH, self.search_button_xpath).click()
    
    def get_search_results_count(self):
        # Wait for search results to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.search_results_xpath)))
        
        # Get all search result items
        results = self.driver.find_elements(By.XPATH, f"{self.search_results_xpath}//div[contains(@class, 'result-item')]")
        return len(results)
    
    def is_search_successful(self):
        # Check if search results are displayed
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.search_results_xpath)))
            return True
        except:
            return False
