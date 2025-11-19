@echo off
REM PyQt5에서 PySide6로 전환 스크립트

echo ===================================
echo Switch to PySide6
echo ===================================
echo.
echo PyQt5 DLL 오류가 계속되면 PySide6를 대신 사용할 수 있습니다.
echo PySide6는 PyQt5와 거의 동일하지만 더 나은 호환성을 제공합니다.
echo.

pause

echo.
echo [1/4] PyQt5 제거 중...
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

echo.
echo [2/4] PySide6 설치 중...
pip install PySide6==6.5.2

echo.
echo [3/4] 코드 변환 중...
python convert_to_pyside6.py

echo.
echo [4/4] 테스트 중...
python -c "from PySide6.QtWidgets import QApplication; print('PySide6 설치 성공!')"

echo.
echo ===================================
echo PySide6로 전환 완료!
echo 이제 python main.py 를 실행하세요.
echo ===================================

pause
