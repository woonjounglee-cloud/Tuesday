"""Tuesday - Excel 문서 관리 프로그램

메인 실행 파일
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

# 현재 디렉토리를 파이썬 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from src.ui.main_window import MainWindow


def main():
    """메인 함수"""
    # QApplication 생성
    app = QApplication(sys.argv)

    # 기본 폰트 설정
    font = QFont("맑은 고딕", 10)
    app.setFont(font)

    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()

    # 이벤트 루프 실행
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
