# Tuesday - Excel 문서 관리 프로그램

Tuesday는 투자 포트폴리오를 관리하는 데스크톱 애플리케이션입니다. ETF, 주식 등의 투자 자산을 추적하고 리밸런싱을 지원합니다.

## 주요 기능

### Home - IRP 탭

#### ROI (수익률) 섹션
- 종목별 투자 정보 관리
- ETF 파일 업로드로 자동 데이터 업데이트
- 평가금 및 수익률 자동 계산
- 마이너스 수익률 빨간색 강조 표시

#### Balance (잔고) 섹션
- 월별 투자 현황 추적
- 투자원금, 입금, 잔고 관리
- 잔고 추이 그래프 표시

#### Portfolio (포트폴리오) 섹션
- 자산 배분 설정 및 관리
- 리밸런싱 계산 기능
- 현재 비중 vs 목표 비중 비교
- 매수/매도 필요 금액 계산

## 시스템 요구사항

- Windows x64 PC
- Python 3.8 이상 (개발용)

## 설치 및 실행

### 방법 1: 실행 파일 사용 (.exe)

1. `dist/Tuesday.exe` 파일을 실행합니다.
2. 별도의 설치나 Python 환경이 필요 없습니다.

### 방법 2: 소스 코드에서 실행 (Windows - 권장)

#### 빠른 설치 (자동 스크립트)
```bash
# 1. setup_venv.bat 실행 - 가상환경 생성 및 의존성 설치
setup_venv.bat

# 2. 가상환경 활성화
venv\Scripts\activate

# 3. 프로그램 실행
python main.py
```

#### 수동 설치
1. **저장소를 클론합니다:**
```bash
git clone <repository-url>
cd Tuesday
```

2. **Python 3.8 이상 설치 확인:**
```bash
python --version
```

3. **가상환경을 생성합니다 (권장):**
```bash
python -m venv venv
venv\Scripts\activate
```

4. **pip 업그레이드:**
```bash
python -m pip install --upgrade pip
```

5. **의존성을 설치합니다:**
```bash
pip install -r requirements.txt
```

6. **PyQt5 오류 시 해결:**
```bash
# PyQt5 DLL 오류가 발생하면
fix_pyqt5.bat
```

7. **샘플 데이터베이스를 생성합니다:**
```bash
python create_sample_db.py
```

8. **프로그램을 실행합니다:**
```bash
python main.py
```

### 방법 3: Linux/Mac에서 실행

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 샘플 DB 생성
python create_sample_db.py

# 실행
python main.py
```

## 빌드 방법

Windows에서 .exe 파일을 빌드하려면:

```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh
./build.sh
```

빌드된 실행 파일은 `dist/Tuesday.exe`에 생성됩니다.

## 사용 방법

### ETF 파일 업로드

1. **파일 형식**: `data_XXXX_YYYYDDMM.xlsx` 또는 `.csv`
   - YYYY: 연도 (예: 2024)
   - DD: 일 (예: 15)
   - MM: 월 (예: 03)

2. **파일 구조**:
   - A열: 종목코드
   - B열: 종목명
   - C열: 종가

3. **업로드 방법**:
   - 상단의 'ETF' 버튼 클릭
   - 파일 선택
   - 자동으로 데이터가 업데이트됩니다

### 데이터 관리

- **행 추가**: 각 섹션 하단의 "행 추가" 버튼 클릭
- **행 삭제**: 삭제할 행 선택 후 "행 삭제" 버튼 클릭
- **데이터 수정**: 테이블 셀을 직접 클릭하여 수정
- **자동 저장**: 데이터 변경 시 자동으로 저장됩니다

### 리밸런싱

1. Portfolio 섹션에서 각 종목의 "세팅비중" 입력 (합계 100%)
2. "Rebalancing" 버튼 클릭
3. 현재비중과 빨강매수 금액이 자동 계산됩니다
   - 빨간색 숫자: 매수 필요
   - 괄호 안 숫자: 매도 필요

## 프로젝트 구조

```
Tuesday/
├── main.py                 # 메인 실행 파일
├── requirements.txt        # Python 의존성
├── Tuesday.spec           # PyInstaller 설정
├── build.bat              # Windows 빌드 스크립트
├── build.sh               # Linux/Mac 빌드 스크립트
├── create_sample_db.py    # 샘플 DB 생성 스크립트
├── db/                    # 데이터베이스 폴더
│   └── Home_IRP.xlsx      # IRP 데이터베이스
├── src/
│   ├── ui/                # UI 모듈
│   │   ├── main_window.py # 메인 윈도우
│   │   └── irp_tab.py     # IRP 탭
│   └── utils/             # 유틸리티 모듈
│       ├── excel_handler.py  # Excel 처리
│       └── calculations.py   # 계산 로직
└── dist/                  # 빌드된 실행 파일 (빌드 후 생성)
    └── Tuesday.exe
```

## 기술 스택

- **GUI Framework**: PyQt5
- **데이터 처리**: openpyxl, pandas
- **차트**: matplotlib
- **패키징**: PyInstaller

## 개발 계획

- [x] Home - IRP 탭
- [ ] WJ - ISA 탭
- [ ] WJ - 주식 탭
- [ ] MG - IRP 탭
- [ ] MG - 개인연금 탭
- [ ] 주식 파일 업로드 기능
- [ ] 데이터 백업/복원 기능
- [ ] 다크 모드 지원

## 라이선스

이 프로젝트는 개인 사용을 위해 제작되었습니다.

## 문의

버그 리포트나 기능 요청은 Issues를 통해 제출해주세요.
