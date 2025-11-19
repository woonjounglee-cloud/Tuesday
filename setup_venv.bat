@echo off
REM 가상환경 설정 스크립트

echo ===================================
echo Virtual Environment Setup
echo ===================================

echo.
echo [1/5] Creating virtual environment...
python -m venv venv

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt

echo.
echo [5/5] Creating sample database...
python create_sample_db.py

echo.
echo ===================================
echo Setup Complete!
echo.
echo To activate the virtual environment:
echo   venv\Scripts\activate
echo.
echo To run Tuesday:
echo   python main.py
echo ===================================

pause
