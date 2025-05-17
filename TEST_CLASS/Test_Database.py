import pytest
import allure
import os
import json
import mysql.connector
from mysql.connector import Error
from UTILITIES.db_utils import DatabaseConnection

# Get the absolute path to the test data files
db_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TEST_DATA", "db_config.json")
db_test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TEST_DATA", "db_test_data.json")
db_setup_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TEST_DATA", "setup_test_db.sql")

# Load test data
with open(db_test_data_path, 'r') as f:
    test_data = json.load(f)

@allure.epic("BTES LMS Database")
@allure.feature("Database Operations")
class TestDatabase:

    @classmethod
    def setup_class(cls):
        """Set up the test database before running tests."""
        # Connect to MySQL server (without specifying a database)
        try:
            with open(db_config_path, 'r') as f:
                config = json.load(f)

            # Create a connection to MySQL server (without database)
            connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )

            if connection.is_connected():
                cursor = connection.cursor()

                # Read and execute the setup script
                with open(db_setup_script_path, 'r') as script_file:
                    script = script_file.read()

                    # Split the script into individual statements
                    statements = script.split(';')

                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement)

                connection.commit()
                allure.attach("Database setup completed successfully", name="Setup_Result", attachment_type=allure.attachment_type.TEXT)
        except Error as e:
            allure.attach(f"Error setting up database: {str(e)}", name="Setup_Error", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Failed to set up test database: {str(e)}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    @pytest.fixture(scope="function")
    def db_connection(self):
        """Fixture to provide a database connection for each test."""
        connection = DatabaseConnection(config_file=db_config_path)
        connection.connect()
        yield connection
        connection.disconnect()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("User Management")
    @allure.description("Test creating, reading, updating, and deleting users")
    @allure.title("User CRUD Operations Test")
    def test_user_crud_operations(self, db_connection):
        """Test CRUD operations for users."""
        # Test data
        test_users = test_data['users']

        # CREATE - Insert a new user
        with allure.step("Create a new user"):
            user_data = test_users[0]
            user_id = db_connection.insert_data('users', user_data)

            allure.attach(
                f"User created with ID: {user_id}\nData: {json.dumps(user_data, indent=2)}",
                name="Create_User_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert user_id is not None, "Failed to insert user"

        # READ - Retrieve the user
        with allure.step("Read the user data"):
            query = "SELECT * FROM users WHERE id = %s"
            result = db_connection.execute_query(query, (user_id,))

            allure.attach(
                f"User data retrieved: {json.dumps(result[0], indent=2, default=str)}",
                name="Read_User_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(result) == 1, "User not found"
            assert result[0]['username'] == user_data['username'], "Username does not match"
            assert result[0]['email'] == user_data['email'], "Email does not match"

        # UPDATE - Update the user
        with allure.step("Update the user data"):
            update_data = {
                'first_name': 'Updated',
                'last_name': 'User'
            }
            rows_affected = db_connection.update_data('users', update_data, f"id = {user_id}")

            allure.attach(
                f"User updated. Rows affected: {rows_affected}\nUpdate data: {json.dumps(update_data, indent=2)}",
                name="Update_User_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert rows_affected == 1, "Failed to update user"

            # Verify update
            result = db_connection.execute_query(query, (user_id,))
            assert result[0]['first_name'] == update_data['first_name'], "First name not updated"
            assert result[0]['last_name'] == update_data['last_name'], "Last name not updated"

        # DELETE - Delete the user
        with allure.step("Delete the user"):
            rows_affected = db_connection.delete_data('users', f"id = {user_id}")

            allure.attach(
                f"User deleted. Rows affected: {rows_affected}",
                name="Delete_User_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert rows_affected == 1, "Failed to delete user"

            # Verify deletion
            result = db_connection.execute_query(query, (user_id,))
            assert len(result) == 0, "User was not deleted"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Course Management")
    @allure.description("Test creating, reading, updating, and deleting courses")
    @allure.title("Course CRUD Operations Test")
    def test_course_crud_operations(self, db_connection):
        """Test CRUD operations for courses."""
        # Test data
        test_courses = test_data['courses']

        # CREATE - Insert a new course
        with allure.step("Create a new course"):
            course_data = test_courses[0]
            course_id = db_connection.insert_data('courses', course_data)

            allure.attach(
                f"Course created with ID: {course_id}\nData: {json.dumps(course_data, indent=2)}",
                name="Create_Course_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert course_id is not None, "Failed to insert course"

        # READ - Retrieve the course
        with allure.step("Read the course data"):
            query = "SELECT * FROM courses WHERE id = %s"
            result = db_connection.execute_query(query, (course_id,))

            allure.attach(
                f"Course data retrieved: {json.dumps(result[0], indent=2, default=str)}",
                name="Read_Course_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(result) == 1, "Course not found"
            assert result[0]['course_name'] == course_data['course_name'], "Course name does not match"
            assert result[0]['course_code'] == course_data['course_code'], "Course code does not match"

        # UPDATE - Update the course
        with allure.step("Update the course data"):
            update_data = {
                'course_name': 'Updated Course',
                'description': 'Updated course description'
            }
            rows_affected = db_connection.update_data('courses', update_data, f"id = {course_id}")

            allure.attach(
                f"Course updated. Rows affected: {rows_affected}\nUpdate data: {json.dumps(update_data, indent=2)}",
                name="Update_Course_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert rows_affected == 1, "Failed to update course"

            # Verify update
            result = db_connection.execute_query(query, (course_id,))
            assert result[0]['course_name'] == update_data['course_name'], "Course name not updated"
            assert result[0]['description'] == update_data['description'], "Description not updated"

        # DELETE - Delete the course
        with allure.step("Delete the course"):
            rows_affected = db_connection.delete_data('courses', f"id = {course_id}")

            allure.attach(
                f"Course deleted. Rows affected: {rows_affected}",
                name="Delete_Course_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert rows_affected == 1, "Failed to delete course"

            # Verify deletion
            result = db_connection.execute_query(query, (course_id,))
            assert len(result) == 0, "Course was not deleted"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Enrollment Management")
    @allure.description("Test enrolling users in courses using stored procedure")
    @allure.title("Enrollment Stored Procedure Test")
    @pytest.mark.parametrize("user_id,course_id,expected_success", [
        (4, 4, True),  # Valid enrollment
        (5, 4, True),  # Valid enrollment
        (4, 1, False), # Already enrolled
        (999, 1, False), # User doesn't exist
        (4, 999, False) # Course doesn't exist
    ])
    def test_enrollment_stored_procedure(self, db_connection, user_id, course_id, expected_success):
        """Test the stored procedure for enrolling users in courses."""
        # Set up test case title for Allure
        test_case_title = f"Enroll User {user_id} in Course {course_id} - Expected: {'Success' if expected_success else 'Failure'}"
        allure.dynamic.title(test_case_title)

        with allure.step(f"Call stored procedure to enroll user {user_id} in course {course_id}"):
            try:
                # Call the stored procedure
                db_connection.call_procedure('enroll_user_in_course', (user_id, course_id), commit=True)

                # Check if enrollment was successful
                query = "SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s"
                result = db_connection.execute_query(query, (user_id, course_id))

                if expected_success:
                    allure.attach(
                        f"Enrollment successful. Result: {json.dumps(result[0], indent=2, default=str) if result else 'No result'}",
                        name="Enrollment_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert len(result) == 1, "Enrollment record not found"
                else:
                    allure.attach(
                        "Enrollment should have failed but succeeded",
                        name="Enrollment_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert False, "Enrollment should have failed but succeeded"
            except Error as e:
                error_message = str(e)
                allure.attach(
                    f"Error: {error_message}",
                    name="Enrollment_Error",
                    attachment_type=allure.attachment_type.TEXT
                )

                if expected_success:
                    assert False, f"Enrollment should have succeeded but failed: {error_message}"
                else:
                    # Expected failure, so this is correct behavior
                    assert True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Assignment Submission")
    @allure.description("Test submitting assignments using stored procedure")
    @allure.title("Assignment Submission Stored Procedure Test")
    @pytest.mark.parametrize("assignment_id,user_id,submission_text,file_path,expected_success", [
        (1, 4, "Test submission", "test.txt", True),  # Valid submission
        (2, 5, "Another test", "another.txt", True),  # Valid submission
        (1, 4, "Updated submission", "updated.txt", True),  # Update existing submission
        (999, 4, "Invalid assignment", "invalid.txt", False),  # Assignment doesn't exist
        (1, 999, "Invalid user", "invalid.txt", False)  # User not enrolled
    ])
    def test_assignment_submission_procedure(self, db_connection, assignment_id, user_id, submission_text, file_path, expected_success):
        """Test the stored procedure for submitting assignments."""
        # Set up test case title for Allure
        test_case_title = f"Submit Assignment {assignment_id} for User {user_id} - Expected: {'Success' if expected_success else 'Failure'}"
        allure.dynamic.title(test_case_title)

        with allure.step(f"Call stored procedure to submit assignment {assignment_id} for user {user_id}"):
            try:
                # Call the stored procedure
                db_connection.call_procedure('submit_assignment', (assignment_id, user_id, submission_text, file_path), commit=True)

                # Check if submission was successful
                query = "SELECT * FROM assignment_submissions WHERE assignment_id = %s AND user_id = %s"
                result = db_connection.execute_query(query, (assignment_id, user_id))

                if expected_success:
                    allure.attach(
                        f"Submission successful. Result: {json.dumps(result[0], indent=2, default=str) if result else 'No result'}",
                        name="Submission_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert len(result) == 1, "Submission record not found"
                    assert result[0]['submission_text'] == submission_text, "Submission text does not match"
                    assert result[0]['file_path'] == file_path, "File path does not match"
                else:
                    allure.attach(
                        "Submission should have failed but succeeded",
                        name="Submission_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert False, "Submission should have failed but succeeded"
            except Error as e:
                error_message = str(e)
                allure.attach(
                    f"Error: {error_message}",
                    name="Submission_Error",
                    attachment_type=allure.attachment_type.TEXT
                )

                if expected_success:
                    assert False, f"Submission should have succeeded but failed: {error_message}"
                else:
                    # Expected failure, so this is correct behavior
                    assert True

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Assignment Grading")
    @allure.description("Test grading assignments using stored procedure")
    @allure.title("Assignment Grading Stored Procedure Test")
    @pytest.mark.parametrize("submission_id,score,feedback,expected_success", [
        (1, 90, "Updated feedback", True),  # Valid grading
        (2, 145, "Great work", True),  # Valid grading
        (999, 80, "Invalid submission", False),  # Submission doesn't exist
        (1, 999, "Score too high", False)  # Score exceeds maximum
    ])
    def test_assignment_grading_procedure(self, db_connection, submission_id, score, feedback, expected_success):
        """Test the stored procedure for grading assignments."""
        # Set up test case title for Allure
        test_case_title = f"Grade Submission {submission_id} with Score {score} - Expected: {'Success' if expected_success else 'Failure'}"
        allure.dynamic.title(test_case_title)

        with allure.step(f"Call stored procedure to grade submission {submission_id} with score {score}"):
            try:
                # Call the stored procedure
                db_connection.call_procedure('grade_assignment', (submission_id, score, feedback), commit=True)

                # Check if grading was successful
                query = "SELECT * FROM assignment_submissions WHERE id = %s"
                result = db_connection.execute_query(query, (submission_id,))

                if expected_success:
                    allure.attach(
                        f"Grading successful. Result: {json.dumps(result[0], indent=2, default=str) if result else 'No result'}",
                        name="Grading_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert len(result) == 1, "Submission record not found"
                    assert float(result[0]['score']) == float(score), "Score does not match"
                    assert result[0]['feedback'] == feedback, "Feedback does not match"
                else:
                    allure.attach(
                        "Grading should have failed but succeeded",
                        name="Grading_Result",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert False, "Grading should have failed but succeeded"
            except Error as e:
                error_message = str(e)
                allure.attach(
                    f"Error: {error_message}",
                    name="Grading_Error",
                    attachment_type=allure.attachment_type.TEXT
                )

                if expected_success:
                    assert False, f"Grading should have succeeded but failed: {error_message}"
                else:
                    # Expected failure, so this is correct behavior
                    assert True

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Complex Queries")
    @allure.description("Test complex queries for retrieving related data")
    @allure.title("Complex Query Test")
    @pytest.mark.parametrize("query_name,param_value,expected_min_rows", [
        ("user_courses", 4, 2),  # Courses for user 4
        ("user_courses", 6, 3),  # Courses for user 6
        ("course_students", 1, 2),  # Students in course 1
        ("course_students", 3, 2),  # Students in course 3
        ("assignment_submissions", 1, 2),  # Submissions for assignment 1
        ("assignment_submissions", 3, 1),  # Submissions for assignment 3
        ("user_grades", 4, 1),  # Grades for user 4
        ("user_grades", 5, 1)   # Grades for user 5
    ])
    def test_complex_queries(self, db_connection, query_name, param_value, expected_min_rows):
        """Test complex queries for retrieving related data."""
        # Set up test case title for Allure
        test_case_title = f"Execute {query_name} Query with Parameter {param_value}"
        allure.dynamic.title(test_case_title)

        with allure.step(f"Execute {query_name} query with parameter {param_value}"):
            # Get the query from test data
            query = test_data['queries'][query_name]

            # Execute the query
            result = db_connection.execute_query(query, (param_value,))

            allure.attach(
                f"Query: {query}\nParameter: {param_value}\nResult: {json.dumps(result, indent=2, default=str)}",
                name="Query_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            # Verify the result
            assert len(result) >= expected_min_rows, f"Expected at least {expected_min_rows} rows, got {len(result)}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Batch Operations")
    @allure.description("Test batch insert operations")
    @allure.title("Batch Insert Test")
    def test_batch_insert(self, db_connection):
        """Test batch insert operations."""
        # Test data
        test_users = test_data['users'][1:3]  # Use two test users

        with allure.step("Prepare data for batch insert"):
            # Prepare data for batch insert
            insert_query = "INSERT INTO users (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            params_list = [
                (user['username'], user['password'], user['email'], user['first_name'], user['last_name'])
                for user in test_users
            ]

            allure.attach(
                f"Query: {insert_query}\nParameters: {json.dumps(params_list, indent=2)}",
                name="Batch_Insert_Data",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Execute batch insert"):
            # Execute batch insert
            rows_affected = db_connection.execute_many(insert_query, params_list)

            allure.attach(
                f"Rows affected: {rows_affected}",
                name="Batch_Insert_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert rows_affected == len(params_list), f"Expected {len(params_list)} rows affected, got {rows_affected}"

        with allure.step("Verify inserted data"):
            # Verify inserted data
            usernames = [user['username'] for user in test_users]
            placeholders = ', '.join(['%s'] * len(usernames))
            query = f"SELECT * FROM users WHERE username IN ({placeholders})"

            result = db_connection.execute_query(query, usernames)

            allure.attach(
                f"Query: {query}\nParameters: {usernames}\nResult: {json.dumps(result, indent=2, default=str)}",
                name="Verification_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(result) == len(test_users), f"Expected {len(test_users)} rows, got {len(result)}"

            # Clean up - delete the inserted users
            delete_query = f"DELETE FROM users WHERE username IN ({placeholders})"
            db_connection.execute_query(delete_query, usernames, commit=True)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Transaction Management")
    @allure.description("Test transaction management with rollback")
    @allure.title("Transaction Rollback Test")
    def test_transaction_rollback(self, db_connection):
        """Test transaction management with rollback."""
        # Test data
        test_user = test_data['users'][0]

        with allure.step("Start transaction and insert user"):
            # Start transaction (don't commit)
            insert_query = "INSERT INTO users (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            params = (test_user['username'], test_user['password'], test_user['email'], test_user['first_name'], test_user['last_name'])

            # Execute insert without committing
            db_connection.execute_query(insert_query, params, commit=False)

            allure.attach(
                f"User inserted (not committed): {test_user['username']}",
                name="Insert_Result",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify user is visible within transaction"):
            # Verify user is visible within the transaction
            query = "SELECT * FROM users WHERE username = %s"
            result = db_connection.execute_query(query, (test_user['username'],))

            allure.attach(
                f"Query result within transaction: {json.dumps(result, indent=2, default=str)}",
                name="Within_Transaction_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(result) == 1, "User should be visible within the transaction"

        with allure.step("Rollback transaction"):
            # Rollback the transaction
            if db_connection.connection:
                db_connection.connection.rollback()

                allure.attach(
                    "Transaction rolled back",
                    name="Rollback_Result",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("Verify user is not visible after rollback"):
            # Verify user is not visible after rollback
            result = db_connection.execute_query(query, (test_user['username'],))

            allure.attach(
                f"Query result after rollback: {json.dumps(result, indent=2, default=str)}",
                name="After_Rollback_Result",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(result) == 0, "User should not be visible after rollback"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Error Handling")
    @allure.description("Test error handling for invalid operations")
    @allure.title("Error Handling Test")
    @pytest.mark.parametrize("operation,expected_error", [
        ("duplicate_user", "Duplicate entry"),
        ("invalid_foreign_key", "foreign key constraint fails"),
        ("invalid_data_type", "Incorrect")
    ])
    def test_error_handling(self, db_connection, operation, expected_error):
        """Test error handling for invalid operations."""
        # Set up test case title for Allure
        test_case_title = f"Error Handling for {operation}"
        allure.dynamic.title(test_case_title)

        with allure.step(f"Attempt invalid operation: {operation}"):
            try:
                if operation == "duplicate_user":
                    # First insert a user
                    user_data = test_data['users'][0]
                    db_connection.insert_data('users', user_data)

                    # Try to insert the same user again (should fail)
                    db_connection.insert_data('users', user_data)

                elif operation == "invalid_foreign_key":
                    # Try to insert enrollment with invalid user_id
                    enrollment_data = {
                        'user_id': 999,
                        'course_id': 1,
                        'completion_status': 'not_started'
                    }
                    db_connection.insert_data('enrollments', enrollment_data)

                elif operation == "invalid_data_type":
                    # Try to insert invalid data type
                    query = "INSERT INTO assignments (course_id, title, description, due_date, max_score) VALUES (%s, %s, %s, %s, %s)"
                    params = (1, "Test Assignment", "Description", "not-a-date", 100)
                    db_connection.execute_query(query, params, commit=True)

                allure.attach(
                    f"Operation succeeded when it should have failed: {operation}",
                    name="Unexpected_Success",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert False, f"Operation {operation} should have failed but succeeded"

            except Error as e:
                error_message = str(e)
                allure.attach(
                    f"Error message: {error_message}",
                    name="Error_Message",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Verify the error message contains the expected text
                assert expected_error in error_message, f"Expected error message to contain '{expected_error}', got '{error_message}'"

            finally:
                # Clean up - make sure to rollback any pending transactions
                if db_connection.connection:
                    db_connection.connection.rollback()

                    # If we inserted a user, try to delete it
                    if operation == "duplicate_user":
                        try:
                            db_connection.delete_data('users', f"username = '{test_data['users'][0]['username']}'")
                        except:
                            pass
