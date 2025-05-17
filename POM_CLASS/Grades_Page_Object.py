from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Grades:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for grades
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    grades_link_xpath = "//a[contains(@class, 'dropdown-item') and contains(text(), 'Grades')]"
    user_menu_xpath = "//div[contains(@class, 'usermenu')]"
    grades_table_xpath = "//table[contains(@class, 'generaltable')]"
    grade_items_xpath = "//tr[contains(@class, 'gradeitem')]"
    grade_value_xpath = "//td[contains(@class, 'grade')]"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()
    
    def navigate_to_courses(self):
        self.driver.find_element(By.XPATH, self.btn_sidebar_xpath).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_courses_xpath)))
        self.driver.find_element(By.XPATH, self.btn_courses_xpath).click()
    
    def select_course(self, course_index=0):
        # Select a course by index (0 for the first course)
        courses = self.driver.find_elements(By.XPATH, self.course_card_xpath)
        if len(courses) > course_index:
            courses[course_index].click()
        else:
            raise Exception(f"Course with index {course_index} not found")
    
    def navigate_to_grades(self):
        # Click on user menu
        self.driver.find_element(By.XPATH, self.user_menu_xpath).click()
        
        # Click on Grades link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.grades_link_xpath)))
        self.driver.find_element(By.XPATH, self.grades_link_xpath).click()
    
    def get_grade_items(self):
        # Get all grade items
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.grades_table_xpath)))
            grade_items = self.driver.find_elements(By.XPATH, self.grade_items_xpath)
            return grade_items
        except:
            return []
    
    def get_grade_item_names(self):
        # Get the names of all grade items
        grade_items = self.get_grade_items()
        names = []
        for item in grade_items:
            try:
                name = item.find_element(By.XPATH, ".//th").text
                names.append(name)
            except:
                pass
        return names
    
    def get_grade_item_values(self):
        # Get the values of all grade items
        grade_items = self.get_grade_items()
        values = []
        for item in grade_items:
            try:
                value = item.find_element(By.XPATH, f".{self.grade_value_xpath}").text
                values.append(value)
            except:
                values.append("N/A")
        return values
    
    def get_grades_as_dict(self):
        # Get grades as a dictionary of name: value
        names = self.get_grade_item_names()
        values = self.get_grade_item_values()
        
        # Make sure we have the same number of names and values
        min_length = min(len(names), len(values))
        
        # Create dictionary
        grades_dict = {}
        for i in range(min_length):
            grades_dict[names[i]] = values[i]
        
        return grades_dict
    
    def get_course_total_grade(self):
        # Get the course total grade
        try:
            grades_dict = self.get_grades_as_dict()
            for key in grades_dict:
                if "course total" in key.lower():
                    return grades_dict[key]
            return "Course total not found"
        except:
            return "Error getting course total"
