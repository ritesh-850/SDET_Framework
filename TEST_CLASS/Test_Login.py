import pytest
from POM_CLASS.Login_Page_Object import LoginPage
from selenium import webdriver




class Testlogin:
    def test_login(self):
        driver = webdriver.Chrome()
        driver.get("https://online.btes.co.in/login/index.php")
        driver.implicitly_wait(5)
        driver.maximize_window()
        lp=LoginPage(driver)
        lp.setUserName("ritesh@123")
        lp.setPassword("Ritesh@123")
        lp.setBtn()
        act_title = driver.title
        assert act_title == 'BTES-LMS: Log in to the site',"not he correct way"

