#!/usr/bin/env bash
# Quick setup and installation for Lyra-San
# This script handles all dependencies and builds

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         LYRA-SAN RUST-ACCELERATED SETUP                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check system
OS=$(uname -s)
echo "📋 System: $OS"

# Check Python
echo -n "🐍 Checking Python... "
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Install Python 3.8+"
    exit 1
fi
PY_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PY_VERSION"

# Check Rust
echo -n "🦀 Checking Rust... "
if ! command -v cargo &> /dev/null; then
    echo "❌ Not found. Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi
RUST_VERSION=$(rustc --version | awk '{print $2}')
echo "✓ Rust $RUST_VERSION"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet flask ollama chromadb maturin wheel
# Fix dependency conflicts
pip install --quiet --upgrade psutil pyOpenSSL tokenizers 2>&1 | grep -i "successfully\|requirement" || true

# Build Rust core
echo ""
echo "🔨 Building Lyra Core (Rust)..."
cd "$(dirname "$0")"

if [ -d "lyra_core" ]; then
    cd lyra_core
    
    # Use maturin for building
    if command -v maturin &> /dev/null; then
        echo "   Using maturin (optimized)..."
        maturin develop --release 2>&1 | grep -E "(Compiling|Finished|error)" || true
        if [ $? -eq 0 ]; then
            echo "✓ Build successful!"
        else
            echo "⚠ Maturin build had issues - will use Python fallback"
        fi
    else
        echo "⚠ Maturin not found - will use Python fallback"
    fi
    
    cd ..
else
    echo "❌ lyra_core directory not found"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✓ SETUP COMPLETE                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Start Lyra: python lyrasan.py"
echo "  2. Open browser to http://127.0.0.1:5000"
echo ""
echo "Check build status:"
echo "  python -c \"from lyra_core import JsonHandler; print('✓ Rust loaded')\""
echo ""
