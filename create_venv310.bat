@echo off
chcp 65001 >nul
echo ========================================
echo Create Python 3.10 Virtual Environment
echo ========================================
echo.

echo Step 1: Finding Python 3.10...
echo.

REM Try py launcher first
py -3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3.10 via py launcher
    set PYTHON_CMD=py -3.10
    goto :create_venv
)

REM Try C:\Python310
if exist "C:\Python310\python.exe" (
    echo Found Python 3.10 at C:\Python310
    set PYTHON_CMD=C:\Python310\python.exe
    goto :create_venv
)

REM Try AppData location
for /d %%i in ("C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310*") do (
    if exist "%%i\python.exe" (
        echo Found Python 3.10 at %%i
        set PYTHON_CMD=%%i\python.exe
        goto :create_venv
    )
)

echo.
echo ========================================
echo ERROR: Python 3.10 not found!
echo ========================================
echo.
echo Please install Python 3.10.11 from:
echo https://www.python.org/downloads/release/python-31011/
echo.
echo Make sure to check "Add Python to PATH" during installation.
echo ========================================
pause
exit /b 1

:create_venv
echo.
echo Step 2: Creating virtual environment with Python 3.10...
%PYTHON_CMD% -m venv venv310

echo.
echo Step 3: Activating virtual environment...
call venv310\Scripts\activate

echo.
echo Step 4: Verifying Python version...
python --version

echo.
echo Step 5: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 6: Installing packages...
pip install PySide6 openpyxl matplotlib

echo.
echo Step 7: Converting code to PySide6...
python convert_to_pyside6.py

echo.
echo Step 8: Creating sample database...
python create_sample_db.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your virtual environment is activated.
echo Python version in this environment:
python --version
echo.
echo To run Tuesday:
echo   python main.py
echo.
echo To activate this environment later:
echo   venv310\Scripts\activate
echo.
echo IMPORTANT: In PyCharm, set interpreter to:
echo   %CD%\venv310\Scripts\python.exe
echo ========================================

pause
