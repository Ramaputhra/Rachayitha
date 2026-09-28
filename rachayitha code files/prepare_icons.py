import os
import shutil
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_LOGO = os.path.join(PARENT_DIR, "rachayitha_logo.png")
DEST_LOGO = os.path.join(SCRIPT_DIR, "rachayitha_logo.png")
ICO_PATH = os.path.join(SCRIPT_DIR, "icon.ico")
PNG_PATH = os.path.join(SCRIPT_DIR, "icon.png")

def main():
    if os.path.exists(SOURCE_LOGO):
        shutil.copy2(SOURCE_LOGO, DEST_LOGO)
        print(f"Copied {SOURCE_LOGO} -> {DEST_LOGO}")
    else:
        print(f"Source logo not found at {SOURCE_LOGO}")
        return

    with Image.open(DEST_LOGO) as img:
        img = img.convert("RGBA")
        # Save standard PNG
        img.save(PNG_PATH)
        # Save multi-resolution ICO for Windows
        icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ICO_PATH, format="ICO", sizes=icon_sizes)
        print(f"Generated {ICO_PATH} and {PNG_PATH}")

if __name__ == "__main__":
    main()
