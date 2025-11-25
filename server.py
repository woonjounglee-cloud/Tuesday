"""
Tuesday - Portfolio Management Web Server
Python 표준 라이브러리만 사용하는 웹 서버
"""
import http.server
import socketserver
import json
import os
import urllib.parse
import mimetypes
import re
import tempfile
from pathlib import Path
from io import BytesIO

# openpyxl이 있으면 사용, 없으면 CSV 사용
try:
    from openpyxl import load_workbook, Workbook
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("⚠️  openpyxl not found. Using CSV fallback mode.")

PORT = 8000
DB_DIR = Path("db")


def extract_date_from_filename(filename):
    """
    파일명에서 날짜 추출
    예: data_XXXX_YYYYDDMM.xlsx -> {year: YYYY, month: MM}
    """
    # data_XXXX_YYYYDDMM 패턴 찾기
    match = re.search(r'data_\w+_(\d{4})(\d{2})(\d{2})', filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        return {'year': year, 'month': month}
    return None


class TuesdayHandler(http.server.SimpleHTTPRequestHandler):
    """Tuesday HTTP 요청 핸들러"""

    def do_GET(self):
        """GET 요청 처리"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('templates/index.html', 'text/html')
        elif self.path.startswith('/static/'):
            file_path = self.path[1:]  # Remove leading /
            self.serve_file(file_path)
        elif self.path.startswith('/api/data'):
            self.api_get_data()
        elif self.path == '/api/datafiles':
            self.api_list_datafiles()
        elif self.path.startswith('/api/datafile'):
            self.api_get_datafile()
        else:
            self.send_error(404)

    def do_POST(self):
        """POST 요청 처리"""
        if self.path == '/api/save':
            self.api_save_data()
        elif self.path == '/api/upload':
            self.api_upload_file()
        elif self.path == '/api/rebalance':
            self.api_rebalance()
        else:
            self.send_error(404)

    def serve_file(self, file_path, content_type=None):
        """파일 서빙"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            if content_type is None:
                content_type = mimetypes.guess_type(file_path)[0] or 'text/plain'

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def api_get_data(self):
        """데이터 가져오기 API"""
        try:
            # URL 파라미터에서 DB 이름 가져오기
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            db_name = params.get('db', ['Home_IRP'])[0]

            db_path = DB_DIR / f"{db_name}.xlsx"

            data = {
                'roi': [],
                'balance': [],
                'portfolio': []
            }

            if db_path.exists() and HAS_OPENPYXL:
                wb = load_workbook(db_path, data_only=True)

                # ROI 데이터
                if 'ROI' in wb.sheetnames:
                    ws = wb['ROI']
                    # 헤더 읽기
                    headers = [cell for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
                    data['roi'] = [
                        {headers[i]: cell for i, cell in enumerate(row) if i < len(headers)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                        if any(cell is not None for cell in row)
                    ]

                # Balance 데이터
                if 'Balance' in wb.sheetnames:
                    ws = wb['Balance']
                    # 헤더 읽기
                    headers = [cell for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
                    data['balance'] = [
                        {headers[i]: cell for i, cell in enumerate(row) if i < len(headers)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                        if any(cell is not None for cell in row)
                    ]

                # Portfolio 데이터
                if 'Portfolio' in wb.sheetnames:
                    ws = wb['Portfolio']
                    # 헤더 읽기
                    headers = [cell for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
                    data['portfolio'] = [
                        {headers[i]: cell for i, cell in enumerate(row) if i < len(headers)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                        if any(cell is not None for cell in row)
                    ]

            self.send_json_response(data)
        except Exception as e:
            print(f"Error in api_get_data: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def api_save_data(self):
        """데이터 저장 API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            db_name = request_data.get('db', 'Home_IRP')
            data = request_data.get('data', {})

            if HAS_OPENPYXL:
                # Excel 파일로 저장
                wb = Workbook()
                wb.remove(wb.active)

                # ROI 시트
                if 'roi' in data and data['roi']:
                    ws = wb.create_sheet('ROI')
                    headers = list(data['roi'][0].keys())
                    ws.append(headers)
                    for row in data['roi']:
                        ws.append([row.get(h) for h in headers])

                # Balance 시트
                if 'balance' in data and data['balance']:
                    ws = wb.create_sheet('Balance')
                    headers = list(data['balance'][0].keys())
                    ws.append(headers)
                    for row in data['balance']:
                        ws.append([row.get(h) for h in headers])

                # Portfolio 시트
                if 'portfolio' in data and data['portfolio']:
                    ws = wb.create_sheet('Portfolio')
                    headers = list(data['portfolio'][0].keys())
                    ws.append(headers)
                    for row in data['portfolio']:
                        ws.append([row.get(h) for h in headers])

                db_path = DB_DIR / f"{db_name}.xlsx"
                DB_DIR.mkdir(exist_ok=True)
                wb.save(db_path)

            self.send_json_response({'success': True})
        except Exception as e:
            print(f"Error in api_save_data: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def api_upload_file(self):
        """파일 업로드 API"""
        try:
            # multipart/form-data 파싱
            content_type = self.headers['Content-Type']
            if not content_type.startswith('multipart/form-data'):
                self.send_json_response({'error': 'Invalid content type'}, 400)
                return

            # 경계 문자열 추출
            boundary = content_type.split('boundary=')[1].encode()
            content_length = int(self.headers['Content-Length'])

            # 데이터 읽기
            post_data = self.rfile.read(content_length)

            # 파트 분리
            parts = post_data.split(b'--' + boundary)

            file_data = None
            filename = None
            upload_type = None
            db_name = None

            for part in parts:
                if b'Content-Disposition' in part:
                    # 헤더와 본문 분리
                    header_end = part.find(b'\r\n\r\n')
                    if header_end == -1:
                        continue

                    header = part[:header_end].decode('utf-8', errors='ignore')
                    body = part[header_end + 4:]

                    # filename 추출
                    if 'filename=' in header:
                        filename_match = re.search(r'filename="([^"]+)"', header)
                        if filename_match:
                            filename = filename_match.group(1)
                            # 본문에서 마지막 \r\n 제거
                            if body.endswith(b'\r\n'):
                                body = body[:-2]
                            file_data = body

                    # name 필드 추출
                    name_match = re.search(r'name="([^"]+)"', header)
                    if name_match:
                        field_name = name_match.group(1)
                        field_value = body.decode('utf-8', errors='ignore').strip()

                        if field_name == 'type':
                            upload_type = field_value
                        elif field_name == 'db':
                            db_name = field_value

            if not file_data or not filename:
                self.send_json_response({'error': 'No file uploaded'}, 400)
                return

            # 파일명에서 날짜 추출
            date_info = extract_date_from_filename(filename)

            # Excel 파일 처리
            result_data = {'rows': []}

            if HAS_OPENPYXL and (filename.endswith('.xlsx') or filename.endswith('.xls')):
                # 임시 파일로 저장
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    tmp.write(file_data)
                    tmp_path = tmp.name

                try:
                    wb = load_workbook(tmp_path, data_only=True)
                    ws = wb.active

                    # 첫 번째 시트의 데이터 읽기
                    for row in ws.iter_rows(min_row=2, values_only=True):
                        if any(cell is not None for cell in row):
                            result_data['rows'].append(list(row))

                    wb.close()
                finally:
                    os.unlink(tmp_path)

            self.send_json_response({
                'success': True,
                'filename': filename,
                'date': date_info,
                'fileData': result_data
            })

        except Exception as e:
            print(f"Error in api_upload_file: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, 500)

    def api_rebalance(self):
        """리밸런싱 API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            roi_data = data.get('roi', [])
            portfolio_data = data.get('portfolio', [])

            # 총 평가금 계산
            total_eval = sum(float(row.get('평가금', 0) or 0) for row in roi_data)

            # 리밸런싱 계산
            for i, row in enumerate(portfolio_data):
                # ROI에서 해당 종목의 평가금 찾기
                eval_amt = 0
                for roi_row in roi_data:
                    if roi_row.get('종목코드') == row.get('종목코드'):
                        eval_amt = float(roi_row.get('평가금', 0) or 0)
                        break

                # 현재비중 계산
                current_ratio = (eval_amt / total_eval * 100) if total_eval > 0 else 0
                row['현재비중'] = round(current_ratio, 1)

                # 녹색매수 계산
                setting_ratio = float(row.get('세팅비중', 0) or 0)
                rebalancing = (setting_ratio - current_ratio) / 100 * total_eval
                row['녹색매수'] = round(rebalancing, 0)

            self.send_json_response({'portfolio': portfolio_data})
        except Exception as e:
            print(f"Error in api_rebalance: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def api_list_datafiles(self):
        """data_*.xlsx 파일 목록 API"""
        try:
            data_files = []

            # db 디렉토리에서 data_*.xlsx 파일 찾기
            if DB_DIR.exists():
                for file in DB_DIR.glob('data_*.xlsx'):
                    # 파일명에서 날짜 추출 (YYYYMMDD)
                    match = re.search(r'data_\w+_(\d{8})', file.name)
                    if match:
                        date_str = match.group(1)
                        data_files.append({
                            'filename': file.name,
                            'date': date_str
                        })

            # 날짜순으로 정렬 (최신순)
            data_files.sort(key=lambda x: x['date'], reverse=True)

            self.send_json_response({'files': data_files})
        except Exception as e:
            print(f"Error in api_list_datafiles: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def api_get_datafile(self):
        """특정 data_*.xlsx 파일 읽기 API (VLOOKUP용)"""
        try:
            # URL 파라미터에서 파일명 가져오기
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            filename = params.get('filename', [''])[0]

            if not filename:
                self.send_json_response({'error': 'No filename specified'}, 400)
                return

            file_path = DB_DIR / filename

            if not file_path.exists():
                self.send_json_response({'error': 'File not found'}, 404)
                return

            data_rows = []

            if HAS_OPENPYXL and filename.endswith('.xlsx'):
                wb = load_workbook(file_path, data_only=True)
                ws = wb.active

                # 데이터 읽기 (A열: 종목코드, C열: 종가)
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if row[0]:  # 종목코드가 있으면
                        data_rows.append({
                            '종목코드': str(row[0]),
                            '종목명': row[1] if len(row) > 1 else '',
                            '종가': row[2] if len(row) > 2 else 0
                        })

                wb.close()

            self.send_json_response({'data': data_rows})
        except Exception as e:
            print(f"Error in api_get_datafile: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def send_json_response(self, data, status=200):
        """JSON 응답 전송"""
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-length', len(response))
        self.end_headers()
        self.wfile.write(response)


def main():
    """서버 시작"""
    print("=" * 60)
    print("📊 Tuesday - Portfolio Management Web Server")
    print("=" * 60)
    print(f"\n🌐 Server running at: http://localhost:{PORT}")
    print(f"📁 Database directory: {DB_DIR}")
    print(f"📦 openpyxl: {'✓ Available' if HAS_OPENPYXL else '✗ Not found (using CSV)'}")
    print("\n💡 Open your browser and go to:")
    print(f"   http://localhost:{PORT}")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # DB 디렉토리 생성
    DB_DIR.mkdir(exist_ok=True)

    with socketserver.TCPServer(("", PORT), TuesdayHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")


if __name__ == "__main__":
    main()
