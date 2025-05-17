from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class Assignment:
    # Locators for login
    txt_username_id = 'username'
    txt_password_id = 'password'
    btn_signin_id = 'loginbtn'

    # Locators for navigation
    btn_sidebar_xpath = '//*[@id="header"]/div/div/button'
    btn_courses_xpath = '//*[@id="nav-drawer"]/nav/ul/li[2]/a'

    # Locators for assignments
    course_card_xpath = "//div[contains(@class, 'card dashboard-card')]"
    assignment_link_xpath = "//span[contains(@class, 'instancename') and contains(text(), 'Assignment')]"
    add_submission_button_xpath = "//button[contains(@type, 'submit') and contains(text(), 'Add submission')]"
    edit_submission_button_xpath = "//button[contains(@type, 'submit') and contains(text(), 'Edit submission')]"
    file_upload_field_xpath = "//input[@type='file']"
    online_text_iframe_xpath = "//iframe[contains(@id, 'id_onlinetext')]"
    save_changes_button_xpath = "//input[@type='submit' and @value='Save changes']"
    submission_status_xpath = "//div[contains(@class, 'submissionstatustable')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, username, password):
        self.driver.find_element(By.ID, self.txt_username_id).send_keys(username)
        self.driver.find_element(By.ID, self.txt_password_id).send_keys(password)
        self.driver.find_element(By.ID, self.btn_signin_id).click()

    def navigate_to_courses(self):
        try:
            # Click on sidebar button
            sidebar_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_sidebar_xpath)))
            sidebar_btn.click()

            # Take screenshot after clicking sidebar
            import allure
            from allure_commons.types import AttachmentType
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="after_sidebar_click",
                attachment_type=AttachmentType.PNG
            )

            # Wait for courses button to be clickable
            courses_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.btn_courses_xpath)))

            # Take screenshot before clicking courses button
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="before_courses_click",
                attachment_type=AttachmentType.PNG
            )

            # Click on courses button
            courses_btn.click()

            # Take screenshot after clicking courses button
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="after_courses_click",
                attachment_type=AttachmentType.PNG
            )
        except Exception as e:
            # Capture screenshot on any exception
            import allure
            from allure_commons.types import AttachmentType
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_navigating_to_courses",
                attachment_type=AttachmentType.PNG
            )
            raise Exception(f"Error navigating to courses: {str(e)}")

    def select_course(self, course_index=0):
        # Select a course by index (0 for the first course)
        try:
            # Wait for courses to be visible
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.course_card_xpath)))

            # Get all course cards
            courses = self.driver.find_elements(By.XPATH, self.course_card_xpath)

            # Log the number of courses found
            print(f"Found {len(courses)} courses")

            # Take a screenshot of the courses page
            import allure
            from allure_commons.types import AttachmentType
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"courses_found_{len(courses)}",
                attachment_type=AttachmentType.PNG
            )

            # Check if we have enough courses
            if len(courses) > course_index:
                courses[course_index].click()
            else:
                # Try an alternative XPath if the original one doesn't work
                alt_xpath = "//div[contains(@class, 'coursebox')]"
                alt_courses = self.driver.find_elements(By.XPATH, alt_xpath)
                print(f"Trying alternative XPath, found {len(alt_courses)} courses")

                if len(alt_courses) > course_index:
                    alt_courses[course_index].click()
                else:
                    # Capture page source for debugging
                    page_source = self.driver.page_source
                    allure.attach(
                        page_source.encode('utf-8'),
                        name="page_source_when_no_courses_found",
                        attachment_type=AttachmentType.TEXT
                    )

                    raise Exception(f"Course with index {course_index} not found. Found {len(courses)} courses with primary XPath and {len(alt_courses)} with alternative XPath.")
        except Exception as e:
            # Capture screenshot on any exception
            import allure
            from allure_commons.types import AttachmentType
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_selecting_course",
                attachment_type=AttachmentType.PNG
            )
            raise Exception(f"Error selecting course: {str(e)}")

    def open_assignment(self, assignment_index=0):
        # Open an assignment by index
        assignments = self.driver.find_elements(By.XPATH, self.assignment_link_xpath)
        if len(assignments) > assignment_index:
            assignments[assignment_index].click()
            return True
        return False

    def click_add_submission(self):
        # Click on Add submission button
        try:
            add_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.add_submission_button_xpath)))
            add_button.click()
            return True
        except:
            # Maybe the submission already exists, try to edit it
            try:
                edit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.edit_submission_button_xpath)))
                edit_button.click()
                return True
            except:
                return False

    def upload_file(self, file_path):
        # Upload a file for submission
        try:
            # Make sure the file exists
            if not os.path.exists(file_path):
                raise Exception(f"File not found: {file_path}")

            # Find the file upload field and upload the file
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, self.file_upload_field_xpath)))
            file_input.send_keys(file_path)
            return True
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return False

    def enter_online_text(self, text):
        # Enter text in the online text editor
        try:
            # Switch to the iframe
            iframe = self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.online_text_iframe_xpath)))

            # Enter text in the body
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.clear()
            body.send_keys(text)

            # Switch back to the main content
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            print(f"Error entering online text: {str(e)}")
            return False

    def submit_assignment(self):
        # Click on Save changes button to submit the assignment
        try:
            save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.save_changes_button_xpath)))
            save_button.click()
            return True
        except:
            return False

    def get_submission_status(self):
        # Get the submission status text
        try:
            status_element = self.wait.until(EC.presence_of_element_located((By.XPATH, self.submission_status_xpath)))
            return status_element.text
        except:
            return "Status not found"
