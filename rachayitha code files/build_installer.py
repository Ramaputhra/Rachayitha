import os
import sys
import subprocess
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_EXE = os.path.join(ROOT_DIR, "dist", "Rachayitha.exe")
ISS_FILE = os.path.join(ROOT_DIR, "installer.iss")
OUTPUT_DIR = os.path.join(ROOT_DIR, "installer_output")

def find_iscc():
    # 1. Check in PATH
    iscc = shutil.which("iscc") or shutil.which("ISCC")
    if iscc:
        return iscc

    # 2. Check standard Program Files locations
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Inno Setup 6\ISCC.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"),
        os.path.expandvars(r"%ProgramFiles%\Inno Setup 5\ISCC.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe"),
        os.path.expandvars(r"%LocalAppData%\Programs\Inno Setup 6\ISCC.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path

    return None

def build_installer():
    print("=" * 60)
    print("  Rachayitha (రచయిత) - Windows Installer Builder")
    print("=" * 60)

    # 1. Ensure standalone EXE exists
    if not os.path.exists(DIST_EXE):
        print("\n[1/3] Compiling standalone Rachayitha.exe with PyInstaller...")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--noconsole", "--onefile",
            "--name=Rachayitha",
            "--add-data=data;data",
            "--add-data=engine;engine",
            "--add-data=ui;ui",
            "main.py"
        ]
        ret = subprocess.run(cmd, cwd=ROOT_DIR)
        if ret.returncode != 0:
            print("[ERROR] PyInstaller failed to build Rachayitha.exe")
            return False
    else:
        print(f"\n[1/3] Found compiled executable: {DIST_EXE}")

    # 2. Locate ISCC.exe
    print("\n[2/3] Checking for Inno Setup Compiler (ISCC.exe)...")
    iscc_path = find_iscc()

    if not iscc_path:
        print("\n" + "!" * 60)
        print("  [NOTE] Inno Setup is not installed on this machine.")
        print("  To generate the official single setup file (Rachayitha_Setup.exe):")
        print("  Run this command in PowerShell:")
        print("      winget install JRSoftware.InnoSetup")
        print("!" * 60)
        print("\nIn the meantime, your standalone application is ready at:")
        print(f"  --> {DIST_EXE}")
        print("\nYou can also run 'Install_Rachayitha.bat' to install it to your PC right now!")
        return False

    print(f"Found Inno Setup Compiler at: {iscc_path}")

    # 3. Compile installer using Inno Setup
    print("\n[3/3] Compiling single installer (Rachayitha_Setup.exe)...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = [iscc_path, ISS_FILE]
    ret = subprocess.run(cmd, cwd=ROOT_DIR)

    if ret.returncode == 0:
        setup_exe = os.path.join(OUTPUT_DIR, "Rachayitha_Setup.exe")
        print("\n" + "=" * 60)
        print("  SUCCESS! Windows Single Installer created at:")
        print(f"  {setup_exe}")
        print("=" * 60)
        return True
    else:
        print("[ERROR] Inno Setup compilation failed.")
        return False

if __name__ == "__main__":
    success = build_installer()
    if not success and not os.path.exists(DIST_EXE):
        sys.exit(1)
