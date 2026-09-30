@echo off
chcp 65001 > nul
echo Syncing data files to WebSite/data...
if not exist "WebSite\data" mkdir "WebSite\data"
copy /Y "data\casual_type_dict.json" "WebSite\data\"
copy /Y "data\te_top10k.json" "WebSite\data\"
copy /Y "data\typo_fixes.json" "WebSite\data\"
echo Done! Data files copied successfully.
pause
