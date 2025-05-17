from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class CalendarEvents:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_calendar_xpath = '//*[@id="nav-drawer"]/nav/ul/li[3]/a'
    
    # Locators for calendar
    new_event_button_xpath = "//button[contains(text(), 'New event')]"
    month_view_button_xpath = "//button[contains(@data-action, 'view-month')]"
    week_view_button_xpath = "//button[contains(@data-action, 'view-week')]"
    day_view_button_xpath = "//button[contains(@data-action, 'view-day')]"
    
    # Locators for event creation
    event_name_id = "id_name"
    event_date_day_id = "id_timestart_day"
    event_date_month_id = "id_timestart_month"
    event_date_year_id = "id_timestart_year"
    event_date_hour_id = "id_timestart_hour"
    event_date_minute_id = "id_timestart_minute"
    event_description_iframe_xpath = "//iframe[contains(@id, 'id_description')]"
    event_type_id = "id_eventtype"
    save_event_button_xpath = "//input[@type='submit' and @value='Save']"
    
    # Locators for event viewing
    event_link_xpath = "//a[contains(@class, 'calendar_event_')]"
    event_title_xpath = "//h3[contains(@class, 'name')]"
    event_time_xpath = "//div[contains(@class, 'date')]"
    event_description_xpath = "//div[contains(@class, 'description')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_calendar(self):
        self.driver.find_element(By.XPATH, self.btn_sidebar_xpath).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_calendar_xpath)))
        self.driver.find_element(By.XPATH, self.btn_calendar_xpath).click()
    
    def switch_to_month_view(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.month_view_button_xpath)))
        self.driver.find_element(By.XPATH, self.month_view_button_xpath).click()
    
    def switch_to_week_view(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.week_view_button_xpath)))
        self.driver.find_element(By.XPATH, self.week_view_button_xpath).click()
    
    def switch_to_day_view(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.day_view_button_xpath)))
        self.driver.find_element(By.XPATH, self.day_view_button_xpath).click()
    
    def click_new_event(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.new_event_button_xpath)))
        self.driver.find_element(By.XPATH, self.new_event_button_xpath).click()
    
    def create_event(self, event_name, description, event_type="User", day=None, month=None, year=None, hour=None, minute=None):
        # Enter event name
        event_name_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.event_name_id)))
        event_name_field.clear()
        event_name_field.send_keys(event_name)
        
        # Set event date if provided
        if day:
            day_select = Select(self.driver.find_element(By.ID, self.event_date_day_id))
            day_select.select_by_value(str(day))
        
        if month:
            month_select = Select(self.driver.find_element(By.ID, self.event_date_month_id))
            month_select.select_by_value(str(month))
        
        if year:
            year_select = Select(self.driver.find_element(By.ID, self.event_date_year_id))
            year_select.select_by_value(str(year))
        
        if hour:
            hour_select = Select(self.driver.find_element(By.ID, self.event_date_hour_id))
            hour_select.select_by_value(str(hour))
        
        if minute:
            minute_select = Select(self.driver.find_element(By.ID, self.event_date_minute_id))
            minute_select.select_by_value(str(minute))
        
        # Enter description in the iframe
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.event_description_iframe_xpath)))
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        body.send_keys(description)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
        
        # Select event type
        event_type_select = Select(self.driver.find_element(By.ID, self.event_type_id))
        event_type_select.select_by_visible_text(event_type)
        
        # Click Save button
        save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_event_button_xpath)))
        save_button.click()
    
    def get_events(self):
        # Get all events in the calendar
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.event_link_xpath)))
            events = self.driver.find_elements(By.XPATH, self.event_link_xpath)
            return events
        except:
            return []
    
    def open_event(self, event_index=0):
        # Open an event by index
        events = self.get_events()
        if len(events) > event_index:
            events[event_index].click()
            return True
        return False
    
    def get_event_details(self):
        # Get the details of the currently open event
        event_details = {}
        
        try:
            event_details["title"] = self.driver.find_element(By.XPATH, self.event_title_xpath).text
            event_details["time"] = self.driver.find_element(By.XPATH, self.event_time_xpath).text
            event_details["description"] = self.driver.find_element(By.XPATH, self.event_description_xpath).text
        except:
            pass
        
        return event_details
    
    def is_event_present(self, event_name):
        # Check if an event with the given name is present
        events = self.get_events()
        for event in events:
            if event_name in event.text:
                return True
        return False
