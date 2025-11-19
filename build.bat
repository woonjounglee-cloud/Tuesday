@echo off
REM Tuesday 빌드 스크립트 (Windows)

echo ===================================
echo Tuesday Build Script
echo ===================================

REM 가상환경 활성화 (선택사항)
REM call venv\Scripts\activate

echo.
echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Creating sample database...
python create_sample_db.py

echo.
echo [3/3] Building executable...
pyinstaller Tuesday.spec

echo.
echo ===================================
echo Build Complete!
echo Executable location: dist\Tuesday.exe
echo ===================================

pause
