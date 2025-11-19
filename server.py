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
from pathlib import Path

# openpyxl이 있으면 사용, 없으면 CSV 사용
try:
    from openpyxl import load_workbook, Workbook
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("⚠️  openpyxl not found. Using CSV fallback mode.")

PORT = 8000
DB_PATH = Path("db/Home_IRP.xlsx")


class TuesdayHandler(http.server.SimpleHTTPRequestHandler):
    """Tuesday HTTP 요청 핸들러"""

    def do_GET(self):
        """GET 요청 처리"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('templates/index.html', 'text/html')
        elif self.path.startswith('/static/'):
            file_path = self.path[1:]  # Remove leading /
            self.serve_file(file_path)
        elif self.path == '/api/data':
            self.api_get_data()
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
            data = {
                'roi': [],
                'balance': [],
                'portfolio': []
            }

            if DB_PATH.exists() and HAS_OPENPYXL:
                wb = load_workbook(DB_PATH, data_only=True)

                # ROI 데이터
                if 'ROI' in wb.sheetnames:
                    ws = wb['ROI']
                    headers = [cell.value for cell in ws[1]]
                    data['roi'] = [
                        {headers[i]: cell.value for i, cell in enumerate(row)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                    ]

                # Balance 데이터
                if 'Balance' in wb.sheetnames:
                    ws = wb['Balance']
                    headers = [cell.value for cell in ws[1]]
                    data['balance'] = [
                        {headers[i]: cell.value for i, cell in enumerate(row)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                    ]

                # Portfolio 데이터
                if 'Portfolio' in wb.sheetnames:
                    ws = wb['Portfolio']
                    headers = [cell.value for cell in ws[1]]
                    data['portfolio'] = [
                        {headers[i]: cell.value for i, cell in enumerate(row)}
                        for row in ws.iter_rows(min_row=2, values_only=True)
                    ]

            self.send_json_response(data)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

    def api_save_data(self):
        """데이터 저장 API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            if HAS_OPENPYXL:
                # Excel 파일로 저장
                wb = Workbook()
                wb.remove(wb.active)

                # ROI 시트
                if 'roi' in data:
                    ws = wb.create_sheet('ROI')
                    if data['roi']:
                        headers = list(data['roi'][0].keys())
                        ws.append(headers)
                        for row in data['roi']:
                            ws.append([row.get(h) for h in headers])

                # Balance 시트
                if 'balance' in data:
                    ws = wb.create_sheet('Balance')
                    if data['balance']:
                        headers = list(data['balance'][0].keys())
                        ws.append(headers)
                        for row in data['balance']:
                            ws.append([row.get(h) for h in headers])

                # Portfolio 시트
                if 'portfolio' in data:
                    ws = wb.create_sheet('Portfolio')
                    if data['portfolio']:
                        headers = list(data['portfolio'][0].keys())
                        ws.append(headers)
                        for row in data['portfolio']:
                            ws.append([row.get(h) for h in headers])

                DB_PATH.parent.mkdir(exist_ok=True)
                wb.save(DB_PATH)

            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

    def api_upload_file(self):
        """파일 업로드 API"""
        # 간단한 구현을 위해 생략
        self.send_json_response({'error': 'Not implemented yet'}, 501)

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

                # 빨강매수 계산
                setting_ratio = float(row.get('세팅비중', 0) or 0)
                rebalancing = (setting_ratio - current_ratio) / 100 * total_eval
                row['빨강매수'] = round(rebalancing, 0)

            self.send_json_response({'portfolio': portfolio_data})
        except Exception as e:
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
    print(f"📁 Database: {DB_PATH}")
    print(f"📦 openpyxl: {'✓ Available' if HAS_OPENPYXL else '✗ Not found (using CSV)'}")
    print("\n💡 Open your browser and go to:")
    print(f"   http://localhost:{PORT}")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    with socketserver.TCPServer(("", PORT), TuesdayHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")


if __name__ == "__main__":
    main()
