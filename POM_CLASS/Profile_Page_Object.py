from selenium.webdriver.common.by import By


class Profile:
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    btn_profile = '//*[@class="userbutton"]'

    def __init__(self, driver):
        self.driver = driver

    def setUserName(self, username):
        user_txt = self.driver.find_element(By.ID, self.txt_username_id)
        user_txt.send_keys(username)

    def setPassword(self, password):
        pass_txt = self.driver.find_element(By.ID, self.txt_password_id)
        pass_txt.send_keys(password)

    def setBtn(self):
        clck_btn = self.driver.find_element(By.ID, self.btn_signin_id)
        clck_btn.click()

    def profile(self):
        prf_click = self.driver.find_element(By.XPATH, self.btn_profile)
        prf_click.click()
