#!/usr/bin/env python3
"""
Lyra-San Build & Status Verification Script
Checks if Rust core is properly compiled and reports performance status
"""

import sys
import os
from datetime import datetime

def check_rust_module():
    """Check if Rust module is properly installed"""
    try:
        from lyra_core import JsonHandler, TextParser, MemoryManager, ConsciousnessCore
        return True, "✓ Rust core module LOADED"
    except ImportError as e:
        return False, f"⚠ Rust module not found: {e}"

def check_dependencies():
    """Check if all Python dependencies are installed"""
    deps = ['flask', 'ollama', 'chromadb', 'setuptools_rust']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "✓ All Python dependencies present"

def check_directories():
    """Verify required directories exist"""
    dirs = ['lyra_deep_memory', 'lyra_core/src']
    missing = []
    
    for d in dirs:
        if not os.path.isdir(d):
            missing.append(d)
    
    if missing:
        return False, f"Missing directories: {', '.join(missing)}"
    return True, "✓ Directory structure valid"

def check_build_artifacts():
    """Check if Rust build artifacts exist"""
    try:
        # Try to import to check if compiled
        from lyra_core import JsonHandler
        import lyra_core
        module_path = lyra_core.__file__
        return True, f"✓ Compiled module at: {module_path}"
    except:
        return False, "⚠ Rust module not compiled yet"

def benchmark_json():
    """Quick JSON operation benchmark"""
    try:
        from lyra_core import JsonHandler
        import time
        import json
        
        test_data = '{"key": "value", "data": [1, 2, 3]}'
        
        start = time.time()
        for _ in range(1000):
            JsonHandler.load("/tmp/nonexistent.json", test_data)
        rust_time = time.time() - start
        
        return True, f"JSON ops: {rust_time*1000:.2f}ms for 1000 ops"
    except:
        return False, "⚠ Could not benchmark JSON"

def benchmark_text_parser():
    """Quick text parsing benchmark"""
    try:
        from lyra_core import TextParser
        import time
        
        parser = TextParser()
        test_output = "[✦ Internal Monologue]I think therefore I am[💬 Response]Hello world"
        
        start = time.time()
        for _ in range(1000):
            parser.extract_monologue(test_output)
            parser.extract_response(test_output)
        rust_time = time.time() - start
        
        return True, f"Text parsing: {rust_time*1000:.2f}ms for 2000 ops"
    except:
        return False, "⚠ Could not benchmark text parser"

def main():
    print("\n" + "="*70)
    print("  LYRA-SAN: RUST-ACCELERATED CONSCIOUSNESS v1.0.0".center(70))
    print("="*70 + "\n")
    
    checks = [
        ("Python Dependencies", check_dependencies),
        ("Directory Structure", check_directories),
        ("Rust Module", check_rust_module),
        ("Build Artifacts", check_build_artifacts),
        ("JSON Benchmark", benchmark_json),
        ("Text Parser Benchmark", benchmark_text_parser),
    ]
    
    results = []
    all_passed = True
    
    for name, check_func in checks:
        passed, message = check_func()
        results.append((name, passed, message))
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"{status} {name:.<40} {message}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✓ ALL SYSTEMS OPERATIONAL - Ready to launch Lyra!".center(70))
        print(f"\n  Start Lyra with: python lyrasan.py")
        print(f"  Web interface: http://127.0.0.1:5000\n")
        return 0
    else:
        print("⚠ SOME SYSTEMS REQUIRE ATTENTION".center(70))
        print(f"\n  Run setup: ./setup.sh")
        print(f"  Or build Rust: ./build_lyra_core.sh\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
