"""
Helper script to export generated Product Hunt assets to workspace folder
"""
import shutil
from pathlib import Path

SOURCE_DIR = Path(r"C:\Users\Sm!le\.gemini\antigravity-ide\brain\c576fa95-679d-4be7-895d-eb6b4cc03179")
# Put them in Desktop\రచయిత\product_hunt_assets
DEST_DIR = Path(__file__).resolve().parent.parent / "product_hunt_assets"

DEST_DIR.mkdir(parents=True, exist_ok=True)

ASSETS = [
    ("ph_thumbnail_icon_1790612037586.jpg", "01_product_hunt_icon_square_1x1.jpg"),
    ("product_hunt_hero_showcase_1790611936945.jpg", "02_hero_transliteration_16x9.jpg"),
    ("ph_features_keymap_1790611990186.jpg", "03_features_keymap_playground_16x9.jpg"),
    ("ph_universal_apps_1790612011846.jpg", "04_universal_apps_offline_16x9.jpg")
]

print("🚀 Exporting Product Hunt Assets...")
for src_name, dest_name in ASSETS:
    src_path = SOURCE_DIR / src_name
    dest_path = DEST_DIR / dest_name
    if src_path.exists():
        shutil.copy2(src_path, dest_path)
        print(f"  [✓] Copied: {dest_name}")
    else:
        print(f"  [!] Missing: {src_name}")

print(f"\nAll assets exported successfully to:\n{DEST_DIR.resolve()}\n")
