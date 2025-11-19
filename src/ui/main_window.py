"""메인 윈도우 UI"""
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .irp_tab import IRPTab


class MainWindow(QMainWindow):
    """Tuesday 메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tuesday - Excel 문서 관리")
        self.setGeometry(100, 100, 1200, 800)

        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 탭 위젯 생성
        self.tab_widget = QTabWidget()

        # Home 탭 생성
        home_tab = QTabWidget()
        home_irp_tab = IRPTab("db/Home_IRP.xlsx")
        home_tab.addTab(home_irp_tab, "IRP")
        self.tab_widget.addTab(home_tab, "Home")

        # WJ 탭 생성
        wj_tab = QTabWidget()
        wj_isa_tab = self.create_placeholder_tab("WJ-ISA")
        wj_stock_tab = self.create_placeholder_tab("WJ-주식")
        wj_tab.addTab(wj_isa_tab, "ISA")
        wj_tab.addTab(wj_stock_tab, "주식")
        self.tab_widget.addTab(wj_tab, "WJ")

        # MG 탭 생성
        mg_tab = QTabWidget()
        mg_irp_tab = self.create_placeholder_tab("MG-IRP")
        mg_pension_tab = self.create_placeholder_tab("MG-개인연금")
        mg_tab.addTab(mg_irp_tab, "IRP")
        mg_tab.addTab(mg_pension_tab, "개인연금")
        self.tab_widget.addTab(mg_tab, "MG")

        main_layout.addWidget(self.tab_widget)

    def create_placeholder_tab(self, name):
        """플레이스홀더 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{name} 탭은 준비 중입니다.")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def closeEvent(self, event):
        """윈도우 닫기 이벤트"""
        reply = QMessageBox.question(
            self, '종료',
            '프로그램을 종료하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
