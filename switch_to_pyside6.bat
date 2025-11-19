@echo off
chcp 65001 >nul
echo ===================================
echo Switch to PySide6
echo ===================================
echo.
echo If PyQt5 DLL errors persist, we can use PySide6 instead.
echo PySide6 is similar to PyQt5 but provides better compatibility.
echo.

pause

echo.
echo [1/4] Removing PyQt5...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [2/4] Installing PySide6...
pip install PySide6==6.5.2

echo.
echo [3/4] Converting code...
python convert_to_pyside6.py

echo.
echo [4/4] Testing...
python -c "from PySide6.QtWidgets import QApplication; print('PySide6 installed successfully!')"

echo.
echo ===================================
echo Conversion Complete!
echo Now run: python main.py
echo ===================================

pause
