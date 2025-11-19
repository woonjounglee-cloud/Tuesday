@echo off
chcp 65001 >nul
echo ========================================
echo Tuesday Ultimate Fix
echo ========================================
echo.
echo Step 1: Check Python version
python --version
echo.

pause

echo.
echo Step 2: Uninstall PyQt5
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo Step 3: Upgrade pip
python -m pip install --upgrade pip

echo.
echo Step 4: Install PySide6 (simple method)
python install_gui.py

echo.
echo Step 5: Convert code
python convert_to_pyside6.py

echo.
echo Step 6: Create sample database
python create_sample_db.py

echo.
echo ========================================
echo Setup Complete!
echo Now run: python main.py
echo ========================================

pause
