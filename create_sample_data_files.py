"""
샘플 data_*.xlsx 파일 생성 스크립트
"""
from openpyxl import Workbook
from pathlib import Path

# DB 디렉토리 생성
db_dir = Path("db")
db_dir.mkdir(exist_ok=True)

# 샘플 데이터 (종목코드, 종목명, 종가)
sample_data = [
    ("069500", "KODEX 200", 32500),
    ("114800", "KODEX 인버스", 4800),
    ("148070", "KOSEF 국고채10년", 102350),
    ("A069500", "TIGER 200", 32450),
    ("360750", "TIGER 미국S&P500", 18500),
]

# 3개의 샘플 DB 파일 생성
dates = [
    ("data_TEST_20241101.xlsx", "2024년 11월 1일"),
    ("data_TEST_20241201.xlsx", "2024년 12월 1일"),
    ("data_TEST_20250101.xlsx", "2025년 1월 1일"),
]

for filename, desc in dates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    # 헤더
    ws.append(["종목코드", "종목명", "종가"])

    # 데이터 추가
    for code, name, price in sample_data:
        ws.append([code, name, price])

    filepath = db_dir / filename
    wb.save(filepath)
    print(f"✓ Created: {filepath} ({desc})")

print("\n✅ Sample data files created successfully!")
