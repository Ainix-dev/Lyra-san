#!/usr/bin/env bash
# Build script for Lyra Core Rust library
# Requires: Rust toolchain, maturin, or setuptools-rust

set -e

echo "🔨 Building Lyra Core Rust library..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Python dev headers exist
if ! python3 -c "import sysconfig; print(sysconfig.get_path('include'))" > /dev/null 2>&1; then
    echo "❌ Python development headers not found. Install python3-dev."
    exit 1
fi

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust toolchain not found. Install from https://rustup.rs/"
    exit 1
fi

cd "$(dirname "$0")"

# Install maturin and dependencies
if ! command -v maturin &> /dev/null; then
    echo "📦 Installing maturin..."
    pip install maturin wheel
fi

# Fix dependency conflicts
pip install --upgrade psutil pyOpenSSL tokenizers 2>&1 | grep -i "successfully\|requirement" || true

# Build with maturin (faster for PyO3)
echo "🚀 Compiling with maturin..."
cd lyra_core
maturin develop --release 2>&1 | tail -20
cd ..

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Lyra Core built successfully!"
echo ""
echo "You can now import lyra_core in Python:"
echo "  from lyra_core import JsonHandler, TextParser, MemoryManager, ConsciousnessCore"
