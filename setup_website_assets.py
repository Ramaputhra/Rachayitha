"""
Setup WebSite assets folder with real high-resolution product images
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEBSITE_DIR = ROOT / "WebSite"
ASSETS_DIR = WEBSITE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Copy marketing images
PH_DIR = ROOT / "product_hunt_assets"
mappings = [
    (PH_DIR / "01_product_hunt_icon_square_1x1.jpg", ASSETS_DIR / "icon_logo.jpg"),
    (PH_DIR / "02_hero_transliteration_16x9.jpg", ASSETS_DIR / "hero_showcase.jpg"),
    (PH_DIR / "03_features_keymap_playground_16x9.jpg", ASSETS_DIR / "keymap_showcase.jpg"),
    (PH_DIR / "04_universal_apps_offline_16x9.jpg", ASSETS_DIR / "apps_showcase.jpg"),
    (ROOT / "rachayitha_logo.png", ASSETS_DIR / "rachayitha_logo.png"),
]

for src, dest in mappings:
    if src.exists():
        shutil.copy2(src, dest)
        print(f"Copied {src.name} -> {dest.name}")
    else:
        print(f"Warning: {src} not found")

print("Assets setup completed successfully!")
