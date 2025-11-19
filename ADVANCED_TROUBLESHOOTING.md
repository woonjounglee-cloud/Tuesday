# 고급 문제 해결 가이드

PyQt5 DLL 오류가 계속 발생하는 경우 이 가이드를 따라주세요.

## 진단 먼저 하기

```bash
python diagnose.py
```

이 스크립트가 다음을 확인합니다:
- Python 버전 및 아키텍처
- PyQt5 설치 상태
- 시스템 정보

## 해결 방법 (우선순위 순)

### 방법 1: PySide6로 전환 ⭐ (가장 권장)

PySide6는 PyQt5와 거의 동일하지만 더 나은 Windows 호환성을 제공합니다.

```bash
# 자동 전환 스크립트 실행
switch_to_pyside6.bat
```

또는 수동으로:
```bash
# 1. PyQt5 제거
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip -y

# 2. PySide6 설치
pip install PySide6==6.5.2

# 3. 코드 변환
python convert_to_pyside6.py

# 4. 실행
python main.py
```

### 방법 2: Python 버전 확인 및 변경

Python 3.11 이상에서 PyQt5 DLL 문제가 자주 발생합니다.

**현재 버전 확인:**
```bash
python --version
```

**Python 3.10으로 다운그레이드 권장:**

1. Python 3.10.11 다운로드:
   - https://www.python.org/downloads/release/python-31011/
   - "Windows installer (64-bit)" 선택

2. 설치 시 "Add Python to PATH" 체크

3. 새 가상환경 생성:
```bash
# 기존 venv 삭제
rmdir /s venv

# Python 3.10으로 새 가상환경
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 방법 3: Anaconda 사용

Anaconda는 사전 컴파일된 바이너리를 제공하여 DLL 문제를 피할 수 있습니다.

1. **Anaconda 설치:**
   - https://www.anaconda.com/download

2. **Anaconda Prompt 열기**

3. **환경 생성:**
```bash
conda create -n tuesday python=3.10
conda activate tuesday
```

4. **패키지 설치:**
```bash
conda install pyqt=5.15.9
pip install openpyxl matplotlib pyinstaller
```

5. **실행:**
```bash
python main.py
```

6. **PyCharm에서 Anaconda 환경 사용:**
   - File → Settings → Project: Tuesday → Python Interpreter
   - Add Interpreter → Conda Environment
   - Existing environment: `C:\Users\[username]\anaconda3\envs\tuesday\python.exe`

### 방법 4: 32-bit vs 64-bit 확인

**진단:**
```bash
python diagnose.py
```

출력에서 "32bit" 또는 "64bit" 확인

**64-bit Python이 아니면:**
1. 64-bit Python 3.10 설치
2. 새 가상환경 생성
3. 패키지 재설치

### 방법 5: 시스템 DLL 복구

관리자 권한으로 PowerShell 실행:
```powershell
# Windows DLL 복구
sfc /scannow

# .NET Framework 복구
DISM /Online /Cleanup-Image /RestoreHealth
```

### 방법 6: PyQt5 특정 버전 시도

```bash
# 다른 버전들 시도
pip install PyQt5==5.15.7
# 또는
pip install PyQt5==5.15.6
# 또는
pip install PyQt5==5.15.4
```

### 방법 7: PATH 환경 변수 확인

1. **시작 → "환경 변수" 검색**

2. **시스템 변수에서 Path 확인:**
   - Python 설치 경로가 있는지 확인
   - 예: `C:\Python310\`, `C:\Python310\Scripts\`

3. **중복된 Python 경로 제거**

4. **컴퓨터 재부팅**

### 방법 8: 완전 초기화

```bash
# 1. 모든 Python 패키지 제거
pip freeze > uninstall.txt
pip uninstall -r uninstall.txt -y

# 2. pip 캐시 삭제
pip cache purge

# 3. 가상환경 삭제
rmdir /s venv

# 4. 새로 시작
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 대안: Tkinter 버전 (임시)

PyQt5가 정말 안 되면 Tkinter 기반의 간단한 버전을 사용할 수 있습니다:

```bash
python main_tkinter.py
```

(별도로 제공 예정)

## 여전히 안 되면

다음 정보를 함께 공유해주세요:

1. **Python 버전:**
```bash
python --version
```

2. **진단 결과:**
```bash
python diagnose.py
```

3. **pip list 출력:**
```bash
pip list
```

4. **전체 오류 메시지:**
```bash
python main.py 2>&1 > error.txt
```

5. **Visual C++ Redistributable 설치 여부:**
   - 제어판 → 프로그램 및 기능
   - "Microsoft Visual C++ 2015-2022 Redistributable" 확인

## 빠른 해결 체크리스트

- [ ] `python diagnose.py` 실행
- [ ] Python 버전 3.8-3.10 확인
- [ ] 64-bit Python 확인
- [ ] Visual C++ Redistributable 설치
- [ ] `fix_pyqt5.bat` 실행
- [ ] `switch_to_pyside6.bat` 실행 (PySide6로 전환)
- [ ] Anaconda 환경 시도
- [ ] 가상환경 재생성
- [ ] 컴퓨터 재부팅

## PySide6 vs PyQt5

| 항목 | PyQt5 | PySide6 |
|------|-------|---------|
| 라이선스 | GPL | LGPL (더 자유로움) |
| 안정성 | 높음 | 높음 |
| Windows 호환성 | 보통 | **매우 높음** |
| API | Qt5 기반 | Qt6 기반 |
| 성능 | 우수 | 우수 |

**결론: PySide6 사용을 강력히 권장합니다!**
