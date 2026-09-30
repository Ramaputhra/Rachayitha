@echo off
chcp 65001 > nul
echo ======================================================================
echo   Rachayitha: Syncing Casual Typing Showcase Images to WebSite/assets
echo ======================================================================

set "SRC1=C:\Users\Sm!le\.gemini\antigravity-ide\brain\354ebab5-b49f-4582-9479-eb61f7011a5b\casual_typing_showcase_1790785205122.jpg"
set "SRC2=C:\Users\Sm!le\.gemini\antigravity-ide\brain\354ebab5-b49f-4582-9479-eb61f7011a5b\casual_vs_highkey_1790785260899.jpg"

if not exist "WebSite\assets" mkdir "WebSite\assets"
if not exist "product_hunt_assets" mkdir "product_hunt_assets"

copy /Y "%SRC1%" "WebSite\assets\casual_typing_showcase.jpg" > nul
copy /Y "%SRC2%" "WebSite\assets\casual_vs_highkey.jpg" > nul
copy /Y "%SRC1%" "product_hunt_assets\05_casual_typing_showcase_16x9.jpg" > nul
copy /Y "%SRC2%" "product_hunt_assets\06_casual_vs_highkey_16x9.jpg" > nul

echo [SUCCESS] Copied casual_typing_showcase.jpg -> WebSite\assets\
echo [SUCCESS] Copied casual_vs_highkey.jpg -> WebSite\assets\
echo.
echo You can now view WebSite\index.html in your browser!
pause
