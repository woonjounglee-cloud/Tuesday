#!/bin/bash
# Tuesday 빌드 스크립트 (Linux/Mac)

echo "==================================="
echo "Tuesday Build Script"
echo "==================================="

# 가상환경 활성화 (선택사항)
# source venv/bin/activate

echo ""
echo "[1/3] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/3] Creating sample database..."
python create_sample_db.py

echo ""
echo "[3/3] Building executable..."
pyinstaller Tuesday.spec

echo ""
echo "==================================="
echo "Build Complete!"
echo "Executable location: dist/Tuesday"
echo "==================================="
