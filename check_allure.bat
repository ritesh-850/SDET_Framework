@echo off
echo Checking if Allure is installed...

where allure >nul 2>nul
if %errorlevel% neq 0 (
    echo Allure is not installed. Please install Allure command-line tool.
    echo.
    echo For Windows:
    echo 1. Install Scoop (if not already installed):
    echo    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo    irm get.scoop.sh ^| iex
    echo.
    echo 2. Install Allure using Scoop:
    echo    scoop install allure
    echo.
    echo For more information, see README.md
) else (
    echo Allure is installed.
    allure --version
)

pause
