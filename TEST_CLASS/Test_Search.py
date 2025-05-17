import pytest
import allure
from POM_CLASS.Search_Page_Object import Search

@allure.epic("BTES LMS Application")
@allure.feature("Search Functionality")
@pytest.mark.usefixtures("setup")
class TestSearch:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Search for Courses")
    @allure.description("Test to verify search functionality")
    @allure.title("Search Functionality Test")
    @pytest.mark.parametrize("search_term", ["Python", "SDET", "Java"])
    def test_search(self, search_term):
        # Get the driver from the fixture
        driver = self.driver

        # Navigate to the application URL
        with allure.step("Navigate to the application URL"):
            driver.get("https://online.btes.co.in/login/index.php")
            allure.attach(driver.get_screenshot_as_png(), name="Login_Page", attachment_type=allure.attachment_type.PNG)

        # Create search page object
        search = Search(driver)

        # Login to the application
        with allure.step("Login to the application"):
            search.login("ritesh@123", "Ritesh@123")
            allure.attach(driver.get_screenshot_as_png(), name="After_Login", attachment_type=allure.attachment_type.PNG)
        
        # Perform search
        with allure.step(f"Search for term: {search_term}"):
            try:
                search.perform_search(search_term)
                allure.attach(driver.get_screenshot_as_png(), name=f"Search_Results_{search_term}", attachment_type=allure.attachment_type.PNG)
                
                # Verify search results
                with allure.step("Verify search results"):
                    is_search_successful = search.is_search_successful()
                    allure.attach(driver.get_screenshot_as_png(), name="Search_Results_Verification", attachment_type=allure.attachment_type.PNG)
                    
                    # We're just checking if the search functionality works, not specific results
                    assert is_search_successful, f"Search for '{search_term}' failed to return results page"
                    
                    # Optional: Check if we got any results
                    try:
                        results_count = search.get_search_results_count()
                        allure.attach(
                            f"Found {results_count} results for search term '{search_term}'".encode('utf-8'),
                            name="Search_Results_Count",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    except:
                        # It's okay if we can't count results
                        pass
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_During_Search", attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Error during search: {str(e)}")
