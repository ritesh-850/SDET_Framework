from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CreateNew:
    # Locators
    btn_new_xpath = '//*[text()="Create new account"]'
    username_xpath = '//*[@name="username"]'
    password_xpath = '//*[@name="password"]'
    email_xpath = '//*[@name="email"]'
    email2_xpath = '//*[@name="email2"]'
    firstname_xpath = '//*[@name="firstname"]'
    lastname_xpath = '//*[@name="lastname"]'
    city_xpath = '//*[@name="city"]'
    country_id = 'id_country'
    create_account_id = 'id_submitbutton'

    def __init__(self, driver):
        self.driver = driver

    def click_create_new_account(self):
        self.driver.find_element(By.XPATH, self.btn_new_xpath).click()

    def set_username(self, username):
        self.driver.find_element(By.XPATH, self.username_xpath).send_keys(username)

    def set_password(self, password):
        self.driver.find_element(By.XPATH, self.password_xpath).send_keys(password)

    def set_email(self, email):
        self.driver.find_element(By.XPATH, self.email_xpath).send_keys(email)

    def set_email_confirmation(self, email):
        self.driver.find_element(By.XPATH, self.email2_xpath).send_keys(email)

    def set_firstname(self, firstname):
        self.driver.find_element(By.XPATH, self.firstname_xpath).send_keys(firstname)

    def set_lastname(self, lastname):
        self.driver.find_element(By.XPATH, self.lastname_xpath).send_keys(lastname)

    def set_city(self, city):
        self.driver.find_element(By.XPATH, self.city_xpath).send_keys(city)

    def select_country(self, country_text):
        country_dropdown = Select(self.driver.find_element(By.ID, self.country_id))
        country_dropdown.select_by_visible_text(country_text)

    def click_create_account_button(self):
        self.driver.find_element(By.ID, self.create_account_id).click()
