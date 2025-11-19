# Tuesday - Portfolio Management Web App

투자 포트폴리오를 관리하는 웹 기반 애플리케이션입니다. ETF, 주식 등의 투자 자산을 추적하고 리밸런싱을 지원합니다.

## 🌟 주요 기능

### Home - IRP 탭

#### 📈 ROI (수익률)
- 종목별 투자 정보 관리
- ETF/주식 파일 업로드로 자동 데이터 업데이트
- 평가금 및 수익률 자동 계산
- 실시간 편집 가능한 데이터 테이블
- 투자 요약 통계 (총 투자원금, 평가금, 수익금, 수익률)

#### 💰 Balance (잔고)
- 월별 투자 현황 추적
- 투자원금, 추가납입, 잔고 관리
- 인터랙티브 잔고 추이 그래프

#### 🎯 Portfolio (포트폴리오)
- 자산 배분 설정 및 관리
- 리밸런싱 계산 기능
- 현재 비중 vs 목표 비중 비교
- 매수/매도 필요 금액 자동 계산

## 🚀 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 웹 서버 실행

**Windows:**
```bash
run.bat
```

**또는 명령줄:**
```bash
streamlit run app.py
```

### 3. 브라우저 접속

자동으로 브라우저가 열립니다. 또는 직접 접속:
```
http://localhost:8501
```

## 📁 프로젝트 구조

```
Tuesday/
├── app.py                 # 메인 Streamlit 앱
├── pages/                 # 페이지 모듈
│   └── irp_page.py       # IRP 탭
├── src/utils/            # 유틸리티
│   ├── excel_handler.py  # Excel 처리
│   └── calculations.py   # 계산 로직
├── db/                   # 데이터베이스
│   └── Home_IRP.xlsx     # IRP 데이터
├── requirements.txt      # 의존성
└── run.bat              # 실행 스크립트
```

## 🛠️ 기술 스택

- **Streamlit**: 웹 프레임워크
- **pandas**: 데이터 처리
- **openpyxl**: Excel 파일
- **plotly**: 인터랙티브 차트

## 📝 사용 방법

1. **파일 업로드**: 상단 버튼으로 ETF/주식 파일 업로드
2. **데이터 편집**: 테이블에서 직접 수정
3. **리밸런싱**: Portfolio 탭에서 실행

브라우저에서 실행되므로 방화벽 문제가 없습니다!
