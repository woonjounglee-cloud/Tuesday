"""
Tuesday 환경 진단 스크립트
PyQt5 DLL 오류 원인 파악
"""
import sys
import platform

print("=" * 50)
print("Tuesday 환경 진단")
print("=" * 50)

# Python 버전 확인
print(f"\n1. Python 버전: {sys.version}")
print(f"   Python 실행 파일: {sys.executable}")
print(f"   Python 아키텍처: {platform.architecture()}")

# 시스템 정보
print(f"\n2. 시스템 정보:")
print(f"   OS: {platform.system()} {platform.release()}")
print(f"   프로세서: {platform.processor()}")

# 설치된 패키지 확인
print(f"\n3. 패키지 확인:")
try:
    import PyQt5
    print(f"   PyQt5 버전: {PyQt5.QtCore.PYQT_VERSION_STR}")
    print(f"   PyQt5 경로: {PyQt5.__file__}")
    print(f"   Qt 버전: {PyQt5.QtCore.QT_VERSION_STR}")
except Exception as e:
    print(f"   PyQt5 가져오기 실패: {e}")

try:
    import openpyxl
    print(f"   openpyxl 버전: {openpyxl.__version__}")
except:
    print(f"   openpyxl 미설치")

try:
    import matplotlib
    print(f"   matplotlib 버전: {matplotlib.__version__}")
except:
    print(f"   matplotlib 미설치")

# PATH 확인
print(f"\n4. Python PATH:")
for path in sys.path[:5]:
    print(f"   {path}")

print("\n" + "=" * 50)
print("진단 완료")
print("=" * 50)
print("\n다음 단계:")
print("1. Python 버전이 3.11 이상이면 3.10 이하로 다운그레이드 권장")
print("2. 아키텍처가 32-bit이면 64-bit Python 설치 권장")
print("3. PyQt5 대신 PySide6 사용 고려")
print("=" * 50)
