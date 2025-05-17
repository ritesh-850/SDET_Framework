@echo off
echo ===================================================
echo Generating and Viewing Allure Report
echo ===================================================
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
    exit /b 1
)

REM Check if results directory exists
if not exist allure-results (
    echo No test results found in allure-results directory.
    echo Please run tests first using run.bat or run_framework.bat
    echo.
    pause
    exit /b 1
)

echo Generating and serving Allure report...
echo (Press Ctrl+C to stop the server when done)
echo.

REM Serve the Allure report
allure serve allure-results
