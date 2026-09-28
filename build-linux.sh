#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  Rachayitha (రచయిత) - Linux Standalone App Build"
echo "========================================================"

echo "[1/3] Generating icons..."
python3 scripts/setup_icons.py || true

echo "[2/3] Checking dependencies..."
if ! command -v cargo &> /dev/null; then
    echo "[ERROR] Cargo/Rust is not installed. Visit https://rustup.rs"
    exit 1
fi

echo "[3/3] Compiling Linux release binary..."
cd src-tauri
cargo build --release
cd ..

echo "Build complete! Binary located at target/release/rachayitha"
