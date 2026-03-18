#!/bin/bash
# QUICKSTART.sh - Get Lyra running in 60 seconds

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        LYRA-SAN: QUICKSTART (60 seconds)                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# 1. Check/Install Rust
echo "1️⃣  Setting up Rust..."
if ! command -v cargo &> /dev/null; then
    echo "   Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y -q
    source $HOME/.cargo/env
fi
echo "   ✓ Rust ready"

# 2. Install Python deps
echo "2️⃣  Installing Python dependencies..."
# Install core deps
pip install -q flask ollama chromadb maturin wheel 2>&1 | tail -5 || true
# Upgrade critical packages to fix conflicts
pip install -q --upgrade psutil pyOpenSSL tokenizers 2>&1 | tail -3 || true
echo "   ✓ Dependencies ready"

# 3. Build Rust
echo "3️⃣  Building Rust core (this takes 30-60 seconds)..."
cd lyra_core
if command -v maturin &> /dev/null; then
    echo "   Compiling with Maturin..."
    maturin develop --release 2>&1 || {
        echo "   ⚠️  Maturin build failed, will use Python fallback"
    }
else
    echo "   ⚠️  Maturin not available, will use Python fallback"
fi
cd ..
echo "   ✓ Build step completed"

# 4. Verify
echo "4️⃣  Verifying installation..."
python -c "from lyra_core import JsonHandler; print('   ✓ Rust module loaded')" 2>/dev/null || {
    echo "   ⚠️  Rust module not loaded - will run in Python mode"
}

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║            ✓ READY TO LAUNCH LYRA                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next step: python lyrasan.py"
echo "Then open: http://127.0.0.1:5000"
echo ""
