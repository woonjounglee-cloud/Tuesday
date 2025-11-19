"""IRP 탭 UI"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
                             QMessageBox, QHeaderView, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..utils.excel_handler import ExcelHandler
from ..utils.calculations import Calculator


class IRPTab(QWidget):
    """IRP 탭 위젯"""

    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.excel_handler = ExcelHandler(db_path)
        self.calculator = Calculator()

        # 데이터 초기화
        self.roi_data = []
        self.balance_data = []
        self.portfolio_data = []

        self.init_ui()
        self.load_data()

    def init_ui(self):
        """UI 초기화"""
        main_layout = QVBoxLayout()

        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.addWidget(QLabel("Tuesday", font=QFont("Arial", 16, QFont.Bold)))
        button_layout.addStretch()

        self.etf_button = QPushButton("ETF")
        self.etf_button.clicked.connect(self.upload_etf_file)
        button_layout.addWidget(self.etf_button)

        self.stock_button = QPushButton("주식")
        self.stock_button.clicked.connect(self.upload_stock_file)
        button_layout.addWidget(self.stock_button)

        main_layout.addLayout(button_layout)

        # ROI 섹션
        roi_group = self.create_roi_section()
        main_layout.addWidget(roi_group)

        # Balance 섹션 및 그래프
        balance_splitter = QSplitter(Qt.Horizontal)
        balance_group = self.create_balance_section()
        balance_splitter.addWidget(balance_group)

        # 그래프
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        balance_splitter.addWidget(self.canvas)
        balance_splitter.setSizes([600, 400])

        main_layout.addWidget(balance_splitter)

        # Portfolio 섹션
        portfolio_group = self.create_portfolio_section()
        main_layout.addWidget(portfolio_group)

        self.setLayout(main_layout)

    def create_roi_section(self):
        """ROI 섹션 생성"""
        group = QGroupBox("ROI")
        layout = QVBoxLayout()

        # 테이블
        self.roi_table = QTableWidget()
        self.roi_table.setColumnCount(7)
        self.roi_table.setHorizontalHeaderLabels([
            '종목코드', '종목명', '초기투자금', '수량', '종가', '평가금', '수익률'
        ])
        self.roi_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.roi_table.cellChanged.connect(self.on_roi_cell_changed)

        layout.addWidget(self.roi_table)

        # 행 추가/삭제 버튼
        btn_layout = QHBoxLayout()
        add_row_btn = QPushButton("행 추가")
        add_row_btn.clicked.connect(lambda: self.add_row(self.roi_table))
        btn_layout.addWidget(add_row_btn)

        del_row_btn = QPushButton("행 삭제")
        del_row_btn.clicked.connect(lambda: self.delete_row(self.roi_table))
        btn_layout.addWidget(del_row_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        group.setLayout(layout)

        return group

    def create_balance_section(self):
        """Balance 섹션 생성"""
        group = QGroupBox("Balance")
        layout = QVBoxLayout()

        # 테이블
        self.balance_table = QTableWidget()
        self.balance_table.setColumnCount(7)
        self.balance_table.setHorizontalHeaderLabels([
            '연도', '월', '투자원금', '추가납입', '잔고', '수익률', '기타'
        ])
        self.balance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 기타 칸을 4배 크게
        self.balance_table.setColumnWidth(6, self.balance_table.columnWidth(6) * 4)
        self.balance_table.cellChanged.connect(self.on_balance_cell_changed)

        layout.addWidget(self.balance_table)

        # 행 추가/삭제 버튼
        btn_layout = QHBoxLayout()
        add_row_btn = QPushButton("행 추가")
        add_row_btn.clicked.connect(lambda: self.add_row(self.balance_table))
        btn_layout.addWidget(add_row_btn)

        del_row_btn = QPushButton("행 삭제")
        del_row_btn.clicked.connect(lambda: self.delete_row(self.balance_table))
        btn_layout.addWidget(del_row_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        group.setLayout(layout)

        return group

    def create_portfolio_section(self):
        """Portfolio 섹션 생성"""
        group = QGroupBox("Portfolio")
        layout = QVBoxLayout()

        # Rebalancing 버튼
        rebalancing_btn = QPushButton("Rebalancing")
        rebalancing_btn.clicked.connect(self.rebalance_portfolio)
        layout.addWidget(rebalancing_btn)

        # 테이블
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(7)
        self.portfolio_table.setHorizontalHeaderLabels([
            '종목코드', '종목명', '자산군', '구분', '세팅비중', '현재비중', '빨강매수'
        ])
        self.portfolio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.portfolio_table.cellChanged.connect(self.on_portfolio_cell_changed)

        layout.addWidget(self.portfolio_table)

        # 행 추가/삭제 버튼
        btn_layout = QHBoxLayout()
        add_row_btn = QPushButton("행 추가")
        add_row_btn.clicked.connect(lambda: self.add_row(self.portfolio_table))
        btn_layout.addWidget(add_row_btn)

        del_row_btn = QPushButton("행 삭제")
        del_row_btn.clicked.connect(lambda: self.delete_row(self.portfolio_table))
        btn_layout.addWidget(del_row_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        group.setLayout(layout)

        return group

    def load_data(self):
        """데이터베이스에서 데이터 로드"""
        try:
            self.excel_handler.load()

            # ROI 데이터 로드
            roi_data = self.excel_handler.read_sheet_data('ROI')
            if roi_data and len(roi_data) > 1:
                self.populate_table(self.roi_table, roi_data[1:])  # 헤더 제외

            # Balance 데이터 로드
            balance_data = self.excel_handler.read_sheet_data('Balance')
            if balance_data and len(balance_data) > 1:
                self.populate_table(self.balance_table, balance_data[1:])  # 헤더 제외

            # Portfolio 데이터 로드
            portfolio_data = self.excel_handler.read_sheet_data('Portfolio')
            if portfolio_data and len(portfolio_data) > 1:
                self.populate_table(self.portfolio_table, portfolio_data[1:])  # 헤더 제외

            # 계산 수행
            self.recalculate_roi()
            self.recalculate_balance()
            self.update_balance_chart()

        except Exception as e:
            QMessageBox.warning(self, "오류", f"데이터 로드 실패: {str(e)}")

    def save_data(self):
        """데이터베이스에 데이터 저장"""
        try:
            # ROI 데이터 저장
            roi_data = self.get_table_data(self.roi_table)
            roi_headers = ['종목코드', '종목명', '초기투자금', '수량', '종가', '평가금', '수익률']
            self.excel_handler.write_sheet_data('ROI', roi_data, roi_headers)

            # Balance 데이터 저장
            balance_data = self.get_table_data(self.balance_table)
            balance_headers = ['연도', '월', '투자원금', '추가납입', '잔고', '수익률', '기타']
            self.excel_handler.write_sheet_data('Balance', balance_data, balance_headers)

            # Portfolio 데이터 저장
            portfolio_data = self.get_table_data(self.portfolio_table)
            portfolio_headers = ['종목코드', '종목명', '자산군', '구분', '세팅비중', '현재비중', '빨강매수']
            self.excel_handler.write_sheet_data('Portfolio', portfolio_data, portfolio_headers)

            self.excel_handler.save()

        except Exception as e:
            QMessageBox.warning(self, "오류", f"데이터 저장 실패: {str(e)}")

    def populate_table(self, table, data):
        """테이블에 데이터 채우기"""
        table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else '')
                table.setItem(row_idx, col_idx, item)

    def get_table_data(self, table):
        """테이블에서 데이터 가져오기"""
        data = []
        for row_idx in range(table.rowCount()):
            row_data = []
            for col_idx in range(table.columnCount()):
                item = table.item(row_idx, col_idx)
                row_data.append(item.text() if item else '')
            data.append(row_data)
        return data

    def add_row(self, table):
        """테이블에 행 추가"""
        table.insertRow(table.rowCount())

    def delete_row(self, table):
        """테이블에서 선택된 행 삭제"""
        current_row = table.currentRow()
        if current_row >= 0:
            table.removeRow(current_row)
            self.save_data()

    def upload_etf_file(self):
        """ETF 파일 업로드"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "ETF 파일 선택", "", "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )

        if file_path:
            try:
                # 파일에서 데이터 읽기
                uploaded_data = ExcelHandler.read_uploaded_file(file_path)

                # ROI 테이블 업데이트
                for row_idx in range(self.roi_table.rowCount()):
                    code_item = self.roi_table.item(row_idx, 0)
                    if code_item:
                        code = code_item.text().strip()
                        if code in uploaded_data:
                            # 종목명 업데이트
                            self.roi_table.setItem(row_idx, 1,
                                                  QTableWidgetItem(uploaded_data[code]['종목명']))
                            # 종가 업데이트
                            self.roi_table.setItem(row_idx, 4,
                                                  QTableWidgetItem(str(uploaded_data[code]['종가'])))

                # Balance 테이블 업데이트 (연도/월 추출)
                year, month = ExcelHandler.extract_date_from_filename(file_path)
                if year and month:
                    # 새 행 추가
                    row_count = self.balance_table.rowCount()
                    self.balance_table.insertRow(row_count)
                    self.balance_table.setItem(row_count, 0, QTableWidgetItem(year))
                    self.balance_table.setItem(row_count, 1, QTableWidgetItem(month))

                # 계산 수행
                self.recalculate_roi()
                self.recalculate_balance()
                self.update_balance_chart()

                # 저장
                self.save_data()

                QMessageBox.information(self, "성공", "ETF 파일이 업로드되었습니다.")

            except Exception as e:
                QMessageBox.warning(self, "오류", f"파일 업로드 실패: {str(e)}")

    def upload_stock_file(self):
        """주식 파일 업로드"""
        QMessageBox.information(self, "정보", "주식 파일 업로드 기능은 준비 중입니다.")

    def on_roi_cell_changed(self, row, col):
        """ROI 셀 변경 이벤트"""
        self.recalculate_roi()
        self.save_data()

    def on_balance_cell_changed(self, row, col):
        """Balance 셀 변경 이벤트"""
        self.recalculate_balance()
        self.update_balance_chart()
        self.save_data()

    def on_portfolio_cell_changed(self, row, col):
        """Portfolio 셀 변경 이벤트"""
        self.save_data()

    def recalculate_roi(self):
        """ROI 테이블 재계산"""
        self.roi_table.blockSignals(True)  # 신호 차단

        for row_idx in range(self.roi_table.rowCount()):
            # 평가금 계산 (수량 * 종가)
            quantity_item = self.roi_table.item(row_idx, 3)
            price_item = self.roi_table.item(row_idx, 4)

            quantity = float(quantity_item.text()) if quantity_item and quantity_item.text() else 0
            price = float(price_item.text()) if price_item and price_item.text() else 0

            evaluation = self.calculator.calculate_evaluation(quantity, price)
            self.roi_table.setItem(row_idx, 5, QTableWidgetItem(f"{evaluation:,.0f}"))

            # 수익률 계산
            initial_item = self.roi_table.item(row_idx, 2)
            initial = float(initial_item.text()) if initial_item and initial_item.text() else 0

            roi = self.calculator.calculate_roi(evaluation, initial)
            roi_item = QTableWidgetItem(f"{roi:.2f}%")

            # 수익률이 마이너스면 빨간색 볼드
            if roi < 0:
                roi_item.setForeground(QColor(255, 0, 0))
                roi_item.setFont(QFont("Arial", 10, QFont.Bold))

            self.roi_table.setItem(row_idx, 6, roi_item)

        self.roi_table.blockSignals(False)  # 신호 복원

    def recalculate_balance(self):
        """Balance 테이블 재계산"""
        self.balance_table.blockSignals(True)  # 신호 차단

        # ROI 테이블에서 총 합계 계산
        total_initial = 0
        total_evaluation = 0

        for row_idx in range(self.roi_table.rowCount()):
            initial_item = self.roi_table.item(row_idx, 2)
            eval_item = self.roi_table.item(row_idx, 5)

            if initial_item and initial_item.text():
                total_initial += float(initial_item.text().replace(',', ''))
            if eval_item and eval_item.text():
                total_evaluation += float(eval_item.text().replace(',', ''))

        # Balance 테이블 업데이트
        for row_idx in range(self.balance_table.rowCount()):
            # 투자원금 = ROI 초기투자금 총합
            self.balance_table.setItem(row_idx, 2, QTableWidgetItem(f"{total_initial:,.0f}"))

            # 잔고 = ROI 평가금 총합
            self.balance_table.setItem(row_idx, 4, QTableWidgetItem(f"{total_evaluation:,.0f}"))

            # 수익률 계산
            balance_roi = self.calculator.calculate_balance_roi(total_evaluation, total_initial)
            self.balance_table.setItem(row_idx, 5, QTableWidgetItem(f"{balance_roi:.2f}%"))

        self.balance_table.blockSignals(False)  # 신호 복원

    def update_balance_chart(self):
        """Balance 차트 업데이트"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # 데이터 수집
        labels = []
        balances = []

        for row_idx in range(self.balance_table.rowCount()):
            year_item = self.balance_table.item(row_idx, 0)
            month_item = self.balance_table.item(row_idx, 1)
            balance_item = self.balance_table.item(row_idx, 4)

            if year_item and month_item and balance_item:
                label = f"{year_item.text()} {month_item.text()}"
                balance = float(balance_item.text().replace(',', '')) if balance_item.text() else 0

                labels.append(label)
                balances.append(balance)

        # 그래프 그리기
        if labels and balances:
            ax.plot(labels, balances, marker='o')
            ax.set_xlabel('연도/월')
            ax.set_ylabel('잔고')
            ax.set_title('잔고 추이')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()

    def rebalance_portfolio(self):
        """포트폴리오 리밸런싱"""
        self.portfolio_table.blockSignals(True)  # 신호 차단

        # ROI 테이블에서 총 평가금 계산
        total_evaluation = 0
        total_initial = 0

        for row_idx in range(self.roi_table.rowCount()):
            eval_item = self.roi_table.item(row_idx, 5)
            initial_item = self.roi_table.item(row_idx, 2)

            if eval_item and eval_item.text():
                total_evaluation += float(eval_item.text().replace(',', ''))
            if initial_item and initial_item.text():
                total_initial += float(initial_item.text().replace(',', ''))

        # Portfolio 테이블과 ROI 테이블 동기화
        # Portfolio 종목코드를 ROI와 동일하게 설정
        self.portfolio_table.setRowCount(self.roi_table.rowCount())
        for row_idx in range(self.roi_table.rowCount()):
            # 종목코드, 종목명 복사
            code_item = self.roi_table.item(row_idx, 0)
            name_item = self.roi_table.item(row_idx, 1)

            if code_item:
                self.portfolio_table.setItem(row_idx, 0, QTableWidgetItem(code_item.text()))
            if name_item:
                self.portfolio_table.setItem(row_idx, 1, QTableWidgetItem(name_item.text()))

        # Portfolio 계산
        for row_idx in range(self.portfolio_table.rowCount()):
            # 세팅비중 가져오기
            setting_ratio_item = self.portfolio_table.item(row_idx, 4)
            setting_ratio = float(setting_ratio_item.text()) if setting_ratio_item and setting_ratio_item.text() else 0

            # ROI 테이블에서 해당 종목의 평가금 가져오기
            eval_item = self.roi_table.item(row_idx, 5)
            evaluation = float(eval_item.text().replace(',', '')) if eval_item and eval_item.text() else 0

            # 현재비중 계산
            current_ratio = self.calculator.calculate_current_ratio(evaluation, total_evaluation)
            self.portfolio_table.setItem(row_idx, 5, QTableWidgetItem(f"{current_ratio:.1f}%"))

            # 빨강매수 계산
            rebalancing_amount = self.calculator.calculate_rebalancing(setting_ratio, current_ratio, total_evaluation)
            rebalancing_text = self.calculator.format_rebalancing(rebalancing_amount)
            rebalancing_item = QTableWidgetItem(rebalancing_text)

            # 양수면 빨간색
            if rebalancing_amount > 0:
                rebalancing_item.setForeground(QColor(255, 0, 0))

            self.portfolio_table.setItem(row_idx, 6, rebalancing_item)

        self.portfolio_table.blockSignals(False)  # 신호 복원

        # 저장
        self.save_data()

        QMessageBox.information(self, "성공", "포트폴리오 리밸런싱이 완료되었습니다.")
