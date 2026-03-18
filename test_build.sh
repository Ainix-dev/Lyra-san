#!/bin/bash
set -x  # Debug mode
cd /home/nehtrm/Desktop/Lyra-san

echo "Step 1: Check Python"
python3 --version

echo "Step 2: Upgrade pip"
python3 -m pip install --upgrade pip 2>&1 | tail -3

echo "Step 3: Install maturin"
python3 -m pip install maturin wheel 2>&1 | tail -3

echo "Step 4: Clean old artifacts"
cd lyra_core
rm -rf target build *.egg-info
cd ..

echo "Step 5: Build Rust"
cd lyra_core
maturin develop --release 2>&1 | tail -50
BUILD_STATUS=$?
cd ..

echo "Step 6: Test import"
python3 -c "from lyra_core import JsonHandler; print('✓ Import successful')" 2>&1 || echo "⚠ Import failed - will use Python fallback"

echo "Done. Build status: $BUILD_STATUS"
