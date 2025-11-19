"""
PySide6 호환성 확인 및 자동 설치 스크립트
"""
import sys
import subprocess

print("=" * 60)
print("PySide6 Compatibility Check and Auto Install")
print("=" * 60)

# Python 버전 확인
python_version = sys.version_info
print(f"\nPython Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
print(f"Python Path: {sys.executable}")

# Python 버전에 따른 PySide6 버전 추천
if python_version.major == 3:
    if python_version.minor >= 12:
        pyside6_version = "PySide6>=6.6.0"
        print("\n✓ Python 3.12+: Installing PySide6 6.6.0 or later")
    elif python_version.minor == 11:
        pyside6_version = "PySide6>=6.4.0"
        print("\n✓ Python 3.11: Installing PySide6 6.4.0 or later")
    elif python_version.minor == 10:
        pyside6_version = "PySide6>=6.2.0"
        print("\n✓ Python 3.10: Installing PySide6 6.2.0 or later")
    elif python_version.minor == 9:
        pyside6_version = "PySide6>=6.2.0"
        print("\n✓ Python 3.9: Installing PySide6 6.2.0 or later")
    elif python_version.minor == 8:
        pyside6_version = "PySide6>=6.2.0,<6.6.0"
        print("\n✓ Python 3.8: Installing PySide6 6.2.0 - 6.5.x")
    elif python_version.minor == 7:
        pyside6_version = "PySide6>=6.2.0,<6.4.0"
        print("\n✓ Python 3.7: Installing PySide6 6.2.0 - 6.3.x")
    else:
        print(f"\n✗ Python 3.{python_version.minor} is too old for PySide6")
        print("  Please upgrade to Python 3.8 or later")
        print("\n  Alternative: Use PyQt5 instead")
        sys.exit(1)
else:
    print("\n✗ Python 2 is not supported")
    print("  Please use Python 3.8 or later")
    sys.exit(1)

print("\n" + "=" * 60)
print("Installing PySide6...")
print("=" * 60)

try:
    # pip 업그레이드
    print("\n[1/3] Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # PySide6 설치
    print(f"\n[2/3] Installing {pyside6_version}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pyside6_version])

    # 추가 패키지 설치
    print("\n[3/3] Installing additional packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "openpyxl>=3.1.0", "matplotlib>=3.7.0"])

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
        print("  Please try running: pip install PySide6")
        sys.exit(1)

except subprocess.CalledProcessError as e:
    print(f"\n✗ Installation failed: {e}")
    print("\nTrying alternative method...")
    print("Please run manually:")
    print(f"  pip install {pyside6_version}")
    sys.exit(1)

print("\n" + "=" * 60)
print("Next Steps:")
print("=" * 60)
print("1. Run: python convert_to_pyside6.py")
print("2. Run: python main.py")
print("=" * 60)
