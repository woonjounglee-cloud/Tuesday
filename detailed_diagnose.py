"""
상세 환경 진단 스크립트
"""
import sys
import subprocess
import platform

print("=" * 70)
print("DETAILED ENVIRONMENT DIAGNOSIS")
print("=" * 70)

# 1. Python 정보
print("\n[1] PYTHON INFORMATION")
print("-" * 70)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python version_info: {sys.version_info}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")

# 2. pip 정보
print("\n[2] PIP INFORMATION")
print("-" * 70)
try:
    result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                          capture_output=True, text=True)
    print(f"pip version: {result.stdout.strip()}")
except Exception as e:
    print(f"Error checking pip: {e}")

# 3. sys.path 확인
print("\n[3] PYTHON PATH")
print("-" * 70)
for i, path in enumerate(sys.path[:10], 1):
    print(f"{i}. {path}")

# 4. 가상환경 확인
print("\n[4] VIRTUAL ENVIRONMENT")
print("-" * 70)
venv = sys.prefix != sys.base_prefix
print(f"In virtual environment: {venv}")
print(f"sys.prefix: {sys.prefix}")
print(f"sys.base_prefix: {sys.base_prefix}")

# 5. 설치된 패키지 확인
print("\n[5] INSTALLED GUI PACKAGES")
print("-" * 70)
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"],
                          capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if any(pkg in line.lower() for pkg in ['pyqt', 'pyside', 'qt']):
            print(f"  {line}")
except Exception as e:
    print(f"Error listing packages: {e}")

# 6. PySide6 설치 시도 (dry-run)
print("\n[6] PYSIDE6 AVAILABILITY TEST")
print("-" * 70)
print("Testing if PySide6 can be installed...")
try:
    result = subprocess.run([sys.executable, "-m", "pip", "install",
                           "--dry-run", "PySide6"],
                          capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("✓ PySide6 CAN be installed")
        print(result.stdout[:500])
    else:
        print("✗ PySide6 CANNOT be installed")
        print("STDOUT:", result.stdout[:500])
        print("STDERR:", result.stderr[:500])
except Exception as e:
    print(f"Error testing PySide6: {e}")

# 7. pip 설정 확인
print("\n[7] PIP CONFIGURATION")
print("-" * 70)
try:
    result = subprocess.run([sys.executable, "-m", "pip", "config", "list"],
                          capture_output=True, text=True)
    print(result.stdout if result.stdout else "(No custom configuration)")
except Exception as e:
    print(f"Error checking pip config: {e}")

# 8. 인터넷 연결 확인
print("\n[8] NETWORK TEST")
print("-" * 70)
try:
    import urllib.request
    response = urllib.request.urlopen('https://pypi.org', timeout=5)
    print(f"✓ Can reach PyPI (status: {response.status})")
except Exception as e:
    print(f"✗ Cannot reach PyPI: {e}")

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)

# 9. 권장 사항
print("\n[9] RECOMMENDATIONS")
print("-" * 70)

if sys.version_info >= (3, 13):
    print("⚠ WARNING: Python 3.13+ detected")
    print("  → PySide6 may not be available")
    print("  → Use Python 3.10 or 3.11 instead")
elif not venv:
    print("⚠ WARNING: Not in a virtual environment")
    print("  → Recommended to use: py -3.10 -m venv venv310")
else:
    print("✓ Python version looks compatible")
    print("✓ Using virtual environment")
    print("\nIf PySide6 still fails to install, try:")
    print("  1. pip cache purge")
    print("  2. python -m pip install --upgrade pip")
    print("  3. pip install --no-cache-dir PySide6")

print("=" * 70)
