from selenium.webdriver.common.by import By


class Dashboard:
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_dashboard_xpath = '//*[@id="nav-drawer"]/nav/ul/li[1]/a'

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

    def dahsboard(self):
        d_click = self.driver.find_element(By.XPATH,self.btn_dashboard_xpath)
        d_click.click()