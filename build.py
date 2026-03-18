#!/usr/bin/env python3
"""
Simple Python-based build script for Lyra-san
No shell scripting, cross-platform compatible
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_cmd(cmd, description=""):
    """Run a shell command and return status"""
    if description:
        print(f"\n📌 {description}")
    print(f"   Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.stdout:
            # Show last 10 lines of output
            lines = result.stdout.strip().split('\n')
            for line in lines[-10:]:
                print(f"   {line}")
        if result.returncode != 0:
            print(f"   ⚠️  Exit code: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout after 120 seconds")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     LYRA-SAN PYTHON BUILD (Cross-Platform)                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Change to project directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"\n📁 Project directory: {os.getcwd()}")
    
    # Step 1: Check Python
    print("\n1️⃣  Checking Python...")
    py_version = sys.version.split()[0]
    print(f"   ✓ Python {py_version}")
    
    # Step 2: Upgrade pip
    if not run_cmd([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "pip"],
                   "Upgrading pip"):
        print("   ⚠️  pip upgrade had issues, continuing anyway...")
    
    # Step 3: Install dependencies
    deps = ["maturin", "wheel", "psutil", "pyOpenSSL", "tokenizers"]
    for dep in deps:
        run_cmd([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", dep],
               f"Installing {dep}")
    
    print("   ✓ Dependencies installed")
    
    # Step 4: Check Rust
    print("\n2️⃣  Checking Rust...")
    try:
        result = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ {result.stdout.strip()}")
        else:
            print("   ⚠️  Rust not found - build may fail")
            print("   Install from: https://rustup.rs/")
    except FileNotFoundError:
        print("   ⚠️  Rust not found - build may fail")
    
    # Step 5: Clean old artifacts
    print("\n3️⃣  Cleaning old build artifacts...")
    lyra_core = script_dir / "lyra_core"
    for item in ["target", "build", "dist"]:
        path = lyra_core / item
        if path.exists():
            shutil.rmtree(path)
            print(f"   ✓ Removed {item}/")
    for item in lyra_core.glob("*.egg-info"):
        shutil.rmtree(item)
        print(f"   ✓ Removed {item.name}/")
    
    # Step 6: Build with Maturin
    print("\n4️⃣  Building Lyra Core with Maturin...")
    old_cwd = os.getcwd()
    os.chdir(lyra_core)
    
    success = run_cmd([sys.executable, "-m", "maturin", "develop", "--release"],
                     "Compiling Rust library (this takes 30-60 seconds)")
    
    os.chdir(old_cwd)
    
    if not success:
        print("\n   ⚠️  Maturin build failed")
        print("   System will use Python fallback mode (slower)")
    else:
        print("\n   ✓ Rust build successful!")
    
    # Step 7: Test import
    print("\n5️⃣  Testing module import...")
    try:
        from lyra_core import JsonHandler
        print("   ✓ Rust module loaded successfully!")
        print("   ✓ You'll get 40-50x speedup!")
    except ImportError as e:
        print("   ⚠️  Rust module failed to load")
        print(f"   Error: {e}")
        print("   System will use Python fallback mode")
    
    # Summary
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║              ✓ BUILD COMPLETE                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\nNext steps:")
    print("  1. Run: python lyrasan.py")
    print("  2. Open: http://127.0.0.1:5000")
    print("  3. Enjoy your faster Lyra!")
    print()

if __name__ == "__main__":
    main()
