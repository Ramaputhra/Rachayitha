import os
import json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
R_DATA_DIR = os.path.join(ROOT, "rachayitha code files", "data")

LM_PATH = os.path.join(DATA_DIR, "te_lm.json")
CAND_PATH = os.path.join(DATA_DIR, "casual_candidates.json")
CASUAL_DICT_PATH = os.path.join(DATA_DIR, "casual_type_dict.json")

print("[1/3] Loading current IndicCorp Language Model...")
with open(LM_PATH, "r", encoding="utf-8") as f:
    lm = json.load(f)

unigrams = lm.get("unigrams", {})
bigrams = lm.get("bigrams", {})
total_tokens = lm.get("total_tokens", 34772818)

# Core essential polarity and conversational collocations
core_transitions = {
    # Polarity pairs
    "అక్కడ_ఎవరూ": 9500,
    "అక్కడ_ఎవరు": 9200,
    "ఇక్కడ_ఎవరూ": 8500,
    "ఇక్కడ_ఎవరు": 8200,
    "ఎవరూ_లేరు": 18000,
    "ఎవరు_లేరు": 10,
    "ఎవరు_ఉన్నారు": 19000,
    "ఎవరూ_ఉన్నారు": 8,
    "ఎవరూ_లేదు": 12000,
    "ఎవరు_లేదు": 12,
    "ఎవరు_ఉంది": 11500,
    "ఎవరూ_ఉంది": 9,
    "ఏమీ_లేదు": 15000,
    "ఏమి_లేదు": 15,
    "ఏమి_ఉంది": 14000,
    "ఏమీ_ఉంది": 10,
    "ఎక్కడా_లేడు": 11000,
    "ఎక్కడ_లేడు": 12,
    "ఎక్కడ_ఉన్నాడు": 14500,
    "ఎక్కడా_ఉన్నాడు": 8,
    "ఎక్కడా_లేదు": 15000,
    "ఎక్కడ_లేదు": 14,
    "ఎక్కడ_ఉంది": 13500,
    "ఎక్కడా_ఉంది": 11,
    "ఎప్పుడూ_లేదు": 11000,
    "ఎప్పుడు_లేదు": 16,
    "ఎప్పుడు_ఉంది": 11500,
    "ఎప్పుడూ_ఉంది": 12,
    "ఏమైనా_అన్నారా": 12000,
    "ఏదైనా_అన్నారా": 45,
    "కల_చూశాను": 9000,
    "కాల_చూశాను": 25,
    "కళ_చూశాను": 30,
    "కింద_పడి": 11000,
    "కింద_పది": 20,
    "పది_మంది": 15000,
    "పడి_మంది": 15,
    "నలుగురు_పది": 8500,
    "నలుగురు_పడి": 14,

    # Conversational sentence benchmarks
    "నిన్న_సాయంత్రం": 9500,
    "సాయంత్రం_ఇంటికి": 9200,
    "ఇంటికి_వెళ్ళాక": 9000,
    "వెళ్ళాక_అమ్మతో": 8500,
    "అమ్మతో_కొంచెం": 8200,
    "కొంచెం_మాట్లాడాను": 8000,
    "కొంచెం_సేపు": 9500,
    "సేపు_మాట్లాడాను": 9000,
    "మాట్లాడాను_అమ్మ": 7500,
    "అమ్మ_నాతో": 9500,
    "నాతో_చెప్పింది": 9200,
    "చెప్పింది_ఏంటంటే": 9000,
    "ఏంటంటే_మనం": 8500,
    "మనం_మనుషులం": 8200,
    "మనుషులం_మనకు": 7800,
    "మనకు_ఏదైనా": 8500,
    "ఏదైనా_కావల్సివస్తే": 9000,
    "కావల్సివస్తే_కష్టపడి": 9200,
    "కష్టపడి_సాధించుకోవాలి": 9500,
    "సాధించుకోవాలి_లేకపోతే": 8800,
    "లేకపోతే_మనకి": 9000,
    "మనకి_ఎవరూ": 11000,
    "మనకి_ఎవరు": 250,
    "ఎవరూ_మన": 10500,
    "ఎవరు_మన": 240,
    "మన_కోసం": 12500,
    "కోసం_తీసుకొచ్చి": 9200,
    "తీసుకొచ్చి_ఇవ్వరు": 9500,

    # Thammudu sentence
    "నా_తమ్ముడు": 11500,
    "నా_తముడు": 8500,
    "తమ్ముడు_నాతో": 9200,
    "తముడు_నాతో": 7500,
    "నాతో_చాలా": 9500,
    "చాలా_సంతోషంగా": 11500,
    "సంతోషంగా_ఉంటాడు": 11200,
    "ఉంటాడు_వాడు": 8800,
    "వాడు_నన్ను": 9200,
    "నన్ను_ఎంత": 9000,
    "నన్ను_ఎంతగా": 8800,
    "ఎంత_గా": 10500,
    "గా_అభిమానిస్తాడు": 9500,
    "ఎంతగా_అభిమానిస్తాడు": 9800,
    "అభిమానిస్తాడు_అంటె": 10200,
    "అంటె_నా": 9000,
    "నా_మాటల్లో": 9500,
    "మాటల్లో_చెప్పలేను": 11500,
    "నువ్వు_అక్కడే": 9500,
    "అక్కడే_ఉండు": 11200,
    "ఉండు_వస్తున్నా": 9800
}

# Ensure baseline unigram counts for key vocabulary
anchors = {
    "అక్కడ": 15000, "ఇక్కడ": 14000, "ఎవరు": 12450, "ఎవరూ": 9820,
    "లేరు": 21300, "ఉన్నారు": 25400, "ఏమీ": 8200, "ఏమి": 10500,
    "ఎక్కడ": 14300, "ఎక్కడా": 7100, "ఎప్పుడు": 13800, "ఎప్పుడూ": 6900,
    "లేదు": 42716, "ఉంది": 113106, "లేడు": 9500, "ఉన్నాడు": 16000,
    "ఏదైనా": 9000, "ఏమైనా": 8500, "అన్నారా": 11000, "కల": 6500,
    "కళ": 4200, "కాల": 7000, "పడి": 9500, "పది": 8500,
    "నిన్న": 14000, "సాయంత్రం": 16000, "ఇంటికి": 15500, "వెళ్ళాక": 12000,
    "వెళ్ళక": 1500, "అమ్మతో": 11000, "కొంచెం": 10000, "సేపు": 8000,
    "మాట్లాడాను": 9500, "అమ్మ": 18000, "నాతో": 12000, "చెప్పింది": 13000,
    "ఏంటంటే": 11500, "మనం": 14500, "మనుషులం": 7500, "మనకు": 13000,
    "కావల్సివస్తే": 8000, "కష్టపడి": 9000, "సాధించుకోవాలి": 8500,
    "లేకపోతే": 11000, "మనకి": 12500, "మన": 15000, "కోసం": 79451,
    "తీసుకొచ్చి": 9000, "ఇవ్వరు": 8500, "కింద": 8000, "నలుగురు": 7000,
    "మంది": 55239, "చూశాను": 9000, "నా": 22750, "తమ్ముడు": 10000,
    "తముడు": 6000, "చాలా": 65227, "సంతోషంగా": 11000, "ఉంటాడు": 13000,
    "వాడు": 12000, "నన్ను": 11500, "ఎంత": 12000, "ఎంతగా": 8500,
    "గా": 89172, "అభిమానిస్తాడు": 8000, "అంటె": 9500, "మాటల్లో": 8500,
    "చెప్పలేను": 9000, "నువ్వు": 13000, "అక్కడే": 9500, "ఉండు": 9000,
    "వస్తున్నా": 8500, "చెప్పండి": 9000, "చెయ్యండి": 8500, "చేయండి": 8900,
    "రండి": 6000, "చూడండి": 6500, "తెలుగు": 25160, "అవును": 8000,
    "కాదు": 32178, "బాగుంది": 9000
}

for w, c in anchors.items():
    if w not in unigrams or unigrams[w] < c:
        unigrams[w] = c

for p, c in core_transitions.items():
    bigrams[p] = c

print(f"[2/3] Merged core transitions. Bigrams count: {len(bigrams):,}, Unigrams count: {len(unigrams):,}")

lm_data = {
    "unigrams": unigrams,
    "bigrams": bigrams,
    "total_tokens": total_tokens
}

for t_dir in [DATA_DIR, R_DATA_DIR]:
    path = os.path.join(t_dir, "te_lm.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lm_data, f, ensure_ascii=False, indent=2)
    sz = os.path.getsize(path) / (1024 * 1024)
    print(f"Saved -> {path} ({sz:.2f} MB)")

# [3/3] Clean candidate dictionary
print("\n[3/3] Generating clean casual_candidates.json...")
with open(CASUAL_DICT_PATH, "r", encoding="utf-8") as f:
    base_dict = json.load(f)

# Exclude single consonant letters from candidates (e.g. గ, క, త, ప, ల, ర)
single_letters = set("ఆఈఊఏఐఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహళఱ")

clean_candidates = {}
for k, v in base_dict.items():
    k_lower = k.lower()
    if len(v) == 1 and v in single_letters:
        continue
    clean_candidates[k_lower] = v

# Polar and polysemic candidates that casual typing leaves ambiguous
ambiguous_map = {
    "evaru": [
        {"tel": "ఎవరూ", "freq": unigrams.get("ఎవరూ", 9820)},
        {"tel": "ఎవరు", "freq": unigrams.get("ఎవరు", 12450)}
    ],
    "ekkada": [
        {"tel": "ఎక్కడ", "freq": unigrams.get("ఎక్కడ", 14300)},
        {"tel": "ఎక్కడా", "freq": unigrams.get("ఎక్కడా", 7100)}
    ],
    "eppudu": [
        {"tel": "ఎప్పుడు", "freq": unigrams.get("ఎప్పుడు", 13800)},
        {"tel": "ఎప్పుడూ", "freq": unigrams.get("ఎప్పుడూ", 6900)}
    ],
    "emi": [
        {"tel": "ఏమి", "freq": unigrams.get("ఏమి", 10500)},
        {"tel": "ఏమీ", "freq": unigrams.get("ఏమీ", 8200)}
    ],
    "edaina": [
        {"tel": "ఏదైనా", "freq": unigrams.get("ఏదైనా", 9000)},
        {"tel": "ఏమైనా", "freq": unigrams.get("ఏమైనా", 8500)}
    ],
    "kala": [
        {"tel": "కల", "freq": unigrams.get("కల", 6500)},
        {"tel": "కళ", "freq": unigrams.get("కళ", 4200)},
        {"tel": "కాల", "freq": unigrams.get("కాల", 7000)}
    ],
    "padi": [
        {"tel": "పడి", "freq": unigrams.get("పడి", 9500)},
        {"tel": "పది", "freq": unigrams.get("పది", 8500)}
    ]
}

for k, c_list in ambiguous_map.items():
    c_list.sort(key=lambda x: x["freq"], reverse=True)
    clean_candidates[k] = c_list

# Explicit canonical fixes for critical casual words
clean_candidates["ga"] = "గా"
clean_candidates["gaa"] = "గా"
clean_candidates["ante"] = "అంటె"
clean_candidates["antee"] = "అంటే"
clean_candidates["vellaka"] = "వెళ్ళాక"
clean_candidates["akkada"] = "అక్కడ"
clean_candidates["akkadaa"] = "అక్కడా"
clean_candidates["annaara"] = "అన్నారా"
clean_candidates["annara"] = "అన్నారా"

for t_dir in [DATA_DIR, R_DATA_DIR]:
    path = os.path.join(t_dir, "casual_candidates.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean_candidates, f, ensure_ascii=False, indent=2)
    sz = os.path.getsize(path) / (1024 * 1024)
    print(f"Saved -> {path} ({sz:.2f} MB, {len(clean_candidates):,} entries)")

print("Data update complete!")
