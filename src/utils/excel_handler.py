"""Excel 파일 처리 유틸리티"""
import os
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment


class ExcelHandler:
    """Excel 파일 읽기/쓰기 처리 클래스"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = None

    def load(self):
        """Excel 파일 로드"""
        if os.path.exists(self.file_path):
            self.workbook = load_workbook(self.file_path)
        else:
            self.workbook = Workbook()
        return self.workbook

    def save(self):
        """Excel 파일 저장"""
        if self.workbook:
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self.workbook.save(self.file_path)

    def get_sheet(self, sheet_name):
        """시트 가져오기"""
        if not self.workbook:
            self.load()

        if sheet_name in self.workbook.sheetnames:
            return self.workbook[sheet_name]
        else:
            return self.workbook.create_sheet(sheet_name)

    def read_sheet_data(self, sheet_name):
        """시트 데이터 읽기 (헤더 포함)"""
        sheet = self.get_sheet(sheet_name)
        data = []

        for row in sheet.iter_rows(values_only=True):
            data.append(list(row))

        return data

    def write_sheet_data(self, sheet_name, data, headers=None):
        """시트 데이터 쓰기"""
        sheet = self.get_sheet(sheet_name)

        # 기존 데이터 삭제
        sheet.delete_rows(1, sheet.max_row)

        # 헤더 작성
        if headers:
            for col_idx, header in enumerate(headers, 1):
                cell = sheet.cell(row=1, column=col_idx, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                cell.alignment = Alignment(horizontal='center')

        # 데이터 작성
        start_row = 2 if headers else 1
        for row_idx, row_data in enumerate(data, start_row):
            for col_idx, value in enumerate(row_data, 1):
                sheet.cell(row=row_idx, column=col_idx, value=value)

    @staticmethod
    def read_uploaded_file(file_path):
        """업로드된 파일 읽기 (csv 또는 xlsx)"""
        if file_path.endswith('.csv'):
            # CSV 파일 처리
            import csv
            data = {}
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows:
                    # A열: 종목코드, B열: 종목명, C열: 종가
                    for row in rows[1:]:  # 헤더 제외
                        if len(row) >= 3:
                            code = row[0].strip()
                            name = row[1].strip()
                            price = row[2].strip()
                            data[code] = {'종목명': name, '종가': price}
            return data
        elif file_path.endswith('.xlsx'):
            # Excel 파일 처리
            wb = load_workbook(file_path, data_only=True)
            ws = wb.active
            data = {}

            for row in ws.iter_rows(min_row=2, values_only=True):  # 헤더 제외
                if row and len(row) >= 3:
                    code = str(row[0]).strip() if row[0] else ''
                    name = str(row[1]).strip() if row[1] else ''
                    price = row[2] if row[2] else 0

                    if code:
                        data[code] = {'종목명': name, '종가': price}

            return data
        else:
            raise ValueError("지원하지 않는 파일 형식입니다.")

    @staticmethod
    def extract_date_from_filename(filename):
        """파일명에서 날짜 추출 (data_XXXX_YYYYDDMM.xlsx)"""
        import re
        # 파일명에서 확장자 제거
        basename = os.path.basename(filename)
        name_without_ext = os.path.splitext(basename)[0]

        # 패턴: data_XXXX_YYYYDDMM
        pattern = r'data_\w+_(\d{4})(\d{2})(\d{2})'
        match = re.search(pattern, name_without_ext)

        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            return f"{year}년", f"{month}월"

        return None, None
