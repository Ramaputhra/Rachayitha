#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  Rachayitha (రచయిత) - macOS Standalone App Build"
echo "========================================================"

echo "[1/3] Generating icons..."
python3 scripts/setup_icons.py || true

echo "[2/3] Checking Rust environment..."
if ! command -v cargo &> /dev/null; then
    echo "[ERROR] Cargo/Rust is not installed. Visit https://rustup.rs"
    exit 1
fi

echo "[3/3] Compiling macOS release bundle (.app / .dmg)..."
cd src-tauri
cargo build --release
cd ..

echo "Build complete! Binary located at target/release/rachayitha"
