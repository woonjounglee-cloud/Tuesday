"""
PyQt5 코드를 PySide6로 자동 변환하는 스크립트
"""
import os
import re

def convert_file(file_path):
    """파일의 PyQt5 import를 PySide6로 변환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # PyQt5를 PySide6로 변경
    original_content = content
    content = content.replace('from PyQt5', 'from PySide6')
    content = content.replace('import PyQt5', 'import PySide6')

    # matplotlib backend도 변경
    content = content.replace('backend_qt5agg', 'backend_qtagg')

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def convert_project():
    """프로젝트 전체 파일 변환"""
    print("PyQt5 → PySide6 변환 시작...")

    converted_files = []

    # main.py 변환
    if os.path.exists('main.py'):
        if convert_file('main.py'):
            converted_files.append('main.py')

    # src 폴더 변환
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if convert_file(file_path):
                    converted_files.append(file_path)

    print(f"\n변환된 파일 ({len(converted_files)}개):")
    for file in converted_files:
        print(f"  ✓ {file}")

    print("\n변환 완료!")

if __name__ == '__main__':
    convert_project()
