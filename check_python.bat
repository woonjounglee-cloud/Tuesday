@echo off
chcp 65001 >nul
echo ========================================
echo Python Version Checker
echo ========================================
echo.
echo Checking available Python versions...
echo.

echo Python 3.14:
python --version 2>nul
echo Location:
where python

echo.
echo Python 3.10 (if installed):
py -3.10 --version 2>nul || echo Not found in py launcher

echo.
echo Python 3.11 (if installed):
py -3.11 --version 2>nul || echo Not found in py launcher

echo.
echo Python 3.9 (if installed):
py -3.9 --version 2>nul || echo Not found in py launcher

echo.
echo ========================================
echo Checking C:\Python310:
echo ========================================
if exist "C:\Python310\python.exe" (
    echo Found: C:\Python310\python.exe
    C:\Python310\python.exe --version
) else (
    echo Not found: C:\Python310\python.exe
)

echo.
echo ========================================
echo Checking C:\Users\%USERNAME%\AppData\Local\Programs\Python:
echo ========================================
dir /b "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python3*" 2>nul

echo.
pause
