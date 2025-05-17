from selenium.webdriver.common.by import By


class Logout_page:
    txt_logout_xpath = '//*[@id="action-menu-1-menu"]/a[6]'
    def __init__(self,driver):
        self.driver = driver

    def logout(self):
        btn = self.driver.find_element(By.XPATH,self.txt_logout_xpath)
        btn.click()

