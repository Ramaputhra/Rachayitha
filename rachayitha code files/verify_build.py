import os
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SETUP_EXE = os.path.join(ROOT, "installer_output", "Rachayitha_Setup.exe")
MAIN_EXE = os.path.join(ROOT, "dist", "Rachayitha.exe")

def check():
    print("Build Artifact Timestamps:")
    print("-" * 60)
    for name, p in [("Rachayitha.exe (Main App)", MAIN_EXE), ("Rachayitha_Setup.exe (Installer)", SETUP_EXE)]:
        if os.path.exists(p):
            mtime = os.path.getmtime(p)
            dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            size_mb = os.path.getsize(p) / (1024 * 1024)
            print(f"File: {name}")
            print(f"  Path: {p}")
            print(f"  Modified: {dt} (Local Time)")
            print(f"  Size: {size_mb:.2f} MB")
            print()
        else:
            print(f"File: {name} does not exist.")

if __name__ == "__main__":
    check()
