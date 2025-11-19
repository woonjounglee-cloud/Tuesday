# Tuesday - Portfolio Management Web App

**Python 표준 라이브러리만 사용하는 웹 기반 포트폴리오 관리 시스템**

투자 포트폴리오를 관리하는 웹 애플리케이션입니다. **추가 패키지 설치 없이** Python만 있으면 실행됩니다!

## ✨ 특징

- 🚀 **Python 표준 라이브러리만 사용** - 설치 문제 없음!
- 🌐 **브라우저 기반** - 어디서든 접속 가능
- 💾 **Excel 파일 지원** - openpyxl 사용 (선택사항)
- 📊 **실시간 계산** - ROI, Balance, Portfolio 자동 계산
- 📱 **반응형 디자인** - 모바일/태블릿 지원

## 🚀 빠른 시작

### 1. 서버 실행

**Windows:**
```bash
run.bat
```

**또는 명령줄:**
```bash
python server.py
```

### 2. 브라우저 접속

```
http://localhost:8000
```

자동으로 브라우저가 열리지 않으면 위 주소를 직접 입력하세요.

## 📋 기능

### 📈 ROI (수익률)
- 종목별 투자 정보 관리
- 평가금 및 수익률 자동 계산
- 실시간 편집 가능

### 💰 Balance (잔고)
- 월별 투자 현황 추적
- 투자원금, 추가납입, 잔고 관리

### 🎯 Portfolio (포트폴리오)
- 자산 배분 설정
- 리밸런싱 자동 계산
- 현재 비중 vs 목표 비중 비교

## 📁 프로젝트 구조

```
Tuesday/
├── server.py              # Python 웹 서버 (표준 라이브러리)
├── templates/
│   └── index.html        # 메인 HTML
├── static/
│   ├── style.css         # CSS 스타일
│   └── app.js            # JavaScript 로직
├── src/utils/            # 유틸리티
│   ├── excel_handler.py
│   └── calculations.py
├── db/                   # 데이터베이스
│   └── Home_IRP.xlsx
├── run.bat               # 실행 스크립트
└── requirements.txt      # openpyxl (선택사항)
```

## 🛠️ 기술 스택

- **백엔드**: Python `http.server` (표준 라이브러리)
- **프론트엔드**: HTML5, CSS3, JavaScript (Vanilla)
- **데이터**: Excel (openpyxl) 또는 JSON

## 💡 사용 방법

1. **데이터 편집**: 테이블에서 직접 값 입력
2. **행 추가/삭제**: 버튼 클릭
3. **저장**: 💾 저장 버튼 클릭
4. **리밸런싱**: Portfolio 탭에서 🔄 Rebalancing 버튼 클릭

## 📦 선택적 의존성

Excel 파일 지원을 위해 openpyxl을 설치할 수 있습니다 (선택사항):

```bash
pip install openpyxl
```

**openpyxl이 없어도 작동합니다!** (JSON 형식으로 저장됨)

## 🔧 문제 해결

### 포트가 이미 사용 중일 때

`server.py` 파일을 열고 `PORT = 8000`을 다른 포트로 변경:

```python
PORT = 8001  # 또는 다른 사용 가능한 포트
```

### 방화벽 문제

회사 방화벽으로 인한 패키지 설치 불가 시:
- **해결책**: 이미 해결됨! 추가 설치 불필요!
- Python 표준 라이브러리만 사용하므로 방화벽 문제 없음

## 🌟 장점

✅ **추가 설치 불필요** - Python만 있으면 OK  
✅ **방화벽 문제 없음** - PyPI 접속 불필요  
✅ **Python 버전 무관** - 3.6+ 모두 지원  
✅ **브라우저에서 실행** - 크로스 플랫폼  
✅ **간단한 구조** - 이해하기 쉬움

## 📝 라이선스

개인 사용 목적으로 제작되었습니다.
