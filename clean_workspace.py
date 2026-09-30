import os
import shutil

ROOT_DIR = r"c:\Users\Sm!le\Desktop\రచయిత"
CODE_DIR = os.path.join(ROOT_DIR, "rachayitha code files")

# Files to remove in root
ROOT_REMOVE_FILES = [
    "All-Key-Mappers.html",
    "Keymap-Explorer.py",
    "TeluguType.zip",
    "Rachayitha.exe",
    "Cargo.toml",
    "build-linux.sh",
    "build-macos.sh",
    "build-windows.bat",
    "validate_seo.py",
]

# Folders to remove in root (abandoned Rust/Tauri attempt)
ROOT_REMOVE_DIRS = [
    "src-tauri",
    "ui",
    "scripts",
]

# Files to remove in rachayitha code files
CODE_REMOVE_FILES = [
    "test_engine.py",
    "verify_build.py",
    "build_installer.py",
    "main_working.py",
    "PRD.md",
    "Rachayitha.spec",
    "Rachayitha_Setup.spec",
]

# Folders to remove in rachayitha code files (temporary build cache)
CODE_REMOVE_DIRS = [
    "build",
]

def clean():
    print("=" * 60)
    print("  Rachayitha Codebase Cleaner")
    print("=" * 60)

    # Clean root files
    for fname in ROOT_REMOVE_FILES:
        p = os.path.join(ROOT_DIR, fname)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[REMOVED FILE] {fname}")
            except Exception as e:
                print(f"[ERROR] {fname}: {e}")

    # Clean root dirs
    for dname in ROOT_REMOVE_DIRS:
        p = os.path.join(ROOT_DIR, dname)
        if os.path.exists(p):
            try:
                shutil.rmtree(p)
                print(f"[REMOVED DIR]  {dname}/")
            except Exception as e:
                print(f"[ERROR] {dname}: {e}")

    # Clean code files
    for fname in CODE_REMOVE_FILES:
        p = os.path.join(CODE_DIR, fname)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[REMOVED FILE] rachayitha code files/{fname}")
            except Exception as e:
                print(f"[ERROR] rachayitha code files/{fname}: {e}")

    # Clean code dirs
    for dname in CODE_REMOVE_DIRS:
        p = os.path.join(CODE_DIR, dname)
        if os.path.exists(p):
            try:
                shutil.rmtree(p)
                print(f"[REMOVED DIR]  rachayitha code files/{dname}/")
            except Exception as e:
                print(f"[ERROR] rachayitha code files/{dname}: {e}")

    print("\n" + "=" * 60)
    print("  Cleanup Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    clean()
