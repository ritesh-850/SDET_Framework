from selenium import webdriver

from POM_CLASS.Logout_page_object import Logout_page

class Test_Logout:
    def test_logout(self):
        Chrome_option = webdriver.ChromeOptions()
        Chrome_option.add_argument("--headless")
        driver = webdriver.Chrome(options=Chrome_option)
        return driver
        driver = headless_chrome()
        driver.get("https://online.btes.co.in/login/index.php")
        driver.implicitly_wait(5)
        driver.maximize_window()
        lp = Logout_page(driver)
        lp.logout()
        title = driver.title
        assert title == 'bebo’s First-Ever Finishing School BTES Is Now LIVE'