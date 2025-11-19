"""
간단한 PySide6 설치 스크립트 - 버전 제약 없음
"""
import sys
import subprocess

print("=" * 60)
print("PySide6 Simple Installer")
print("=" * 60)

python_version = sys.version_info
print(f"\nPython Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
print(f"Python Path: {sys.executable}")

# Python 버전 체크
if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
    print("\n✗ Error: Python 3.8 or later is required")
    print("  Your Python version is too old")
    print("\n  Please install Python 3.10 from: https://www.python.org/downloads/")
    sys.exit(1)

if python_version.minor >= 12:
    print("\n⚠ Warning: Python 3.12+ may have limited PySide6 support")
    print("  Recommendation: Use Python 3.10 or 3.11 for best compatibility")
    print("\n  Do you want to continue anyway? (y/n)")
    # For automated scripts, we'll continue
    print("  Continuing...\n")

print("=" * 60)
print("Installing packages...")
print("=" * 60)

try:
    # 1. pip 업그레이드
    print("\n[1/4] Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # 2. PySide6 설치 (버전 지정 없이)
    print("\n[2/4] Installing PySide6 (latest compatible version)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
    except subprocess.CalledProcessError:
        print("\n  ✗ PySide6 installation failed")
        print("  Trying with --user flag...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "PySide6"])

    # 3. openpyxl 설치
    print("\n[3/4] Installing openpyxl...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])

    # 4. matplotlib 설치
    print("\n[4/4] Installing matplotlib...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])

    print("\n" + "=" * 60)
    print("✓ Installation Complete!")
    print("=" * 60)

    # 설치 확인
    print("\nVerifying installation...")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6 import QtCore
        print(f"✓ PySide6 version: {QtCore.__version__}")
        print(f"✓ Qt version: {QtCore.qVersion()}")
        print("\n✓ PySide6 is working correctly!")
    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        print("\n⚠ PySide6 may not be compatible with your Python version")
        print("\nRecommended solutions:")
        print("1. Install Python 3.10: https://www.python.org/downloads/release/python-31011/")
        print("2. Or stay with PyQt5 (see TROUBLESHOOTING.md)")
        sys.exit(1)

except subprocess.CalledProcessError as e:
    print(f"\n✗ Installation failed: {e}")
    print("\nPossible causes:")
    print("1. Internet connection issue")
    print("2. Python version incompatibility")
    print("3. pip configuration issue")
    print("\nRecommended solution:")
    print("  Install Python 3.10.11 from: https://www.python.org/downloads/")
    sys.exit(1)

print("\n" + "=" * 60)
print("Next Steps:")
print("=" * 60)
print("1. Run: python convert_to_pyside6.py")
print("2. Run: python main.py")
print("=" * 60)
