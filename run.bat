@echo off
REM Clean previous results
IF EXIST allure-results rmdir /s /q allure-results

REM Run tests with Allure reporting
python -m pytest -v -s TEST_CLASS --alluredir=allure-results

echo.
echo Tests execution completed. Run 'view_report.bat' to see the Allure report.