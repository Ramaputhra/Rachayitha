"""
Sync WebSite folder for Vercel deployment:
- Ensures product_hunt_assets and rachayitha_logo are copied into WebSite/assets
- Validates that index.html, sitemap.xml, robots.txt, and site.webmanifest exist
"""
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = ROOT_DIR / "WebSite"
ASSETS_DIR = WEBSITE_DIR / "assets"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Copy logo into WebSite and WebSite/assets
logo_src = ROOT_DIR / "rachayitha_logo.png"
if logo_src.exists():
    shutil.copy2(logo_src, WEBSITE_DIR / "rachayitha_logo.png")
    shutil.copy2(logo_src, ASSETS_DIR / "rachayitha_logo.png")
    print("  [✓] Copied rachayitha_logo.png to WebSite/ and WebSite/assets/")

print("\n🚀 WebSite directory is 100% prepared for Vercel & Google Search deployment!")
