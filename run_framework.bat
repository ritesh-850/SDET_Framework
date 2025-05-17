@echo off
setlocal enabledelayedexpansion

echo ================================================================
echo BTES LMS Test Framework Runner
echo ================================================================
echo.

:menu
echo Please select an option:
echo 1. Run all tests
echo 2. Run UI tests only
echo 3. Run database tests only
echo 4. Run data-driven login tests only
echo 5. Run specific test class
echo 6. Setup test database
echo 7. Generate Allure report from existing results
echo 8. Exit
echo.

set /p choice=Enter your choice (1-8):

if "%choice%"=="1" goto run_all
if "%choice%"=="2" goto run_ui
if "%choice%"=="3" goto run_db
if "%choice%"=="4" goto run_login_data
if "%choice%"=="5" goto run_specific
if "%choice%"=="6" goto setup_db
if "%choice%"=="7" goto generate_report
if "%choice%"=="8" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:run_all
echo.
echo ================================================================
echo Running all tests...
echo ================================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

REM Run all tests with Allure reporting
python -m pytest -v TEST_CLASS/ DB_TESTS/ DATA_DRIVEN_TESTS/ --alluredir=allure-results

goto generate_report

:run_ui
echo.
echo ================================================================
echo Running UI tests only...
echo ================================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

REM Run UI tests (excluding database tests)
python -m pytest -v TEST_CLASS/ -k "not Database and not DB_Validation" --alluredir=allure-results

goto generate_report

:run_db
echo.
echo ================================================================
echo Running database tests only...
echo ================================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

REM Run database tests
python -m pytest -v .\DB_TESTS\ --alluredir=allure-results

goto generate_report

:run_login_data
echo.
echo ================================================================
echo Running data-driven login tests only...
echo ================================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

REM Run data-driven login tests
python -m pytest -v .\DATA_DRIVEN_TESTS\ --alluredir=allure-results

goto generate_report

:run_specific
echo.
echo ================================================================
echo Available test classes:
echo ================================================================
echo.

echo Test classes in TEST_CLASS directory:
dir /b TEST_CLASS\Test_*.py

echo.
echo Test classes in DB_TESTS directory:
dir /b DB_TESTS\Test_*.py

echo.
echo Test classes in DATA_DRIVEN_TESTS directory:
dir /b DATA_DRIVEN_TESTS\Test_*.py

echo.
echo Enter the test class name with its directory (e.g., TEST_CLASS\Test_Login.py)
echo or just the class name if it's in TEST_CLASS directory (e.g., Test_Login.py)
set /p test_path=Enter the test path:

REM Check if the path includes a directory
echo %test_path% | findstr /C:"\\"
if %errorlevel% EQU 0 (
    REM Path includes directory
    set full_path=%test_path%
) else (
    REM Path is just a filename, assume TEST_CLASS directory
    set full_path=TEST_CLASS\%test_path%
)

if not exist "%full_path%" (
    echo Test class not found: %full_path%
    echo.
    goto menu
)

echo.
echo ================================================================
echo Running %full_path%...
echo ================================================================
echo.

REM Clean previous results
echo Cleaning previous test results...
IF EXIST allure-results rmdir /s /q allure-results
mkdir allure-results

REM Run specific test class
python -m pytest -v %full_path% --alluredir=allure-results

goto generate_report

:setup_db
echo.
echo ================================================================
echo Setting up test database...
echo ================================================================
echo.

REM Check if MySQL is installed
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo MySQL is not installed or not in PATH.
    echo Please install MySQL and make sure it's in your PATH.
    echo.
    goto menu
)

REM Get MySQL credentials
set /p mysql_user=Enter MySQL username (default: root):
if "!mysql_user!"=="" set mysql_user=root

set /p mysql_password=Enter MySQL password:

REM Execute the SQL script
mysql -u !mysql_user! -p!mysql_password! < TEST_DATA\setup_test_db.sql

if %errorlevel% equ 0 (
    echo Test database setup completed successfully.
) else (
    echo Failed to set up test database.
)

echo.
pause
goto menu

:generate_report
echo.
echo ================================================================
echo Generating Allure report...
echo ================================================================
echo.

REM Check if Allure is installed
where allure >nul 2>nul
if %errorlevel% neq 0 (
    echo Allure is not installed or not in PATH.
    echo Please install Allure command-line tool.
    echo.
    echo For Windows:
    echo 1. Install Scoop (if not already installed):
    echo    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo    irm get.scoop.sh ^| iex
    echo.
    echo 2. Install Allure using Scoop:
    echo    scoop install allure
    echo.
    pause
    goto menu
)

REM Generate Allure report
allure generate allure-results -o allure-report --clean

echo.
echo ================================================================
echo Opening Allure report...
echo ================================================================
echo.

REM Open the report
start allure-report\index.html

echo.
echo ================================================================
echo Report is available at: %CD%\allure-report\index.html
echo ================================================================
echo.

pause
goto menu

:end
echo.
echo ================================================================
echo Thank you for using the BTES LMS Test Framework
echo ================================================================
echo.
endlocal
