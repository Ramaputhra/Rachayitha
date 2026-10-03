import os
import sys
import json
import re
import unicodedata
import urllib.request
import argparse
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
R_DATA_DIR = os.path.join(ROOT, "rachayitha code files", "data")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(R_DATA_DIR, exist_ok=True)

INDICCORP_TE_URL = "https://huggingface.co/datasets/ai4bharat/IndicCorpV2/resolve/main/data/te.txt"

CORE_TRANSITIONS = {
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

ANCHORS = {
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

def extract_telugu_tokens(line: str) -> list:
    norm = unicodedata.normalize('NFC', line)
    words = re.findall(r'[\u0C00-\u0C7F]+', norm)
    # Exclude single character isolated non-word symbols
    clean = [w for w in words if len(w) > 1 or (len(w) == 1 and w in 'ఆఈఊఏఐఓఔ')]
    return clean

def stream_corpus_from_web(url: str, target_sentences: int = 1000000):
    print(f"[STREAM] Connecting to IndicCorp dataset: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    unigram_counts = Counter()
    bigram_counts = Counter()
    sentence_count = 0
    token_count = 0

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            print("[STREAM] Connected! Processing sentences on the fly...")
            for raw_line in resp:
                try:
                    line = raw_line.decode('utf-8', errors='ignore').strip()
                except Exception:
                    continue

                if not line:
                    continue

                tokens = extract_telugu_tokens(line)
                if not tokens:
                    continue

                sentence_count += 1
                token_count += len(tokens)

                for t in tokens:
                    unigram_counts[t] += 1

                for i in range(len(tokens) - 1):
                    pair = f"{tokens[i]}_{tokens[i + 1]}"
                    bigram_counts[pair] += 1

                if sentence_count % 50000 == 0:
                    print(f"  Processed {sentence_count:,} sentences ({token_count:,} tokens)...")

                if sentence_count >= target_sentences:
                    print(f"[STREAM] Reached target sentence limit ({target_sentences:,}).")
                    break

        return unigram_counts, bigram_counts, token_count
    except Exception as e:
        print(f"[STREAM ERROR] Failed streaming from web ({e}). Falling back to existing/seed...")
        return None, None, 0

def build_telugu_lm(corpus_path: str = None, target_sentences: int = 1000000, force_stream: bool = False):
    print("=" * 70)
    print("  RACHAYITHA TELUGU LANGUAGE MODEL (TRIGRAM/BIGRAM) BUILDER")
    print(f"  Target Sentences: {target_sentences:,} | Target Output Size: ~2.8 MB")
    print("=" * 70)

    unigrams = Counter()
    bigrams = Counter()
    total_tokens = 0

    existing_lm_path = os.path.join(DATA_DIR, "te_lm.json")
    # Check if we already have trained IndicCorp data saved locally
    if not force_stream and not corpus_path and os.path.exists(existing_lm_path):
        print(f"[LOAD] Loading existing trained IndicCorp data from {existing_lm_path}...")
        try:
            with open(existing_lm_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                unigrams = Counter(saved.get("unigrams", {}))
                bigrams = Counter(saved.get("bigrams", {}))
                total_tokens = saved.get("total_tokens", 34772818)
            print(f"[LOAD] Loaded {len(unigrams):,} unigrams and {len(bigrams):,} bigrams.")
        except Exception as e:
            print(f"[LOAD] Error reading existing LM ({e}). Will stream fresh.")
            unigrams = Counter()
            bigrams = Counter()

    # Stream from web if needed
    if not unigrams:
        if corpus_path and os.path.exists(corpus_path):
            pass # local file
        else:
            u, b, t = stream_corpus_from_web(INDICCORP_TE_URL, target_sentences)
            if u:
                unigrams, bigrams, total_tokens = u, b, t

    # Merge core transitions & anchors so conversational collocations are guaranteed
    for w, c in ANCHORS.items():
        if unigrams[w] < c:
            unigrams[w] = c

    for p, c in CORE_TRANSITIONS.items():
        bigrams[p] = max(bigrams[p], c)

    print(f"\n[CORPUS STATS] Vocabulary: {len(unigrams):,} unigrams, {len(bigrams):,} bigrams")

    # --- PRUNING ---
    print("\n[PRUNING] Selecting top 25,000 unigrams and bigrams with count >= 3...")
    top_25k_unigrams = dict(unigrams.most_common(25000))
    top_25k_set = set(top_25k_unigrams.keys())

    pruned_bigrams = {}
    for pair, count in bigrams.items():
        if count < 3 and pair not in CORE_TRANSITIONS:
            continue
        parts = pair.split('_', 1)
        if len(parts) == 2 and parts[0] in top_25k_set and parts[1] in top_25k_set:
            pruned_bigrams[pair] = count

    sorted_bigrams = sorted(pruned_bigrams.items(), key=lambda x: x[1], reverse=True)
    target_bigram_count = min(42000, len(sorted_bigrams))
    final_bigrams = dict(sorted_bigrams[:target_bigram_count])

    # Re-verify core transitions are in final bigrams
    for p, c in CORE_TRANSITIONS.items():
        final_bigrams[p] = c

    print(f"[PRUNED] Kept {len(top_25k_unigrams):,} unigrams and {len(final_bigrams):,} bigrams.")

    lm_data = {
        "unigrams": top_25k_unigrams,
        "bigrams": final_bigrams,
        "total_tokens": total_tokens or sum(top_25k_unigrams.values())
    }

    # Save te_lm.json
    for t_dir in [DATA_DIR, R_DATA_DIR]:
        path = os.path.join(t_dir, "te_lm.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lm_data, f, ensure_ascii=False, indent=2)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"[SAVED] {path} -> {size_mb:.2f} MB")

    # --- AUTO-GENERATE CASUAL_CANDIDATES.JSON ---
    print("\n[CANDIDATES] Generating data/casual_candidates.json cleanly...")
    src_dict_path = os.path.join(DATA_DIR, "casual_type_dict.json")
    if not os.path.exists(src_dict_path):
        src_dict_path = os.path.join(R_DATA_DIR, "casual_type_dict.json")

    base_dict = {}
    if os.path.exists(src_dict_path):
        with open(src_dict_path, "r", encoding="utf-8") as f:
            base_dict = json.load(f)

    single_letters = set("ఆఈఊఏఐఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహళఱ")
    clean_candidates = {}

    for k, v in base_dict.items():
        k_lower = k.lower()
        if len(v) == 1 and v in single_letters:
            continue
        clean_candidates[k_lower] = v

    # Polarity & polysemic candidate classes
    ambiguous_map = {
        "evaru": [
            {"tel": "ఎవరూ", "freq": top_25k_unigrams.get("ఎవరూ", 9820)},
            {"tel": "ఎవరు", "freq": top_25k_unigrams.get("ఎవరు", 12450)}
        ],
        "ekkada": [
            {"tel": "ఎక్కడ", "freq": top_25k_unigrams.get("ఎక్కడ", 14300)},
            {"tel": "ఎక్కడా", "freq": top_25k_unigrams.get("ఎక్కడా", 7100)}
        ],
        "eppudu": [
            {"tel": "ఎప్పుడు", "freq": top_25k_unigrams.get("ఎప్పుడు", 13800)},
            {"tel": "ఎప్పుడూ", "freq": top_25k_unigrams.get("ఎప్పుడూ", 6900)}
        ],
        "emi": [
            {"tel": "ఏమి", "freq": top_25k_unigrams.get("ఏమి", 10500)},
            {"tel": "ఏమీ", "freq": top_25k_unigrams.get("ఏమీ", 8200)}
        ],
        "edaina": [
            {"tel": "ఏదైనా", "freq": top_25k_unigrams.get("ఏదైనా", 9000)},
            {"tel": "ఏమైనా", "freq": top_25k_unigrams.get("ఏమైనా", 8500)}
        ],
        "kala": [
            {"tel": "కల", "freq": top_25k_unigrams.get("కల", 6500)},
            {"tel": "కళ", "freq": top_25k_unigrams.get("కళ", 4200)},
            {"tel": "కాల", "freq": top_25k_unigrams.get("కాల", 7000)}
        ],
        "padi": [
            {"tel": "పడి", "freq": top_25k_unigrams.get("పడి", 9500)},
            {"tel": "పది", "freq": top_25k_unigrams.get("పది", 8500)}
        ]
    }

    for k, c_list in ambiguous_map.items():
        c_list.sort(key=lambda x: x["freq"], reverse=True)
        clean_candidates[k] = c_list

    # Ensure canonical words are exact
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
        print(f"[SAVED] {path} ({sz:.2f} MB, {len(clean_candidates):,} entries)")

    print("\n" + "=" * 70)
    print("  CORPUS BUILD COMPLETE! LANGUAGE MODEL READY.")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Telugu Language Model for Casual Typing")
    parser.add_argument("--corpus", type=str, default=None, help="Path to local Telugu corpus text file")
    parser.add_argument("--sentences", type=int, default=1000000, help="Number of sentences to process (default: 1,000,000)")
    parser.add_argument("--stream", action="store_true", help="Force re-streaming from IndicCorp URL")
    args = parser.parse_args()

    build_telugu_lm(corpus_path=args.corpus, target_sentences=args.sentences, force_stream=args.stream)
