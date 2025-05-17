from selenium.webdriver.common.by import By


class Calender:
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_calender_xpath = '//*[@id="nav-drawer"]/nav/ul/li[3]/a'

    def __init__(self,driver):
        self.driver = driver

    def setUserName(self,username):
        user_txt=self.driver.find_element(By.ID,self.txt_username_id)
        user_txt.send_keys(username)

    def setPassword(self,password):
        pass_txt=self.driver.find_element(By.ID,self.txt_password_id)
        pass_txt.send_keys(password)

    def setBtn(self):
        clck_btn=self.driver.find_element(By.ID,self.btn_signin_id)
        clck_btn.click()

    def sidebar(self):
        s_click = self.driver.find_element(By.XPATH,self.btn_sidebar_xpath)
        s_click.click()

    def calender(self):
        c_click = self.driver.find_element(By.XPATH,self.btn_calender_xpath)
        c_click.click()
