import pytest
import allure
import os
import tempfile
import time
from POM_CLASS.FileManagement_Page_Object import FileManagement

@allure.epic("BTES LMS Application")
@allure.feature("File Management")
@pytest.mark.usefixtures("setup")
class TestFileManagement:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Upload Private File")
    @allure.description("Test to verify uploading a private file")
    @allure.title("Upload Private File Test")
    def test_upload_private_file(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create file management page object
        file_management = FileManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            file_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to private files
        with allure.step("Navigate to private files"):
            file_management.navigate_to_private_files()
            allure.attach(driver.get_screenshot_as_png(), name="Private_Files_Page", attachment_type=allure.attachment_type.PNG)
        
        # Get initial file list
        with allure.step("Get initial file list"):
            initial_files = file_management.get_file_list()
            allure.attach(
                "\n".join(initial_files).encode('utf-8'),
                name="Initial_File_List",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Create a temporary file for upload
        with allure.step("Create a temporary file for upload"):
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
                temp.write(b"This is a test file created by the automated test.")
                temp_file_path = temp.name
                temp_file_name = os.path.basename(temp_file_path)
        
        # Upload the file
        with allure.step(f"Upload file: {temp_file_path}"):
            try:
                file_management.upload_file(temp_file_path)
                allure.attach(driver.get_screenshot_as_png(), name="After_File_Upload", attachment_type=allure.attachment_type.PNG)
                
                # Save changes
                with allure.step("Save changes"):
                    file_management.save_changes()
                    allure.attach(driver.get_screenshot_as_png(), name="After_Save_Changes", attachment_type=allure.attachment_type.PNG)
                
                # Get updated file list
                with allure.step("Get updated file list"):
                    # Wait for the page to refresh
                    time.sleep(2)
                    
                    updated_files = file_management.get_file_list()
                    allure.attach(
                        "\n".join(updated_files).encode('utf-8'),
                        name="Updated_File_List",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Verify the file was uploaded
                    assert temp_file_name in updated_files, f"File {temp_file_name} was not found in the updated file list"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Uploading_File", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error uploading file: {str(e)}")
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
    
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Delete Private File")
    @allure.description("Test to verify deleting a private file")
    @allure.title("Delete Private File Test")
    def test_delete_private_file(self):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create file management page object
        file_management = FileManagement(driver)

        # Login to the application
        with allure.step("Login to the application"):
            file_management.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Navigate to private files
        with allure.step("Navigate to private files"):
            file_management.navigate_to_private_files()
            allure.attach(driver.get_screenshot_as_png(), name="Private_Files_Page", attachment_type=allure.attachment_type.PNG)
        
        # Get initial file list
        with allure.step("Get initial file list"):
            initial_files = file_management.get_file_list()
            allure.attach(
                "\n".join(initial_files).encode('utf-8'),
                name="Initial_File_List",
                attachment_type=allure.attachment_type.TEXT
            )
            
            if not initial_files:
                pytest.skip("No files found to delete")
        
        # Delete the first file in the list
        with allure.step(f"Delete file: {initial_files[0]}"):
            try:
                file_management.delete_file(initial_files[0])
                allure.attach(driver.get_screenshot_as_png(), name="After_File_Deletion", attachment_type=allure.attachment_type.PNG)
                
                # Save changes
                with allure.step("Save changes"):
                    file_management.save_changes()
                    allure.attach(driver.get_screenshot_as_png(), name="After_Save_Changes", attachment_type=allure.attachment_type.PNG)
                
                # Get updated file list
                with allure.step("Get updated file list"):
                    # Wait for the page to refresh
                    time.sleep(2)
                    
                    updated_files = file_management.get_file_list()
                    allure.attach(
                        "\n".join(updated_files).encode('utf-8'),
                        name="Updated_File_List",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Verify the file was deleted
                    assert initial_files[0] not in updated_files, f"File {initial_files[0]} was still found in the updated file list"
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Deleting_File", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error deleting file: {str(e)}")
