import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "te_lm.json")
CAND_PATH = os.path.join(ROOT, "data", "casual_candidates.json")
REPORT_PATH = os.path.join(ROOT, "scripts", "lm_report.txt")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    lm = json.load(f)

unigrams = lm.get("unigrams", {})
bigrams = lm.get("bigrams", {})

with open(CAND_PATH, "r", encoding="utf-8") as f:
    cands = json.load(f)

words_to_check = [
    "అక్కడ", "అక్కడా", "ఎవరు", "ఎవరూ", "లేరు", "ఉన్నారు",
    "ఎక్కడ", "ఎక్కడా", "లేదు", "ఉన్నాడు", "వస్తున్నా", "వస్తున్న",
    "అంటే", "అంటె", "గా", "గ", "వెళ్ళాక", "వెళ్లాక", "ఔను", "అవును"
]

pairs_to_check = [
    "అక్కడ_ఎవరూ", "అక్కడ_ఎవరు", "అక్కడా_ఎవరూ", "అక్కడా_ఎవరు",
    "ఎవరూ_లేరు", "ఎవరు_లేరు", "ఎవరు_ఉన్నారు", "ఎవరూ_ఉన్నారు",
    "ఎక్కడా_లేదు", "ఎక్కడ_లేదు", "ఎక్కడ_ఉన్నాడు", "ఎక్కడా_ఉన్నాడు",
]

keys_to_check = ["evaru", "akkada", "ekkada", "ante", "ga", "vastunna", "vellaka", "avunu"]

lines = []
lines.append("=== UNIGRAMS ===")
for w in words_to_check:
    lines.append(f"'{w}': {unigrams.get(w, 'NOT IN UNIGRAMS')}")

lines.append("\n=== BIGRAMS ===")
for p in pairs_to_check:
    lines.append(f"'{p}': {bigrams.get(p, 'NOT IN BIGRAMS')}")

lines.append("\n=== CANDIDATES IN casual_candidates.json ===")
for k in keys_to_check:
    lines.append(f"'{k}': {cands.get(k, 'NOT IN CANDIDATES')}")

report = "\n".join(lines)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

print("Report written to:", REPORT_PATH)
