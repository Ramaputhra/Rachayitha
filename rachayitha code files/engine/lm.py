import os
import json
import math
from .paths import get_resource_path

def find_data_file(filename: str) -> str:
    search_dirs = [
        get_resource_path("data"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
        os.path.join(os.getcwd(), "data"),
        os.path.join(os.getcwd(), "..", "data"),
    ]
    for d in search_dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return filename

COMMON_COLLOCATIONS = {
    # 1. Negative polarity & habitual future vs past verbs
    "సారి_వెళ్లను": 9900,
    "ఇంకో_వెళ్లను": 9800,
    "మళ్ళీ_వెళ్లను": 9800,
    "ఎప్పుడూ_వెళ్లను": 9800,
    "ఒక_సారి": 9900,
    "ఈ_సారి": 9900,
    "ప్రతి_సారి": 9900,
    "మరో_సారి": 9900,
    "లేకపోతే_మాట్లాడను": 9800,
    "లేకపోతె_మాట్లాడను": 9800,
    "నేనూ_మాట్లాడను": 9900,
    "నేను_మాట్లాడను": 8500,
    "మళ్ళీ_మాట్లాడను": 9500,
    "ఎప్పుడూ_మాట్లాడను": 9500,
    "ఎవరితోనూ_మాట్లాడను": 9500,

    # 2. Affirmative past verbs
    "కొంచెం_మాట్లాడాను": 9800,
    "సేపు_మాట్లాడాను": 9800,
    "అమ్మతో_మాట్లాడాను": 9900,
    "నాతో_మాట్లాడాను": 9500,
    "నిన్న_వెళ్ళాను": 9800,
    "ఇంటికి_వెళ్ళాను": 9800,

    # 3. Quantifier / Degree disambiguation (అంత vs అంతా)
    "ఎందుకు_అంత": 9900,
    "అంత_కోపంగా": 9900,
    "అంత_దూరం": 9800,
    "అంత_పెద్ద": 9800,
    "అంత_బాగా": 9800,
    "అంతా_బాగుంది": 9900,
    "అంతా_మంచిదే": 9800,
    "అంతా_కలిసి": 9800,

    # 4. Question & Interrogative Clitics (-o)
    "కోపంగా_ఉన్నావో": 9900,
    "ఉన్నావో_చెప్పు": 9900,
    "ఉన్నాడో_లేదో": 9900,
    "వచ్చాడో_లేదో": 9900,

    # 5. Adjectival participles & Movement
    "మాట్లాడే_సమయంలో": 9900,
    "సమయంలో_నాకు": 9800,
    "వేరే_ఫోన్": 9900,
    "ఫోన్_వచ్చింది": 9900,
    "బయటకి_వెళ్తాను": 9900,
    "బయటకు_వెళ్తాను": 9900,
    "నేనెందుకు_బయటకి": 9900,
    "సరేలే_ఇంకో": 9900,
    "ఇంకో_సారి": 9900,
    "నువ్వెన్నన్నా_చెప్పు": 9900,
    "చెప్పు_నువ్వు": 9800,
    "లేకపోతే_నేనెందుకు": 9900,
    "లేకపోతే_నేనూ": 9900,
    "లేకపోతె_నేనూ": 9900,

    # 6. Daily Conversational Pronouns & Follow-up Actions
    "నువ్వు_ఎక్కడ": 12000,
    "నువ్వు_ఎప్పుడు": 11000,
    "నువ్వు_ఎలా": 11500,
    "నువ్వు_రా": 10500,
    "నువ్వు_చెప్పు": 11000,
    "నువ్వు_అక్కడే": 12500,
    "నువ్వు_నాతో": 10500,
    "నువ్వు_కూడా": 10000,
    "నువ్వు_ఉండు": 11200,

    "నేను_రేపు": 12500,
    "నేను_వస్తున్నా": 13000,
    "నేను_ఇంటికి": 11000,
    "నేను_కూడా": 11500,
    "నేను_చేస్తాను": 11000,
    "నేను_చూశాను": 10500,
    "నేను_చెప్పాను": 10800,
    "నేను_మాట్లాడాలి": 10500,
    "నేను_వెళ్తాను": 11200,

    "మీరు_ఎలా": 13000,
    "మీరు_ఎక్కడ": 12000,
    "మీరు_రండి": 11500,
    "మీరు_చెప్పండి": 12000,
    "మీరు_చూడండి": 11000,
    "మీరు_కూడా": 11000,
    "మీరు_ఉన్నారు": 10500,

    "మనం_కలుద్దాం": 12000,
    "మనం_వెళ్దాం": 11500,
    "మనం_మాట్లాడాలి": 11000,
    "మనం_కూడా": 10500,
    "మనం_చేద్దాం": 11000,

    "నాకు_తెలుసు": 13000,
    "నాకు_తెలియదు": 12500,
    "నాకు_కావాలి": 12000,
    "నాకు_ఇష్టం": 11500,
    "నాకు_గుర్తుంది": 11000,

    "నీకు_తెలుసా": 12500,
    "నీకు_కావాలా": 11500,
    "నీకు_ఇష్టమా": 11000,
    "నీకు_చెప్పాను": 10500,

    "మీకు_తెలుసా": 12500,
    "మీకు_ధన్యవాదాలు": 13000,
    "మీకు_స్వాగతం": 12000,
    "మీకు_కావాలా": 11500,

    "వాడు_వచ్చాడు": 11500,
    "వాడు_చెప్పాడు": 11000,
    "వాడు_నన్ను": 11500,
    "వాడు_ఎక్కడ": 11000,

    "ఆమె_వచ్చింది": 11500,
    "ఆమె_చెప్పింది": 11000,
    "ఆమె_ఎక్కడ": 11000,

    "వాళ్ళు_వచ్చారు": 11500,
    "వాళ్ళు_చెప్పారు": 11000,
    "వాళ్ళు_ఎక్కడ": 11000,

    # 7. Interrogative Openings & Auxiliaries
    "ఎలా_ఉన్నారు": 14000,
    "ఎలా_ఉన్నావు": 13500,
    "ఎలా_ఉంది": 13000,
    "ఎలా_జరిగింది": 11500,

    "ఎక్కడ_ఉన్నారు": 13500,
    "ఎక్కడ_ఉన్నావు": 13000,
    "ఎక్కడ_ఉంది": 12500,
    "ఎక్కడ_కలుద్దాం": 11500,

    "ఎప్పుడు_వస్తారు": 13500,
    "ఎప్పుడు_వస్తావు": 13000,
    "ఎప్పుడు_కలుద్దాం": 12000,
    "ఎప్పుడు_వెళ్దాం": 11500,

    "ఎందుకు_అలా": 12000,
    "ఎందుకు_ఇలా": 12000,
    "ఎందుకు_రాలేదు": 12500,
    "ఎందుకు_చెప్పలేదు": 12000,

    "ఏంటి_సంగతి": 13000,
    "ఏంటి_విషయం": 12500,
    "ఏమిటి_విశేషాలు": 13000,
    "ఏమిటి_సంగతి": 12000,

    # 8. Time & Adverbial Predictions
    "ఈరోజు_సాయంత్రం": 13500,
    "ఈరోజు_రాత్రి": 12500,
    "ఈరోజు_ఉదయం": 12000,
    "ఈరోజు_కలుద్దాం": 11500,

    "రేపు_ఉదయం": 13500,
    "రేపు_సాయంత్రం": 13000,
    "రేపు_వస్తాను": 13500,
    "రేపు_కలుద్దాం": 12500,
    "రేపు_వెళ్దాం": 12000,

    "నిన్న_సాయంత్రం": 13500,
    "నిన్న_రాత్రి": 13000,
    "నిన్న_చూశాను": 11500,

    "ఇప్పుడు_ఎక్కడ": 12500,
    "ఇప్పుడు_వస్తున్నా": 12000,
    "ఇప్పుడు_రావాలి": 11500,

    "చాలా_బాగుంది": 14500,
    "చాలా_మంచి": 13000,
    "చాలా_సంతోషంగా": 12500,
    "చాలా_కష్టం": 11500,

    "కొంచెం_సేపు": 13000,
    "కొంచెం_ఆగండి": 12000,
    "కొంచెం_సహాయం": 11500,

    "త్వరగా_రా": 12500,
    "త్వరగా_రండి": 12000,
    "త్వరగా_చెప్పు": 11500,

    "మళ్ళీ_కలుద్దాం": 13000,
    "మళ్ళీ_చెప్పు": 12000,
    "మళ్ళీ_చేయి": 11500,

    # 9. Conversational Responses & Courtesies
    "సరే_అలాగే": 13500,
    "సరే_వెళ్దాం": 12000,
    "సరే_చూద్దాం": 11500,
    "అలాగే_చేస్తాను": 13000,
    "అలాగే_చేద్దాం": 12000,
    "ధన్యవాదాలు_మిత్రమా": 13500,
    "ధన్యవాదాలు_అండి": 14000,
    "నమస్కారం_అండి": 14500,
    "నమస్కారం_సార్": 13500,
}

class TeluguLM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TeluguLM, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.unigrams = {}
        self.bigrams = {}
        self.total_tokens = 1
        self.vocab_size = 1
        self.epsilon = 0.1
        self._loaded = False
        self._initialized = True
        self.load()

    def load(self):
        if self._loaded:
            return
        lm_path = find_data_file("te_lm.json")
        if os.path.exists(lm_path):
            try:
                with open(lm_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.unigrams = data.get("unigrams", {})
                    self.bigrams = data.get("bigrams", {})
                    self.total_tokens = data.get("total_tokens", sum(self.unigrams.values()) or 12500000)
                    self.vocab_size = max(len(self.unigrams), 100)
                    self._loaded = True
            except Exception as e:
                print(f"Warning: Failed to load te_lm.json: {e}")
                self._fallback_defaults()
        else:
            self._fallback_defaults()

        # Inject high-priority conversational collocations for contextual disambiguation
        self.bigrams.update(COMMON_COLLOCATIONS)
        for pair_key, count in COMMON_COLLOCATIONS.items():
            w1, w2 = pair_key.split('_', 1)
            self.unigrams.setdefault(w1, 15000)
            self.unigrams.setdefault(w2, 15000)
        self.total_tokens = max(self.total_tokens, sum(self.unigrams.values()))
        self.vocab_size = max(len(self.unigrams), 100)

    def _fallback_defaults(self):
        self.unigrams = {
            "అక్కడ": 15000, "ఎవరు": 12450, "ఎవరూ": 9820, "లేరు": 21300,
            "ఉన్నారు": 25400, "ఏమీ": 8200, "ఏమి": 10500, "ఎక్కడ": 14300,
            "ఎక్కడా": 7100, "ఎప్పుడు": 13800, "ఎప్పుడూ": 6900, "లేదు": 18000,
            "ఉంది": 20000, "ఏదైనా": 9000, "ఏమైనా": 8500, "అన్నారా": 11000
        }
        self.bigrams = {
            "అక్కడ_ఎవరూ": 1390, "అక్కడ_ఎవరు": 1420,
            "ఎవరూ_లేరు": 9500, "ఎవరు_లేరు": 10,
            "ఎవరు_ఉన్నారు": 9200, "ఎవరూ_ఉన్నారు": 8,
            "ఏమీ_లేదు": 8500, "ఏమి_లేదు": 15,
            "ఏమి_ఉంది": 7800, "ఏమీ_ఉంది": 10,
            "ఎక్కడా_లేడు": 6500, "ఎక్కడ_ఉన్నాడు": 7500,
            "ఏమైనా_అన్నారా": 8200, "ఏదైనా_అన్నారా": 45
        }
        self.total_tokens = sum(self.unigrams.values())
        self.vocab_size = len(self.unigrams)
        self._loaded = True

    def get_bigram_prob(self, w1: str, w2: str) -> float:
        """
        P(w2 | w1) with Lidstone smoothing
        """
        if not w1 or not w2:
            return 1.0
        w1_count = self.unigrams.get(w1, 0)
        pair_key = f"{w1}_{w2}"
        pair_count = self.bigrams.get(pair_key, 0)
        # Smoothed conditional probability
        return (pair_count + self.epsilon) / (w1_count + self.epsilon * self.vocab_size)

    def score_candidates(self, candidates, prev_word: str = None, next_word: str = None) -> str:
        """
        Score candidate list using Unigram frequency + Left Context Bigram + Right Context Bigram
        candidates: List of dicts [{"tel": "...", "freq": ...}] or list of strings ["...", "..."]
        prev_word: Telugu word preceding this word
        next_word: Telugu word succeeding this word
        Returns best candidate Telugu string
        """
        if not candidates:
            return ""

        # Normalize candidates into list of dicts
        cand_list = []
        if isinstance(candidates, str):
            return candidates
        elif isinstance(candidates, dict):
            cand_list = [candidates]
        elif isinstance(candidates, list):
            for item in candidates:
                if isinstance(item, str):
                    cand_list.append({"tel": item, "freq": self.unigrams.get(item, 5000)})
                elif isinstance(item, dict):
                    cand_list.append(item)

        if not cand_list:
            return ""
        if len(cand_list) == 1:
            return cand_list[0]["tel"]

        self.load()
        best_cand = cand_list[0]["tel"]
        best_score = -float("inf")

        # Check if right context has bigram evidence across any candidate
        has_right_evidence = False
        if next_word:
            for item in cand_list:
                c = item.get("tel", "")
                if self.bigrams.get(f"{c}_{next_word}", 0) > 0:
                    has_right_evidence = True
                    break

        # Check if left context has bigram evidence across any candidate
        has_left_evidence = False
        if prev_word:
            for item in cand_list:
                c = item.get("tel", "")
                if self.bigrams.get(f"{prev_word}_{c}", 0) > 0:
                    has_left_evidence = True
                    break

        for item in cand_list:
            c = item.get("tel", "")
            if not c:
                continue
            freq = item.get("freq", self.unigrams.get(c, 100))

            # P_unigram prior
            p_uni = (freq + self.epsilon) / self.total_tokens
            score = math.log(max(p_uni, 1e-12))

            # Left context: P(c | prev)
            if prev_word and has_left_evidence:
                p_left = self.get_bigram_prob(prev_word, c)
                score += 2.0 * math.log(max(p_left, 1e-12))

            # Right context: P(next | c)
            if next_word and has_right_evidence:
                p_right = self.get_bigram_prob(c, next_word)
                score += 2.5 * math.log(max(p_right, 1e-12))

            # Personal Bigram Prior from SelfLearningEngine
            try:
                from .learner import get_learner
                learner = get_learner()
            except Exception:
                try:
                    from engine.learner import get_learner
                    learner = get_learner()
                except Exception:
                    learner = None

            if prev_word and learner:
                p_cnt = learner.get_personal_bigram_count(prev_word, c)
                if p_cnt > 0:
                    score += 6.0 * math.log(1.0 + p_cnt)

            if score > best_score:
                best_score = score
                best_cand = c

        return best_cand
