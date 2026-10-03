import os
import sys
import subprocess
import shutil
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
DIST_DIR = os.path.join(ROOT_DIR, "dist")
OUTPUT_DIR = os.path.join(ROOT_DIR, "installer_output")
MAIN_EXE = os.path.join(DIST_DIR, "Rachayitha.exe")
SETUP_SRC = os.path.join(ROOT_DIR, "installer_src", "setup_gui.py")
LOGO_PNG = os.path.join(ROOT_DIR, "rachayitha_logo.png")
ICON_ICO = os.path.join(ROOT_DIR, "icon.ico")

def clean_old_builds():
    print("\n[0/4] Cleaning previous processes, build caches, and code debts...")
    # 1. Kill running instances so files are not locked
    subprocess.run(["taskkill", "/F", "/IM", "Rachayitha.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "Rachayitha_Setup.exe"], capture_output=True)

    # 2. Invoke canonical workspace cleanup script if present
    clean_script = os.path.join(PARENT_DIR, "clean_workspace.py")
    if os.path.exists(clean_script):
        try:
            subprocess.run([sys.executable, clean_script], cwd=PARENT_DIR)
        except Exception as e:
            print(f"  Note running clean_workspace.py: {e}")

    # 3. Clean build directories for a guaranteed fresh build
    for folder in ["build", "dist", "installer_output"]:
        fpath = os.path.join(ROOT_DIR, folder)
        if os.path.exists(fpath):
            try:
                shutil.rmtree(fpath)
                print(f"  Removed old {folder}/")
            except Exception as e:
                print(f"  Note on {folder}: {e}")

def run_tests():
    print("\n[1/4] Running 100% test suite validation before compilation...")
    test_script = os.path.join(ROOT_DIR, "test_casual_type.py")
    if os.path.exists(test_script):
        res = subprocess.run([sys.executable, test_script], cwd=ROOT_DIR)
        if res.returncode != 0:
            print("\n[ERROR] Test suite failed! Halting build to maintain 100% engine accuracy.")
            sys.exit(1)
        print("  ✓ All linguistic and phonetic engine tests PASSED!")
    else:
        print("  Note: test_casual_type.py not found, proceeding...")

def main():
    print("=" * 70)
    print("  Rachayitha (రచయిత) v2.0 - Clean Standalone Single Installer Builder")
    print("=" * 70)

    clean_old_builds()
    run_tests()

    # 1. Prepare icons from rachayitha_logo.png
    print("\n[2/4] Preparing application icons from rachayitha_logo.png...")
    prepare_script = os.path.join(ROOT_DIR, "prepare_icons.py")
    if os.path.exists(prepare_script):
        subprocess.run([sys.executable, prepare_script], cwd=ROOT_DIR)

    # 1.1 Sync data files (casual_type_dict.json, te_top10k.json, typo_fixes.json)
    parent_data = os.path.join(PARENT_DIR, "data")
    local_data = os.path.join(ROOT_DIR, "data")
    os.makedirs(local_data, exist_ok=True)
    for fname in [
        "casual_type_dict.json",
        "te_top10k.json",
        "typo_fixes.json",
        "te_lm.json",
        "casual_candidates.json",
        "telugu_rules.json",
        "config.json"
    ]:
        src = os.path.join(parent_data, fname)
        dst = os.path.join(local_data, fname)
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f"  Synced {fname} -> data/")
            except Exception as e:
                print(f"  Note copying {fname}: {e}")

    icon_flag = f"--icon={ICON_ICO}" if os.path.exists(ICON_ICO) else None

    # 2. Compile Main Application Rachayitha.exe
    print("\n[3/4] Compiling fresh Rachayitha.exe with Halant-First & Casual-Type engines...")
    cmd_app = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconsole", "--onefile",
        "--name=Rachayitha",
        "--add-data=data;data",
        "--add-data=engine;engine",
        "--add-data=ui;ui",
        f"--add-data={LOGO_PNG};." if os.path.exists(LOGO_PNG) else "--add-data=data;data",
        f"--add-data={ICON_ICO};." if os.path.exists(ICON_ICO) else "--add-data=data;data",
        "main.py"
    ]
    if icon_flag:
        cmd_app.insert(7, icon_flag)

    res = subprocess.run(cmd_app, cwd=ROOT_DIR)
    if res.returncode != 0:
        print("[ERROR] Failed to compile Rachayitha.exe")
        sys.exit(1)

    # 3. Package Professional Single Installer
    print("\n[4/4] Compiling single installer: installer_output\\Rachayitha_Setup.exe...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cmd_installer = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconsole", "--onefile",
        "--name=Rachayitha_Setup",
        f"--add-data={MAIN_EXE};.",
        f"--add-data={LOGO_PNG};." if os.path.exists(LOGO_PNG) else f"--add-data={MAIN_EXE};.",
        f"--add-data={ICON_ICO};." if os.path.exists(ICON_ICO) else f"--add-data={MAIN_EXE};.",
        f"--distpath={OUTPUT_DIR}",
        SETUP_SRC
    ]
    if icon_flag:
        cmd_installer.insert(7, icon_flag)

    res = subprocess.run(cmd_installer, cwd=ROOT_DIR)
    if res.returncode == 0:
        final_setup = os.path.join(OUTPUT_DIR, "Rachayitha_Setup.exe")
        mtime = datetime.fromtimestamp(os.path.getmtime(final_setup)).strftime("%Y-%m-%d %H:%M:%S")
        size_mb = os.path.getsize(final_setup) / (1024 * 1024)

        # Copy installer & portable exe to root and WebSite for easy distribution
        targets = [
            os.path.join(PARENT_DIR, "Rachayitha_Setup.exe"),
            os.path.join(PARENT_DIR, "WebSite", "Rachayitha_Setup.exe"),
        ]
        for t in targets:
            try:
                shutil.copy2(final_setup, t)
                print(f"  Synced installer -> {os.path.relpath(t, PARENT_DIR)}")
            except Exception as e:
                pass

        if os.path.exists(MAIN_EXE):
            try:
                shutil.copy2(MAIN_EXE, os.path.join(PARENT_DIR, "Rachayitha.exe"))
                shutil.copy2(MAIN_EXE, os.path.join(PARENT_DIR, "Rachayitha_v2.exe"))
                shutil.copy2(MAIN_EXE, os.path.join(PARENT_DIR, "WebSite", "Rachayitha.exe"))
                shutil.copy2(MAIN_EXE, os.path.join(PARENT_DIR, "WebSite", "Rachayitha_v2.exe"))
                print("  Synced portable executable -> Rachayitha.exe, Rachayitha_v2.exe & WebSite/Rachayitha_v2.exe")
            except Exception as e:
                pass

        # Sync showcase images if present
        try:
            ph_assets = os.path.join(PARENT_DIR, "product_hunt_assets")
            ws_assets = os.path.join(PARENT_DIR, "WebSite", "assets")
            if os.path.exists(ph_assets) and os.path.exists(ws_assets):
                for f in os.listdir(ph_assets):
                    if f.endswith(('.jpg', '.png')):
                        shutil.copy2(os.path.join(ph_assets, f), os.path.join(ws_assets, f))
        except Exception:
            pass

        print("\n" + "=" * 70)
        print("  SUCCESS! Fresh Windows Single Installer created at:")
        print(f"  Path: {final_setup}")
        print(f"  Timestamp: {mtime} (FRESH BUILD)")
        print(f"  Size: {size_mb:.2f} MB")
        print("=" * 70)
        print("\nFeatures in this clean v2.0 build:")
        print("  • IndicCorp 1M Trigram Language Model (34.7M Tokens, 2.81 MB)")
        print("  • Contextual Polarity Resolution ('akkada evaru leru' -> 'అక్కడ ఎవరూ లేరు')")
        print("  • Desktop Next-Word Prediction with floating ghost pill & [Tab ⇥] accept")
        print("  • Real-time 3-word sliding window retroactive correction buffer")
        print("  • Halant-First typing logic (N -> న్, Na -> న, Ksha -> క్ష, NN -> న్న్)")
        print("  • Casual Type 58,678-entry phonetic candidate lexicon & typo fixes")
        print("  • Official app branding with rachayitha_logo.png (app & installer)")
        print("  • Professional 2-column installer v2.0 with live feature presentation carousel")
        print("  • Integrated clean Windows uninstaller method (Settings -> Installed Apps)")
        print("  • Dynamic System Tray icon ('తె' / 'EN') showing active language")
        print("  • Click-to-open Key Map Table & live custom hotkey setting")
    else:
        print("[ERROR] Failed to build Rachayitha_Setup.exe")
        sys.exit(1)

if __name__ == "__main__":
    main()
