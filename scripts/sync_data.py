import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DATA = os.path.join(ROOT, "data")
DEST_DATA = os.path.join(ROOT, "rachayitha code files", "data")

os.makedirs(DEST_DATA, exist_ok=True)

files = ["casual_type_dict.json", "te_top10k.json", "typo_fixes.json"]
for f in files:
    src = os.path.join(SRC_DATA, f)
    dst = os.path.join(DEST_DATA, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Synced {f} -> {dst}")
    else:
        print(f"Warning: {src} does not exist")
