@echo off
chcp 65001 >nul
echo ========================================
echo Complete Environment Diagnostic
echo ========================================
echo.

echo Running detailed diagnosis...
python detailed_diagnose.py

echo.
echo ========================================
echo.
echo If you see Python 3.14 above, you need to:
echo 1. Create venv with Python 3.10: py -3.10 -m venv venv310
echo 2. Activate it: venv310\Scripts\activate
echo 3. Run this diagnosis again
echo.
echo ========================================

pause
