from selenium import webdriver
from POM_CLASS.Profile_Page_Object import Profile

class TestProfile:
    def test_profile(self):
        driver = webdriver.Chrome()
        driver = webdriver.Chrome()
        driver.get("https://online.btes.co.in/login/index.php")
        driver.implicitly_wait(5)
        driver.maximize_window()
        prf = Profile(driver)

        prf.setUserName("ritesh@123")
        prf.setPassword("Ritesh@123")
        prf.setBtn()
        prf.profile()