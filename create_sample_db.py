"""샘플 데이터베이스 파일 생성 스크립트"""
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    # Excel 파일 생성
    wb = Workbook()
    wb.remove(wb.active)  # 기본 시트 제거

    # ROI 시트
    ws_roi = wb.create_sheet('ROI')
    roi_headers = ['종목코드', '종목명', '초기투자금', '수량', '종가', '평가금', '수익률']
    roi_sample_data = [
        ['069500', 'KODEX 200', 1000000, 50, 20000, 1000000, 0],
        ['114800', 'KODEX 인버스', 500000, 30, 16500, 495000, -1],
        ['123310', 'TIGER 200', 750000, 40, 18750, 750000, 0],
        ['148070', 'KOSEF 국고채10년', 1250000, 60, 20800, 1248000, -0.16]
    ]

    # ROI 헤더
    for col_idx, header in enumerate(roi_headers, 1):
        cell = ws_roi.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')

    # ROI 데이터
    for row_idx, row_data in enumerate(roi_sample_data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws_roi.cell(row=row_idx, column=col_idx, value=value)

    # Balance 시트
    ws_balance = wb.create_sheet('Balance')
    balance_headers = ['연도', '월', '투자원금', '추가납입', '잔고', '수익률', '기타']
    balance_sample_data = [
        ['2024년', '01월', 3500000, 1000000, 3493000, -0.2, ''],
        ['2024년', '11월', 3500000, 0, 3493000, -0.2, '']
    ]

    # Balance 헤더
    for col_idx, header in enumerate(balance_headers, 1):
        cell = ws_balance.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')

    # Balance 데이터
    for row_idx, row_data in enumerate(balance_sample_data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws_balance.cell(row=row_idx, column=col_idx, value=value)

    # Portfolio 시트
    ws_portfolio = wb.create_sheet('Portfolio')
    portfolio_headers = ['종목코드', '종목명', '자산군', '구분', '세팅비중', '현재비중', '빨강매수']
    portfolio_sample_data = [
        ['069500', 'KODEX 200', '국내주식', 'ETF', 25.0, 28.6, -125580],
        ['114800', 'KODEX 인버스', '국내주식', 'ETF', 20.0, 14.2, 202558],
        ['123310', 'TIGER 200', '국내주식', 'ETF', 30.0, 21.5, 296955],
        ['148070', 'KOSEF 국고채10년', '채권', 'ETF', 25.0, 35.7, -373933]
    ]

    # Portfolio 헤더
    for col_idx, header in enumerate(portfolio_headers, 1):
        cell = ws_portfolio.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')

    # Portfolio 데이터
    for row_idx, row_data in enumerate(portfolio_sample_data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws_portfolio.cell(row=row_idx, column=col_idx, value=value)

    # 파일 저장
    wb.save('db/Home_IRP.xlsx')
    print('Sample database file created: db/Home_IRP.xlsx')

except ImportError:
    print('openpyxl is not installed. Please install it first.')
    print('Run: pip install openpyxl')
