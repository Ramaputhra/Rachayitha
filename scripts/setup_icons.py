import os
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ICONS_DIR = os.path.join(ROOT_DIR, "src-tauri", "icons")
os.makedirs(ICONS_DIR, exist_ok=True)

# Path to the generated icon
SOURCE_IMAGE = r"C:\Users\Sm!le\.gemini\antigravity-ide\brain\c576fa95-679d-4be7-895d-eb6b4cc03179\rachayitha_app_icon_1790598949803.jpg"

def generate_icons():
    if not os.path.exists(SOURCE_IMAGE):
        print(f"Source image not found: {SOURCE_IMAGE}")
        return

    with Image.open(SOURCE_IMAGE) as img:
        img = img.convert("RGBA")
        
        # 128x128
        img_128 = img.resize((128, 128), Image.Resampling.LANCZOS)
        img_128.save(os.path.join(ICONS_DIR, "128x128.png"))
        
        # 32x32
        img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
        img_32.save(os.path.join(ICONS_DIR, "32x32.png"))
        
        # Tray icon (32x32)
        img_32.save(os.path.join(ICONS_DIR, "tray.png"))

        # Windows .ico (multi-resolution)
        img.save(os.path.join(ICONS_DIR, "icon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
    print(f"Icons successfully generated in {ICONS_DIR}")

if __name__ == "__main__":
    generate_icons()
