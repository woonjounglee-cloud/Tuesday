@echo off
echo ========================================
echo Tuesday 빠른 수정 스크립트
echo ========================================
echo.
echo 이 스크립트는 PyQt5 DLL 오류를 해결하기 위해
echo PySide6로 전환합니다.
echo.

pause

echo.
echo [1/5] 환경 진단 중...
python diagnose.py
echo.

pause

echo.
echo [2/5] 기존 PyQt5 제거 중...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [3/5] PySide6 및 의존성 설치 중...
pip install -r requirements-pyside6.txt

echo.
echo [4/5] 코드 변환 중...
python convert_to_pyside6.py

echo.
echo [5/5] 샘플 데이터베이스 생성 중...
python create_sample_db.py

echo.
echo ========================================
echo 수정 완료!
echo.
echo 이제 다음 명령으로 실행하세요:
echo   python main.py
echo.
echo 또는 PyCharm에서 main.py를 실행하세요.
echo ========================================

pause
