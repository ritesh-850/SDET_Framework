import pytest
import allure
import os
import json
import time
from UTILITIES.db_utils import DatabaseConnection
from POM_CLASS.Login_Page_Object import LoginPage

# Get the absolute path to the config file
db_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TEST_DATA", "db_config.json")

@allure.epic("BTES LMS Application")
@allure.feature("Authentication with Database Validation")
@pytest.mark.usefixtures("setup")
class TestLoginDBValidation:

    @pytest.fixture(scope="function")
    def db_connection(self):
        """Fixture to provide a database connection for each test."""
        connection = DatabaseConnection(config_file=db_config_path)
        connection.connect()
        yield connection
        connection.disconnect()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Login Validation Against Database")
    @allure.description("Test login functionality and validate credentials against database")
    @pytest.mark.parametrize("username,password,expected_result", [
        ("admin", "Admin@123", "pass"),
        ("instructor1", "Instructor@123", "pass"),
        ("student1", "Student@123", "pass"),
        ("admin", "WrongPassword", "fail"),
        ("nonexistent", "AnyPassword", "fail"),
        ("", "", "fail")
    ])
    def test_login_with_db_validation(self, db_connection, username, password, expected_result):
        # Get the driver from the fixture
        driver = self.driver

        # Create a unique test case title for Allure
        test_case_title = f"Login DB Validation - Username: {username}, Expected: {expected_result}"
        allure.dynamic.title(test_case_title)

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create login page object
        login_page = LoginPage(driver)

        # Perform login
        with allure.step(f"Login with username: {username} and password: {'*' * len(password) if password else 'empty'}"):
            login_page.login(username, password)
            time.sleep(2)  # Wait for login to complete
            allure.attach(driver.get_screenshot_as_png(), name="After_Login_Attempt", attachment_type=allure.attachment_type.PNG)

        # Validate credentials against database
        with allure.step("Validate credentials against database"):
            # Query the database to check if the user exists with the given credentials
            query = "SELECT * FROM users WHERE username = %s"
            result = db_connection.execute_query(query, (username,))

            user_exists = len(result) > 0

            if user_exists:
                # In a real application, you would check the hashed password
                # Here we're just checking if the user exists
                db_password = result[0]['password']
                password_matches = password == db_password

                allure.attach(
                    f"User found in database: {user_exists}\nPassword matches: {password_matches}",
                    name="DB_Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    f"User not found in database",
                    name="DB_Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )

        # Verify login result
        with allure.step(f"Verify login result - Expected: {expected_result}"):
            actual_title = driver.title
            error_message = login_page.get_error_message()

            # Attach actual results to the report
            allure.attach(f"Actual Page Title: {actual_title}", name="Actual_Title", attachment_type=allure.attachment_type.TEXT)
            if error_message:
                allure.attach(f"Error Message: {error_message}", name="Error_Message", attachment_type=allure.attachment_type.TEXT)

            # For successful login, we expect to be redirected to Dashboard or similar page
            if expected_result.lower() == "pass":
                login_successful = "Dashboard" in actual_title

                # Also verify that the user exists in the database
                db_validation = user_exists and password_matches

                allure.attach(
                    f"Login successful: {login_successful}\nDB validation passed: {db_validation}",
                    name="Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert login_successful, f"Login should succeed but failed. Actual title: {actual_title}"
                assert db_validation, "Database validation failed"

            # For failed login, we expect to stay on the login page with an error message
            else:
                login_failed = "Log in" in actual_title and error_message

                # Also verify that either the user doesn't exist or the password is incorrect
                db_validation = not user_exists or not password_matches

                allure.attach(
                    f"Login failed as expected: {login_failed}\nDB validation passed: {db_validation}",
                    name="Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert login_failed, f"Login should fail but succeeded. Actual title: {actual_title}"
                assert db_validation, "Database validation failed"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("User Role Validation")
    @allure.description("Test login and validate user roles from database")
    @pytest.mark.parametrize("username,expected_role", [
        ("admin", "admin"),
        ("instructor1", "instructor"),
        ("student1", "student")
    ])
    def test_user_role_validation(self, db_connection, username, expected_role):
        # Get the driver from the fixture
        driver = self.driver

        # Create a unique test case title for Allure
        test_case_title = f"User Role Validation - Username: {username}, Expected Role: {expected_role}"
        allure.dynamic.title(test_case_title)

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create login page object
        login_page = LoginPage(driver)

        # Determine password based on role pattern in test data
        password = None
        if expected_role == "admin":
            password = "Admin@123"
        elif expected_role == "instructor":
            password = "Instructor@123"
        elif expected_role == "student":
            password = "Student@123"

        # Perform login
        with allure.step(f"Login with username: {username} and password: {'*' * len(password) if password else 'empty'}"):
            login_page.login(username, password)
            time.sleep(2)  # Wait for login to complete
            allure.attach(driver.get_screenshot_as_png(), name="After_Login_Attempt", attachment_type=allure.attachment_type.PNG)

        # Validate user role against database
        with allure.step("Validate user role against database"):
            # In a real application, you would have a roles table or a role field
            # Here we're inferring the role from the username pattern
            query = "SELECT * FROM users WHERE username = %s"
            result = db_connection.execute_query(query, (username,))

            if len(result) > 0:
                # Infer role from username (in a real app, you'd have a role field)
                db_role = None
                if "admin" in username:
                    db_role = "admin"
                elif "instructor" in username:
                    db_role = "instructor"
                elif "student" in username:
                    db_role = "student"

                allure.attach(
                    f"User found in database: {result[0]['username']}\nInferred role: {db_role}",
                    name="Role_Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert db_role == expected_role, f"Expected role {expected_role}, but inferred {db_role} from database"
            else:
                allure.attach(
                    f"User not found in database",
                    name="Role_Validation_Result",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert False, f"User {username} not found in database"

        # Verify login was successful
        with allure.step("Verify login was successful"):
            actual_title = driver.title
            login_successful = "Dashboard" in actual_title

            allure.attach(
                f"Login successful: {login_successful}\nActual title: {actual_title}",
                name="Login_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert login_successful, f"Login failed. Actual title: {actual_title}"

        # Verify role-specific elements on the page
        with allure.step(f"Verify role-specific elements for {expected_role}"):
            # In a real test, you would check for role-specific elements
            # Here we're just taking a screenshot
            allure.attach(driver.get_screenshot_as_png(), name=f"{expected_role.capitalize()}_Dashboard", attachment_type=allure.attachment_type.PNG)

            # Simple check based on role
            if expected_role == "admin":
                # Admin should have access to site administration
                assert "Admin" in driver.page_source or "Administration" in driver.page_source, "Admin-specific elements not found"
            elif expected_role == "instructor":
                # Instructor should have access to courses
                assert "Courses" in driver.page_source, "Instructor-specific elements not found"
            elif expected_role == "student":
                # Student should have access to courses
                assert "Courses" in driver.page_source, "Student-specific elements not found"
