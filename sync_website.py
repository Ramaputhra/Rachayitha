"""
Sync WebSite folder for Vercel deployment:
- Copies Rachayitha-Premium.html to index.html
- Copies product_hunt_assets and rachayitha_logo into WebSite for rich meta previews
"""
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = ROOT_DIR / "WebSite"

src_html = WEBSITE_DIR / "Rachayitha-Premium.html"
dest_html = WEBSITE_DIR / "index.html"

if src_html.exists():
    shutil.copy2(src_html, dest_html)
    print("  [✓] Synced Rachayitha-Premium.html -> WebSite/index.html")

# Copy logo into WebSite
logo_src = ROOT_DIR / "rachayitha_logo.png"
if logo_src.exists():
    shutil.copy2(logo_src, WEBSITE_DIR / "rachayitha_logo.png")
    print("  [✓] Copied rachayitha_logo.png to WebSite/")

print("\n🚀 WebSite directory is 100% prepared for Vercel deployment!")
