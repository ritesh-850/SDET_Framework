from selenium.webdriver.common.by import By


class LoginPage:
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_xpath = '//*[@class="login"]'


#constructor
    def __init__(self,driver):
        self.driver = driver

#Action
    def setUserName(self,username):
        user_txt=self.driver.find_element(By.ID,self.txt_username_id)
        user_txt.send_keys(username)

    def setPassword(self,password):
        pass_txt=self.driver.find_element(By.ID,self.txt_password_id)
        pass_txt.send_keys(password)

    def setBtn(self):
        clck_btn=self.driver.find_element(By.XPATH,self.btn_signin_xpath)
        clck_btn.click()