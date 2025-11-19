@echo off
chcp 65001 >nul
echo ========================================
echo Tuesday Quick Fix Script v2
echo ========================================
echo.
echo This script will fix PyQt5 DLL errors
echo by switching to PySide6.
echo.

pause

echo.
echo [1/4] Diagnosing environment...
python diagnose.py
echo.

pause

echo.
echo [2/4] Uninstalling PyQt5...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [3/4] Installing PySide6 (auto-detecting version)...
python install_pyside6.py

echo.
echo [4/4] Converting code to PySide6...
python convert_to_pyside6.py

echo.
echo ========================================
echo Fix Complete!
echo.
echo Now run: python main.py
echo Or run main.py in PyCharm
echo ========================================

pause
