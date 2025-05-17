@echo off
echo Generating HTML report...

REM Clean previous results
IF EXIST reports rmdir /s /q reports
mkdir reports

REM Run tests with HTML reporting
python -m pytest -v -s TEST_CLASS --html=reports/report.html --self-contained-html

echo.
echo HTML report generated at reports/report.html
echo.

REM Open the report in the default browser
start reports\report.html

pause
