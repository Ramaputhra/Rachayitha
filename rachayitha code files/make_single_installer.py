import os
import sys
import subprocess
import shutil
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
OUTPUT_DIR = os.path.join(ROOT_DIR, "installer_output")
MAIN_EXE = os.path.join(DIST_DIR, "Rachayitha.exe")
SETUP_SRC = os.path.join(ROOT_DIR, "installer_src", "setup_gui.py")
LOGO_PNG = os.path.join(ROOT_DIR, "rachayitha_logo.png")
ICON_ICO = os.path.join(ROOT_DIR, "icon.ico")

def clean_old_builds():
    print("\n[0/4] Cleaning previous processes and build caches...")
    # 1. Kill running instances so files are not locked
    subprocess.run(["taskkill", "/F", "/IM", "Rachayitha.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "Rachayitha_Setup.exe"], capture_output=True)

    # 2. Clean build directories for a guaranteed fresh build
    for folder in ["build", "dist", "installer_output"]:
        fpath = os.path.join(ROOT_DIR, folder)
        if os.path.exists(fpath):
            try:
                shutil.rmtree(fpath)
                print(f"  Removed old {folder}/")
            except Exception as e:
                print(f"  Note on {folder}: {e}")

def main():
    print("=" * 70)
    print("  Rachayitha (రచయిత) - Clean Standalone Single Installer Builder")
    print("=" * 70)

    clean_old_builds()

    # 1. Prepare icons from rachayitha_logo.png
    print("\n[1/3] Preparing application icons from rachayitha_logo.png...")
    prepare_script = os.path.join(ROOT_DIR, "prepare_icons.py")
    subprocess.run([sys.executable, prepare_script], cwd=ROOT_DIR)

    icon_flag = f"--icon={ICON_ICO}" if os.path.exists(ICON_ICO) else None

    # 2. Compile Main Application Rachayitha.exe
    print("\n[2/3] Compiling fresh Rachayitha.exe with Halant-First engine...")
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
    print("\n[3/3] Compiling single installer: installer_output\\Rachayitha_Setup.exe...")
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

        print("\n" + "=" * 70)
        print("  SUCCESS! Fresh Windows Single Installer created at:")
        print(f"  Path: {final_setup}")
        print(f"  Timestamp: {mtime} (FRESH BUILD)")
        print(f"  Size: {size_mb:.2f} MB")
        print("=" * 70)
        print("\nFeatures in this clean build:")
        print("  • Halant-First typing logic (N -> న్, Na -> న, Ksha -> క్ష, NN -> న్న్)")
        print("  • Official app branding with rachayitha_logo.png (app & installer)")
        print("  • Professional 2-column installer with live feature presentation carousel")
        print("  • Integrated clean Windows uninstaller method (Settings -> Installed Apps)")
        print("  • Dynamic System Tray icon ('తె' / 'EN') showing active language")
        print("  • Click-to-open Key Map Table & live custom hotkey setting")
    else:
        print("[ERROR] Failed to build Rachayitha_Setup.exe")
        sys.exit(1)

if __name__ == "__main__":
    main()
