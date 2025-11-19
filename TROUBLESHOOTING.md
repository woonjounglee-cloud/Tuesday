# Tuesday 문제 해결 가이드

## PyQt5 DLL 로드 오류 (Windows)

### 오류 메시지
```
ImportError: DLL load failed while importing QtWidgets: 지정된 모듈을 찾을 수 없습니다.
```

### 해결 방법

#### 방법 1: PyQt5 재설치 (가장 권장)

1. **기존 PyQt5 제거**
```bash
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip
```

2. **최신 버전 설치**
```bash
pip install PyQt5==5.15.9
```

#### 방법 2: Visual C++ Redistributable 설치

PyQt5는 Microsoft Visual C++ Redistributable이 필요합니다.

1. 다음 링크에서 다운로드:
   - [Visual C++ Redistributable 2015-2022 (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

2. 설치 후 컴퓨터 재부팅

3. PyCharm에서 다시 실행

#### 방법 3: 가상환경 사용

1. **새 가상환경 생성**
```bash
# PyCharm 터미널에서
python -m venv venv
```

2. **가상환경 활성화**
```bash
# Windows
venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **PyCharm 인터프리터 설정**
   - File → Settings → Project: Tuesday → Python Interpreter
   - 톱니바퀴 아이콘 → Add
   - Existing environment 선택
   - `venv\Scripts\python.exe` 경로 지정

#### 방법 4: PyQt5-Qt5 수동 설치

```bash
pip uninstall PyQt5
pip install PyQt5-Qt5
pip install PyQt5
```

#### 방법 5: 호환성 있는 버전 설치

```bash
pip uninstall PyQt5
pip install PyQt5==5.15.7
```

### 확인 방법

설치 후 Python에서 테스트:
```python
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 정상 작동')"
```

## 기타 문제

### openpyxl 오류
```bash
pip install openpyxl
```

### matplotlib 오류
```bash
pip install matplotlib
```

### pandas 오류 (선택사항)
```bash
pip install pandas
```

## PyCharm 설정 확인

1. **Python 인터프리터 확인**
   - File → Settings → Project: Tuesday → Python Interpreter
   - Python 3.8 이상인지 확인

2. **패키지 설치 확인**
   - Python Interpreter 창에서 설치된 패키지 목록 확인
   - PyQt5, openpyxl, matplotlib가 모두 설치되어 있는지 확인

3. **작업 디렉토리 확인**
   - Run → Edit Configurations
   - Working directory가 프로젝트 루트 디렉토리인지 확인

## 추가 도움

문제가 계속되면 다음 정보를 확인해주세요:

1. Python 버전
```bash
python --version
```

2. PyQt5 버전
```bash
pip show PyQt5
```

3. 설치된 패키지 목록
```bash
pip list
```
