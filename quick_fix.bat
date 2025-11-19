@echo off
chcp 65001 >nul
echo ========================================
echo Tuesday Quick Fix Script
echo ========================================
echo.
echo This script will fix PyQt5 DLL errors
echo by switching to PySide6.
echo.

pause

echo.
echo [1/5] Diagnosing environment...
python diagnose.py
echo.

pause

echo.
echo [2/5] Uninstalling PyQt5...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [3/5] Installing PySide6 and dependencies...
pip install -r requirements-pyside6.txt

echo.
echo [4/5] Converting code to PySide6...
python convert_to_pyside6.py

echo.
echo [5/5] Creating sample database...
python create_sample_db.py

echo.
echo ========================================
echo Fix Complete!
echo.
echo Now run: python main.py
echo Or run main.py in PyCharm
echo ========================================

pause
