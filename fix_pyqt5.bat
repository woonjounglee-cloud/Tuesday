@echo off
chcp 65001 >nul
echo ===================================
echo PyQt5 DLL Error Fix Script
echo ===================================

echo.
echo [1/4] Uninstalling existing PyQt5...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/4] Installing PyQt5...
pip install PyQt5==5.15.9

echo.
echo [4/4] Testing PyQt5...
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 installed successfully!')"

echo.
echo ===================================
echo If you still get errors, you may need to install:
echo Microsoft Visual C++ Redistributable 2015-2022 (x64)
echo Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
echo ===================================

pause
