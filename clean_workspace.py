import os
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(ROOT_DIR, "rachayitha code files")

# Obsolete / scratch files to remove in root
ROOT_REMOVE_FILES = [
    "All-Key-Mappers.html",
    "Keymap-Explorer.py",
    "TeluguType.zip",
    "Cargo.toml",
    "build-linux.sh",
    "build-macos.sh",
    "build-windows.bat",
    "validate_seo.py",
    "copy_assets.bat",
    "sync_showcase_image.bat",
    "setup_website_assets.py",
    "sync_website_data.bat",
    "build_web_dict.bat",
    "run_build_lm.bat",
    "push_to_repo.bat",
    "run_casual_tests.bat",
    "export_ph_assets.py",
    "sync_website.py",
]

# Obsolete folders to remove in root (abandoned Rust/Tauri attempt, old ui, dummy engine bridge)
ROOT_REMOVE_DIRS = [
    "src-tauri",
    "ui",
    "engine",
]

# Obsolete / scratch files to remove in rachayitha code files
CODE_REMOVE_FILES = [
    "test_engine.py",
    "verify_build.py",
    "build_installer.py",
    "main_working.py",
    "PRD.md",
    "README.md",
    "Rachayitha.spec",
    "Rachayitha_Setup.spec",
    "installer.iss",
    "Install_Rachayitha.bat",
    "build_standalone.bat",
    "clean.bat",
    "build_installer.bat",
    "run_casual_tests.bat",
    "export_ph_assets.py",
]

# Temporary build caches to remove in rachayitha code files
CODE_REMOVE_DIRS = [
    "build",
    "dist",
]

def clean():
    print("=" * 70)
    print("  Rachayitha (రచయిత) - Canonical Workspace Cleaner & Debt Reducer")
    print("=" * 70)

    removed_count = 0

    # 1. Clean root files
    for fname in ROOT_REMOVE_FILES:
        p = os.path.join(ROOT_DIR, fname)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[REMOVED FILE] {fname}")
                removed_count += 1
            except Exception as e:
                print(f"[SKIP/ERROR] {fname}: {e}")

    # 2. Clean root dirs
    for dname in ROOT_REMOVE_DIRS:
        p = os.path.join(ROOT_DIR, dname)
        if os.path.exists(p):
            try:
                shutil.rmtree(p)
                print(f"[REMOVED DIR]  {dname}/")
                removed_count += 1
            except Exception as e:
                print(f"[SKIP/ERROR] {dname}: {e}")

    # 3. Clean inner code files
    for fname in CODE_REMOVE_FILES:
        p = os.path.join(CODE_DIR, fname)
        if os.path.exists(p):
            try:
                os.remove(p)
                print(f"[REMOVED FILE] rachayitha code files/{fname}")
                removed_count += 1
            except Exception as e:
                print(f"[SKIP/ERROR] rachayitha code files/{fname}: {e}")

    # 4. Clean inner code dirs
    for dname in CODE_REMOVE_DIRS:
        p = os.path.join(CODE_DIR, dname)
        if os.path.exists(p):
            try:
                shutil.rmtree(p)
                print(f"[REMOVED DIR]  rachayitha code files/{dname}/")
                removed_count += 1
            except Exception as e:
                print(f"[SKIP/ERROR] rachayitha code files/{dname}: {e}")

    # 5. Clean Python __pycache__ recursively
    for base in [ROOT_DIR, CODE_DIR]:
        if not os.path.exists(base):
            continue
        for root, dirs, _ in os.walk(base):
            for d in list(dirs):
                if d in ("__pycache__", ".pytest_cache"):
                    pycache_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(pycache_path)
                        rel = os.path.relpath(pycache_path, ROOT_DIR)
                        print(f"[REMOVED CACHE] {rel}/")
                        removed_count += 1
                    except Exception:
                        pass

    print("-" * 70)
    print(f"Cleanup finished. Total items purged: {removed_count}")
    print("=" * 70)

if __name__ == "__main__":
    clean()
