from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Forum:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'
    
    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'
    
    # Locators for forums
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    forum_link_xpath = "//span[contains(@class, 'instancename') and contains(text(), 'Forum')]"
    discussion_link_xpath = "//td[contains(@class, 'topic')]//a"
    add_discussion_button_xpath = "//button[contains(text(), 'Add discussion topic')]"
    
    # Locators for creating a discussion
    subject_field_id = "id_subject"
    message_iframe_xpath = "//iframe[contains(@id, 'id_message')]"
    post_to_forum_button_xpath = "//input[@type='submit' and @value='Post to forum']"
    
    # Locators for replying to a discussion
    reply_link_xpath = "//a[contains(@class, 'reply-action')]"
    reply_message_iframe_xpath = "//iframe[contains(@id, 'id_message')]"
    submit_post_button_xpath = "//input[@type='submit' and @value='Post to forum']"
    
    # Locators for viewing discussions
    discussion_posts_xpath = "//div[contains(@class, 'forumpost')]"
    post_content_xpath = "//div[contains(@class, 'posting')]"
    
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
    
    def open_forum(self, forum_index=0):
        # Open a forum by index
        forums = self.driver.find_elements(By.XPATH, self.forum_link_xpath)
        if len(forums) > forum_index:
            forums[forum_index].click()
            return True
        return False
    
    def open_discussion(self, discussion_index=0):
        # Open a discussion by index
        discussions = self.driver.find_elements(By.XPATH, self.discussion_link_xpath)
        if len(discussions) > discussion_index:
            discussions[discussion_index].click()
            return True
        return False
    
    def click_add_discussion(self):
        # Click on Add discussion topic button
        try:
            add_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_discussion_button_xpath)))
            add_button.click()
            return True
        except:
            return False
    
    def create_discussion(self, subject, message):
        # Enter subject
        subject_field = self.wait.until(EC.visibility_of_element_located((By.ID, self.subject_field_id)))
        subject_field.clear()
        subject_field.send_keys(subject)
        
        # Enter message in the iframe
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.message_iframe_xpath)))
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        body.send_keys(message)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
        
        # Click Post to forum button
        post_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.post_to_forum_button_xpath)))
        post_button.click()
    
    def reply_to_discussion(self, message):
        # Click on Reply link
        reply_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.reply_link_xpath)))
        reply_link.click()
        
        # Enter message in the iframe
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.reply_message_iframe_xpath)))
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.clear()
        body.send_keys(message)
        
        # Switch back to the main content
        self.driver.switch_to.default_content()
        
        # Click Submit post button
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.submit_post_button_xpath)))
        submit_button.click()
    
    def get_discussion_posts(self):
        # Get all discussion posts
        posts = self.driver.find_elements(By.XPATH, self.discussion_posts_xpath)
        return posts
    
    def get_post_contents(self):
        # Get the content of all posts
        posts = self.get_discussion_posts()
        contents = []
        for post in posts:
            try:
                content = post.find_element(By.XPATH, f".{self.post_content_xpath}").text
                contents.append(content)
            except:
                contents.append("Content not found")
        return contents
