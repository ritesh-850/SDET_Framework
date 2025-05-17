@echo off
echo Setting up test database...

REM Check if MySQL is installed
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo MySQL is not installed or not in PATH.
    echo Please install MySQL and make sure it's in your PATH.
    pause
    exit /b 1
)

REM Execute the SQL script
mysql -u root -p < TEST_DATA\setup_test_db.sql

if %errorlevel% equ 0 (
    echo Test database setup completed successfully.
) else (
    echo Failed to set up test database.
)

pause
