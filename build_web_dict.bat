@echo off
chcp 65001 > nul
echo ======================================================================
echo   Rachayitha Web: Compiling 58,421-Word Casual Dictionary into JS
echo ======================================================================
python -c "import json, os; p_in = r'data\casual_type_dict.json'; p_out = r'WebSite\casual_dict_data.js'; top_path = r'data\te_top10k.json'; top10k = json.load(open(top_path, encoding='utf-8')) if os.path.exists(top_path) else {}; raw = json.load(open(p_in, encoding='utf-8')); final_d = {}; [final_d.setdefault(k.lower(), v) for k, v in raw.items()]; open(p_out, 'w', encoding='utf-8').write('window.RACHAYITHA_CASUAL_DICT = ' + json.dumps(final_d, ensure_ascii=False) + ';'); print(f'Successfully built {p_out} with {len(final_d)} words!')"
echo.
echo You can now refresh index.html in your browser!
pause
