from selenium import webdriver
from POM_CLASS.SDET_Page_Object import SDET

class TestSdet:
    def test_sdet(self):
        driver = webdriver.Chrome()
        driver = webdriver.Chrome()
        driver.get("https://online.btes.co.in/login/index.php")
        driver.implicitly_wait(5)
        driver.maximize_window()
        sd = SDET(driver)

        sd.setUserName("ritesh@123")
        sd.setPassword("Ritesh@123")
        sd.setBtn()
        sd.sidebar()
        sd.dahsboard()
        sd.sdet()