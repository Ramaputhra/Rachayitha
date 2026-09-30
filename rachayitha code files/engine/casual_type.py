import os
import sys
import json
import re

# Resolve paths
try:
    from .paths import get_resource_path
except ImportError:
    def get_resource_path(rel_path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, rel_path)

# Fallback exact engine
try:
    from .transliterator import transliterate as exact_transliterate
except ImportError:
    try:
        from engine.transliterator import transliterate as exact_transliterate
    except ImportError:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if cur_dir not in sys.path:
            sys.path.insert(0, cur_dir)
        from transliterator import transliterate as exact_transliterate

def find_data_file(filename: str) -> str:
    """
    Search for a data file across standard locations (dev, bundle, root, appdata).
    """
    search_dirs = [
        get_resource_path("data"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data"),
        os.path.join(os.getcwd(), "data"),
        os.path.join(os.getcwd(), "..", "data"),
        r"c:\Users\Sm!le\Desktop\రచయిత\data",
        r"c:\Users\Sm!le\Desktop\రచయిత\rachayitha code files\data",
    ]
    for d in search_dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return filename

# Global dictionaries
CASUAL_DICT = {}
TYPO_FIXES = {}
SORTED_TYPO_FIXES = []
TOP10K_FREQ = {}
_INITIALIZED = False

# High-frequency conversational Telugu lexicon & priority overrides
CONVERSATIONAL_LEXICON = {
    # --- Sentential Benchmark Core ---
    "sayantram": "సాయంత్రం", "saayantram": "సాయంత్రం", "sayantraniki": "సాయంత్రానికి", "sayantramlo": "సాయంత్రంలో",
    "intiki": "ఇంటికి", "intike": "ఇంటికే", "intlo": "ఇంట్లో", "intloki": "ఇంట్లోకి",
    "vellaka": "వెళ్ళాక", "velladu": "వెళ్ళాడు", "vellindi": "వెళ్ళింది", "vellali": "వెళ్ళాలి",
    "velli": "వెళ్ళి", "vellina": "వెళ్ళిన", "vellaru": "వెళ్ళారు", "vellanu": "వెళ్ళాను",
    "vellipoyindi": "వెళ్ళిపోయింది", "vellipoyaru": "వెళ్ళిపోయారు", "vellipoyadu": "వెళ్ళిపోయాడు",
    "ammato": "అమ్మతో", "ammatho": "అమ్మతో", "naato": "నాతో", "naatho": "నాతో",
    "nannato": "నాన్నతో", "manato": "మనతో", "meeto": "మీతో", "meetoo": "మీతో",
    "matladanu": "మాట్లాడాను", "maatladanu": "మాట్లాడాను", "matladadu": "మాట్లాడాడు", "matladindi": "మాట్లాడింది",
    "matladaru": "మాట్లాడారు", "matladali": "మాట్లాడాలి", "matladadam": "మాట్లాడడం", "matladutunna": "మాట్లాడుతున్న",
    "matladutu": "మాట్లాడుతూ", "matladava": "మాట్లాడవా", "sepu": "సేపు", "konchem": "కొంచెం",
    "entante": "ఏంటంటే", "manushulam": "మనుషులం", "manushulu": "మనుషులు", "manushulaku": "మనుషులకు",
    "edaina": "ఏదైనా", "edainaa": "ఏదైనా", "endukante": "ఎందుకంటే", "andukante": "అందుకంటే",
    "kavalsivasthe": "కావల్సివస్తే", "kavalsivaste": "కావల్సివస్తే", "kavalsina": "కావల్సిన", "kavalasina": "కావలసిన",
    "kavali": "కావాలి", "kashtapadi": "కష్టపడి", "kashtapadali": "కష్టపడాలి", "kashtapaddanu": "కష్టపడ్డాను",
    "kashtapadadu": "కష్టపడ్డాడు", "kashtam": "కష్టం", "kashtalu": "కష్టాలు",
    "sadhinchukovali": "సాధించుకోవాలి", "sadhinchukovadam": "సాధించుకోవడం", "sadhinchali": "సాధించాలి",
    "sadhinchadu": "సాధించాడు", "sadhinchindi": "సాధించింది", "sadhincharu": "సాధించారు",
    "sadhinchanu": "సాధించాను", "sadhinchina": "సాధించిన",
    "teesukochchi": "తీసుకొచ్చి", "teesukochi": "తీసుకొచ్చి", "teesukochadu": "తీసుకొచ్చాడు",
    "teesukochindi": "తీసుకొచ్చింది", "teesukocharu": "తీసుకొచ్చారు", "teesukochanu": "తీసుకొచ్చాను",
    "teesukuni": "తీసుకుని", "teesukoni": "తీసుకొని", "teesukovali": "తీసుకోవాలి",
    "ivvaru": "ఇవ్వరు", "ivvadu": "ఇవ్వడు", "ivvandi": "ఇవ్వండి", "ivvali": "ఇవ్వాలి",
    "iccharu": "ఇచ్చారు", "icchadu": "ఇచ్చాడు", "lekapote": "లేకపోతే", "lekapothe": "లేకపోతే",
    "manaki": "మనకి", "evaru": "ఎవరూ", "evaruu": "ఎవరూ", "pettukochchi": "పెట్టుకొచ్చి",
    "chesukovali": "చేసుకోవాలి", "chusukovali": "చూసుకోవాలి", "telusukovali": "తెలుసుకోవాలి",
    "vachchi": "వచ్చి", "vachi": "వచ్చి", "chala": "చాలా", "chaala": "చాలా",
    "appudu": "అప్పుడు", "eppudu": "ఎప్పుడు", "ippudu": "ఇప్పుడు", "kosam": "కోసం", "mana": "మన",

    # --- Pronouns & Demonstratives ---
    "nenu": "నేను", "neenu": "నేను", "naa": "నా", "naaku": "నాకు", "nannu": "నన్ను",
    "nuvvu": "నువ్వు", "nuvu": "నువ్వు", "nee": "నీ", "neeku": "నీకు", "ninnu": "నిన్ను",
    "meeru": "మీరు", "meeruu": "మీరు", "mee": "మీ", "meeku": "మీకు", "mimmalni": "మిమ్మల్ని",
    "memu": "మేము", "maaku": "మాకు",
    "manam": "మనం", "manamu": "మనము", "manaku": "మనకు", "manalni": "మనల్ని",
    "vaaru": "వారు", "varu": "వారు", "vaallu": "వాళ్ళు", "vallu": "వాళ్ళు", "vaallaki": "వాళ్ళకి",
    "atanu": "అతను", "atadu": "అతడు", "ataniki": "అతనికి", "atanni": "అతన్ని",
    "aame": "ఆమె", "aameku": "ఆమెకు", "aamenu": "ఆమెను",
    "idi": "ఇది", "deeni": "దీని", "deeniki": "దీనికి", "deentlo": "దీంట్లో",
    "adi": "అది", "daani": "దాని", "daaniki": "దానికి", "daantlo": "దాంట్లో",
    "ivi": "ఇవి", "veeti": "వీటి", "veetiki": "వీటికి",
    "avi": "అవి", "vaati": "వాటి", "vaatiki": "వాటికి",

    # --- Time & Calendar Adverbs ---
    "eroju": "ఈరోజు", "eeroju": "ఈరోజు", "repu": "రేపు", "ninna": "నిన్న", "monna": "మొన్న",
    "ellundi": "ఎల్లుండి", "ippude": "ఇప్పుడే", "eppudo": "ఎప్పుడో", "appude": "అప్పుడే",
    "roju": "రోజు", "roojuu": "రోజు", "rojulu": "రోజులు", "samvatsaram": "సంవత్సరం",
    "nela": "నెల", "vaaram": "వారం", "udayam": "ఉదయం", "madhyahnam": "మధ్యాహ్నం",
    "raatri": "రాత్రి", "shubharatri": "శుభరాత్రి", "malli": "మళ్ళీ", "mallee": "మళ్ళీ",
    "tvaraga": "త్వరగా", "mundu": "ముందు", "munduku": "ముందుకు", "venuka": "వెనుక", "venakki": "వెనక్కి",

    # --- Question Words (ప్రశ్నార్థకాలు) ---
    "ela": "ఎలా", "elaa": "ఎలా", "ekkada": "ఎక్కడ", "ekkadaa": "ఎక్కడ",
    "akkada": "అక్కడ", "ikkada": "ఇక్కడ", "enduku": "ఎందుకు", "anduku": "అందుకు",
    "emiti": "ఏమిటి", "enti": "ఏంటి", "em": "ఏం", "eedi": "ఏది", "evaru": "ఎవరు",
    "entha": "ఎంత", "enni": "ఎన్ని",

    # --- Affirmations & Negations ---
    "avunu": "అవును", "avnu": "అవును", "kadu": "కాదు", "kaadu": "కాదు",
    "ledu": "లేదు", "ledhu": "లేదు", "laedu": "లేదు", "undi": "ఉంది", "undhi": "ఉంది",
    "unnaru": "ఉన్నారు", "unnanu": "ఉన్నాను", "unnadu": "ఉన్నాడు", "unnadi": "ఉన్నది", "unnamu": "ఉన్నాము", "unnam": "ఉన్నాం", "unnavu": "ఉన్నావు", "unnara": "ఉన్నారా",
    "bagundi": "బాగుంది", "bagundhi": "బాగుంది", "baga": "బాగా", "baaga": "బాగా",
    "nijam": "నిజం", "abaddham": "అబద్ధం", "sare": "సరే", "alage": "అలాగే",

    # --- Common Verbs (Inflected Conversational Forms) ---
    "ra": "రా", "raa": "రా", "randi": "రండి", "ravali": "రావాలి", "vastunna": "వస్తున్నా", "vastundi": "వస్తుంది",
    "vachanu": "వచ్చాను", "vachadu": "వచ్చాడు", "vachindi": "వచ్చింది", "vacharu": "వచ్చారు",
    "po": "పో", "pondhi": "పొండి", "povali": "పోవాలి", "potunna": "పోతున్న", "poyanu": "పోయాను", "poyindi": "పోయింది",
    "cheyyi": "చెయ్యి", "chey": "చేయి", "cheyandi": "చేయండి", "cheyyandi": "చెయ్యండి", "cheyyali": "చెయ్యాలి",
    "chestunna": "చేస్తున్న", "chestundi": "చేస్తుంది", "chesanu": "చేశాను", "chesadu": "చేశాడు", "chesindi": "చేసింది", "chesaru": "చేశారు",
    "cheppu": "చెప్పు", "cheppandi": "చెప్పండి", "cheppali": "చెప్పాలి", "cheptunna": "చెప్తున్న",
    "cheppanu": "చెప్పాను", "cheppadu": "చెప్పాడు", "cheppindi": "చెప్పింది", "chepparu": "చెప్పారు",
    "choodu": "చూడు", "chudu": "చూడు", "choodandi": "చూడండి", "chudandi": "చూడండి", "chudali": "చూడాలి",
    "chustunna": "చూస్తున్న", "chusanu": "చూశాను", "chusadu": "చూశాడు", "chusindi": "చూసింది", "chusaru": "చూశారు",
    "tinu": "తిను", "tinandi": "తినండి", "tinali": "తినాలి", "tintunna": "తింటున్న",
    "tinnanu": "తిన్నాను", "tinnadu": "తిన్నాడు", "tinnindi": "తిన్నది", "tinnaru": "తిన్నారు",
    "adugu": "అడుగు", "adagandi": "అడగండి", "adagali": "అడగాలి", "adugutunna": "అడుగుతున్న",
    "adigaru": "అడిగారు", "adiganu": "అడిగాను", "adigadu": "అడిగాడు",
    "vinu": "విను", "vinandi": "వినండి", "vinali": "వినాలి", "vintunna": "వింటున్న", "vinnanu": "విన్నాను",
    "telusu": "తెలుసు", "teliyadu": "తెలియదు", "telusuko": "తెలుసుకో", "telusukondi": "తెలుసుకోండి",
    "teesuko": "తీసుకో", "teesukondi": "తీసుకోండి", "pettuko": "పెట్టుకో", "pettukondi": "పెట్టుకోండి",
    "aagu": "ఆగు", "aagandi": "ఆగండి", "aagali": "ఆగాలి",
    "aadu": "ఆడు", "aaduko": "ఆడుకో", "aadukovali": "ఆడుకోవాలి", "aadukuntunnaru": "ఆడుకుంటున్నారు", "aadukuntunna": "ఆడుకుంటున్న", "aadukuntundi": "ఆడుకుంటుంది", "aadukuntadu": "ఆడుకుంటాడు", "aadukuntanu": "ఆడుకుంటాను", "aadukuntu": "ఆడుకుంటూ",
    "chaduvu": "చదువు", "chadavandi": "చదవండి", "chadavali": "చదవాలి", "chaduvutunna": "చదువుతున్న",
    "raayi": "రాయి", "raayandi": "రాయండి", "raayali": "రాయాలి", "raastunna": "రాస్తున్న",
    "kurcho": "కూర్చో", "kurchondi": "కూర్చోండి", "nilabadu": "నిలబడు",
    "bhayapadu": "భయపడు", "bhayapadaddu": "భయపడద్దు", "bhayapadali": "భయపడాలి", "bhayapadi": "భయపడి",
    "marchipo": "మర్చిపో", "marchipovaddu": "మర్చిపోవద్దు", "marchipoyanu": "మర్చిపోయాను",

    # --- Family & People ---
    "amma": "అమ్మ", "nanna": "నాన్న", "talli": "తల్లి", "tandri": "తండ్రి",
    "annayya": "అన్నయ్య", "anna": "అన్న", "tammudu": "తమ్ముడు", "akka": "అక్క", "chelli": "చెల్లి", "chellelu": "చెల్లెలు",
    "pillalu": "పిల్లలు", "pilla": "పిల్ల", "babu": "బాబు", "papa": "పాప",
    "koduku": "కొడుకు", "kuthuru": "కూతురు", "bharya": "భార్య", "bhatta": "భర్త",
    "snehithudu": "స్నేహితుడు", "snehitudu": "స్నేహితుడు", "snehithulu": "స్నేహితులు", "snehitulu": "స్నేహితులు", "snehitulato": "స్నేహితులతో", "snehitulatho": "స్నేహితులతో", "snehithulato": "స్నేహితులతో", "snehithulatho": "స్నేహితులతో",
    "mitrudu": "మిత్రుడు", "manishi": "మనిషి", "prajalu": "ప్రజలు",

    # --- Nouns & Everyday Objects ---
    "illu": "ఇల్లు", "ooru": "ఊరు", "badi": "బడి", "gudi": "గుడి",
    "pustakam": "పుస్తకం", "pustakalu": "పుస్తకాలు", "kalam": "కలం", "kagitham": "కాగితం",
    "annam": "అన్నం", "bhojanam": "భోజనం", "neellu": "నీళ్ళు", "neeru": "నీరు", "paalu": "పాలు",
    "pani": "పని", "panulu": "పనులు", "vishayam": "విషయం", "prashna": "ప్రశ్న", "samadhanam": "సమాధానం",
    "bhasha": "భాష", "desham": "దేశం", "raashtram": "రాష్ట్రం", "nagaram": "నగరం", "graamam": "గ్రామం",
    "varsham": "వర్షం", "gaali": "గాలి", "velugu": "వెలుగు", "cheekati": "చీకటి",
    "prema": "ప్రేమ", "sneham": "స్నేహం", "snehamto": "స్నేహంతో", "shanti": "శాంతి", "sukham": "సుఖం",
    "santosham": "సంతోషం", "kopam": "కోపం", "kopamto": "కోపంతో", "bhayam": "భయం", "dhairyam": "ధైర్యం",

    # --- Adjectives ---
    "manchi": "మంచి", "pedda": "పెద్ద", "chinna": "చిన్న", "kotha": "కొత్త", "paatha": "పాత", "pata": "పాత",
    "goppa": "గొప్ప", "teepi": "తీపి", "chaala": "చాలా", "ekkuva": "ఎక్కువ", "takkuva": "తక్కువ",
    "sulabham": "సులభం", "kashtam": "కష్టం", "istam": "ఇష్టం", "ishtam": "ఇష్టం",

    # --- Greetings & Politeness ---
    "namaskaram": "నమస్కారం", "namaskaaram": "నమస్కారం", "namaste": "నమస్తే",
    "dhanyavadalu": "ధన్యవాదాలు", "shubhodhayam": "శుభోదయం", "subhodhayam": "శుభోదయం",
    "dayachesi": "దయచేసి", "kshamanchandi": "క్షమించండి",
}

# Universal Noun Declensions (విభక్తులు)
NOUN_DECLENSIONS = [
    ("nunchi", "నుంచి"),
    ("nundi", "నుండి"),
    ("kosam", "కోసం"),
    ("looki", "లోకి"),
    ("loki", "లోకి"),
    ("looni", "లోని"),
    ("loni", "లోని"),
    ("kante", "కంటే"),
    ("thoo", "తో"),
    ("too", "తో"),
    ("tho", "తో"),
    ("to", "తో"),
    ("loo", "లో"),
    ("lo", "లో"),
    ("pai", "పై"),
    ("ki", "కి"),
    ("ku", "కు"),
]

# Universal Verb Suffixes & Auxiliaries (క్రియా ప్రత్యయాలు)
VERB_DECLENSIONS = [
    # Compound auxiliaries
    ("kovadam", "కోవడం"),
    ("kovali", "కోవాలి"),
    ("koni", "కొని"),
    ("kuni", "కుని"),
    ("kondi", "కోండి"),
    ("kuntunnaaru", "కుంటున్నారు"),
    ("kuntunnaru", "కుంటున్నారు"),
    ("kuntunnaanu", "కుంటున్నాను"),
    ("kuntunnanu", "కుంటున్నాను"),
    ("kuntunnaadu", "కుంటున్నాడు"),
    ("kuntunnadu", "కుంటున్నాడు"),
    ("kuntundi", "కుంటుంది"),
    ("kuntunna", "కుంటున్న"),
    ("kuntaru", "కుంటారు"),
    ("kuntadu", "కుంటాడు"),
    ("kuntanu", "కుంటాను"),
    ("kuntamu", "కుంటాము"),
    ("kuntam", "కుంటాం"),
    ("kuntuu", "కుంటూ"),
    ("kuntoo", "కుంటూ"),
    ("kuntu", "కుంటూ"),
    ("kunnaru", "కున్నారు"),
    ("kunnanu", "కున్నాను"),
    ("kunnadu", "కున్నాడు"),
    ("kunna", "కున్న"),
    ("kune", "కునే"),
    ("vasthe", "వస్తే"),
    ("vaste", "వస్తే"),
    ("ochchi", "ఒచ్చి"),
    ("ochi", "ఒచ్చి"),
    ("padali", "పడాలి"),
    ("paddanu", "పడ్డాను"),
    ("padadu", "పడ్డాడు"),
    ("padindi", "పడింది"),
    ("padaru", "పడ్డారు"),
    ("padi", "పడి"),
    
    # Conditional & Sequential
    ("the", "తే"),
    ("te", "తే"),
    ("aka", "ఆక"),
    
    # Continuous Aspect
    ("tunnaaru", "తున్నారు"),
    ("tunnaru", "తున్నారు"),
    ("tunnaanu", "తున్నాను"),
    ("tunnanu", "తున్నాను"),
    ("tunnaadu", "తున్నాడు"),
    ("tunnadu", "తున్నాడు"),
    ("tunnayi", "తున్నాయి"),
    ("tunnaayi", "తున్నాయి"),
    ("thundi", "తుంది"),
    ("tundi", "తుంది"),
    ("thunna", "తున్న"),
    ("tunna", "తున్న"),
    ("tuu", "తూ"),
    ("too", "తూ"),
    ("tu", "తూ"),
    
    # Past Tense Inflections
    ("aanu", "ాను"),
    ("aadu", "ాడు"),
    ("indi", "ింది"),
    ("indhi", "ింది"),
    ("aaru", "ారు"),
    ("aamu", "ాము"),
    ("anu", "ాను"),
    ("adu", "ాడు"),
    ("aru", "ారు"),
    ("amu", "ాము"),
    
    # Infinitive & Obligation
    ("aalsina", "ాల్సిన"),
    ("alsina", "ాల్సిన"),
    ("aali", "ాలి"),
    ("ali", "ాలి"),
    ("andi", "ండి"),
    ("amdi", "ండి"),
    ("adam", "డం"),
    ("aadam", "ాడం"),
]

def load_dictionaries():
    """
    1. Load dictionaries:
       - te_top10k for frequency ranking (high freq wins on collision)
       - casual_type_dict for casual mode (all lowercase keys)
       - typo_fixes for fallback normalization on unknown words
       - conversational lexicon for colloquial daily language
    """
    global CASUAL_DICT, TYPO_FIXES, SORTED_TYPO_FIXES, TOP10K_FREQ, _INITIALIZED
    if _INITIALIZED:
        return

    # 1. Load te_top10k for frequency ranking
    top10k_path = find_data_file("te_top10k.json")
    if os.path.exists(top10k_path):
        try:
            with open(top10k_path, "r", encoding="utf-8") as f:
                TOP10K_FREQ = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load te_top10k.json: {e}")
            TOP10K_FREQ = {}

    # 2. Load typo_fixes
    typo_path = find_data_file("typo_fixes.json")
    if os.path.exists(typo_path):
        try:
            with open(typo_path, "r", encoding="utf-8") as f:
                TYPO_FIXES = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load typo_fixes.json: {e}")
            TYPO_FIXES = {}

    # Sort typo fixes by key length descending so longer suffixes match first
    SORTED_TYPO_FIXES = sorted(TYPO_FIXES.items(), key=lambda x: len(x[0]), reverse=True)

    # 3. Load casual_type_dict (58421 roman lowercase -> Telugu)
    casual_path = find_data_file("casual_type_dict.json")
    raw_casual = {}
    if os.path.exists(casual_path):
        try:
            with open(casual_path, "r", encoding="utf-8") as f:
                raw_casual = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load casual_type_dict.json: {e}")
            raw_casual = {}

    # Initialize CASUAL_DICT with all lowercase keys
    for k, v in raw_casual.items():
        k_lower = k.lower()
        if k_lower in CASUAL_DICT:
            # Collision resolution: higher frequency in te_top10k wins
            existing_word = CASUAL_DICT[k_lower]
            if existing_word != v:
                freq_existing = TOP10K_FREQ.get(existing_word, 0)
                freq_new = TOP10K_FREQ.get(v, 0)
                if freq_new > freq_existing:
                    CASUAL_DICT[k_lower] = v
        else:
            CASUAL_DICT[k_lower] = v

    def register_freq_mapping(key: str, telugu_word: str):
        key = key.lower()
        if key in CASUAL_DICT:
            existing = CASUAL_DICT[key]
            if existing != telugu_word:
                freq_existing = TOP10K_FREQ.get(existing, 0)
                freq_new = TOP10K_FREQ.get(telugu_word, 0)
                if freq_new >= freq_existing:
                    CASUAL_DICT[key] = telugu_word
        else:
            CASUAL_DICT[key] = telugu_word

    # Apply frequency ranking & collision resolution for high-frequency words from te_top10k
    top_word_mappings = [
        ("వస్తున్నా", ["vastunna", "vasthunna", "vastunnaa", "vastuna", "vastunnaaa"]),
        ("చెప్పండి", ["cheppandi", "cheppamdi"]),
        ("చేయండి", ["cheyandi", "cheeyandi"]),
        ("చెయ్యండి", ["cheyyandi", "cheyyamdi"]),
        ("రండి", ["randi", "randhi", "ramdi"]),
        ("చూడండి", ["choodandi", "chudandi", "chuudandi", "choodamdi"]),
        ("నువ్వు", ["nuvvu", "nuvu"]),
        ("అక్కడే", ["akkade", "akkadae"]),
        ("ఉండు", ["undu", "umdu"]),
        ("ఉంది", ["undi", "undhi", "umdi"]),
        ("లేదు", ["ledu", "ledhu", "laedu"]),
        ("బాగుంది", ["bagundi", "bagundhi", "bagundh"]),
        ("అవును", ["avunu", "avnu"]),
        ("కాదు", ["kaadu", "kadu"]),
        ("వచ్చింది", ["vachindi", "vachchindi", "vachchindhi"]),
        ("వెళ్ళింది", ["vellindi", "vellindhi"]),
    ]

    for tel_word, roman_keys in top_word_mappings:
        for rk in roman_keys:
            register_freq_mapping(rk, tel_word)

    # 4. Inject Conversational Lexicon overrides (highest priority for casual everyday typing)
    for k, v in CONVERSATIONAL_LEXICON.items():
        CASUAL_DICT[k.lower()] = v

    _INITIALIZED = True

def apply_sandhi(base_te: str, sfx_te: str, sfx_en: str) -> str:
    """
    Applies Telugu Sandhi rules when joining a base Telugu word and a suffix.
    """
    if not base_te or not sfx_te:
        return (base_te or "") + (sfx_te or "")

    VIRAMA = '్'
    
    # Case A: Base ends with Halant/Virama (e.g. మాట్లాడ్, చెప్ప్, అడగ్)
    if base_te.endswith(VIRAMA):
        cons_base = base_te[:-1]
        vowel_to_matra = {
            'అ': '', 'ఆ': 'ా', 'ఇ': 'ి', 'ఈ': 'ీ', 'ఉ': 'ు', 'ఊ': 'ూ',
            'ఎ': 'ె', 'ఏ': 'ే', 'ఐ': 'ై', 'ఒ': 'ొ', 'ఓ': 'ో', 'ఔ': 'ౌ'
        }
        first_char = sfx_te[0]
        if first_char in vowel_to_matra:
            matra = vowel_to_matra[first_char]
            return cons_base + matra + sfx_te[1:]
        elif sfx_te[0] in ['ా', 'ి', 'ీ', 'ు', 'ూ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ']:
            return cons_base + sfx_te

    # Case B: Base ends with Anusvara (Sunna 'ం') like 'స్నేహం', 'కోపం', 'సంతోషం'
    if base_te.endswith('ం'):
        return base_te + sfx_te

    # Case C: Suffix starts with a matra but base ends with inherent vowel
    if sfx_te[0] in ['ా', 'ి', 'ీ', 'ు', 'ూ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ']:
        # If base ends with a consonant that has no virama (inherent 'a'), combine directly
        return base_te + sfx_te

    return base_te + sfx_te

def decompose_compound(w: str) -> str:
    """
    Universal Morphological Decomposer:
    Decomposes arbitrary nouns and verbs by stripping known grammatical suffixes,
    resolving the root stem, and recombining with correct Telugu Sandhi.
    """
    if len(w) < 4:
        return None

    # Common irregular conversational roots
    STEM_MAP = {
        "naa": "నా",
        "amma": "అమ్మ",
        "nanna": "నాన్న",
        "mana": "మన",
        "mee": "మీ",
        "int": "ఇంట్",
        "inti": "ఇంటి",
        "oor": "ఊర్",
        "vell": "వెళ్ళ",
        "matlad": "మాట్లాడ్",
        "chepp": "చెప్ప",
        "adag": "అడగ",
        "vach": "వచ్చ",
        "ches": "చేశ",
        "teesuk": "తీసుకు",
        "pettuk": "పెట్టుకు",
        "kavalsi": "కావల్సి",
        "ravalsi": "రావల్సి",
        "chudalsi": "చూడాల్సి",
        "kashta": "కష్ట",
        "sadhinchu": "సాధించు",
        "rav": "రావ",
        "poy": "పోయ",
        "tin": "తిన",
        "chud": "చూడ",
        "chood": "చూడ",
        "chey": "చేయ",
        "vin": "విన",
        "aadu": "ఆడు",
        "aad": "ఆడ",
        "padu": "పడు",
        "pad": "పడ",
        "chaduvu": "చదువు",
        "chadav": "చదవ",
        "chesu": "చేసు",
        "chusu": "చూసు",
        "telusu": "తెలుసు",
        "kurchu": "కూర్చు",
        "nilabadu": "నిలబడు",
        "bhayapad": "భయపడ",
        "und": "ఉండ",
    }

    def resolve_stem(stem: str) -> str:
        if stem in STEM_MAP:
            return STEM_MAP[stem]
        if stem in CASUAL_DICT:
            return CASUAL_DICT[stem]
        
        # Universal Plural Oblique Stem (e.g. pillala -> pillalu, snehitula -> snehitulu)
        if stem.endswith("la") and len(stem) > 3:
            nom_key = stem[:-1] + "u"
            if nom_key in CASUAL_DICT:
                nom_val = CASUAL_DICT[nom_key]
                if nom_val.endswith("లు"):
                    return nom_val[:-1] + "ల"

        # Universal Anusvara Stem (e.g. snehan- -> sneham, kopan- -> kopam)
        if stem.endswith("n") and len(stem) > 2:
            m_key = stem[:-1] + "m"
            if m_key in CASUAL_DICT:
                return CASUAL_DICT[m_key]

        return None

    # 1. Try Universal Verb Declensions
    for sfx_en, sfx_te in VERB_DECLENSIONS:
        if w.endswith(sfx_en) and len(w) > len(sfx_en) + 1:
            stem = w[:-len(sfx_en)]
            base_te = resolve_stem(stem)
            if base_te:
                return apply_sandhi(base_te, sfx_te, sfx_en)

    # 2. Try Universal Noun Declensions
    for sfx_en, sfx_te in NOUN_DECLENSIONS:
        if w.endswith(sfx_en) and len(w) > len(sfx_en) + 1:
            stem = w[:-len(sfx_en)]
            base_te = resolve_stem(stem)
            if base_te:
                return apply_sandhi(base_te, sfx_te, sfx_en)

    return None

def casual_phonetic_transliterate(word: str) -> str:
    """
    Dedicated Casual-Phonetic Fallback Engine:
    - Eliminates toxic RTS diphthongs ('av' -> ౌ and 'ay' -> ై)
    - Automatically maps 'sht' -> ష్ట, 'tl' -> ట్ల, 'dl' -> డ్ల
    - Word-final -am -> Sunna ం (never halant మ్)
    - Word-final postpositions -to, -lo, -ko -> long ో
    - Sibilants: 'sh' before retroflex or vowel -> ష
    """
    if not word:
        return ""

    w = word.lower()

    # 1. Pre-process retroflex clusters
    w = re.sub(r'sht', 'ShTa', w)
    w = re.sub(r'tl', 'Tla', w)
    w = re.sub(r'dl', 'Dla', w)

    # 2. Prevent toxic 'av' -> ౌ
    w = re.sub(r'av([aeiouyrl])', r'a_v\1', w)

    # 3. Prevent toxic 'ay' -> ై
    w = re.sub(r'ay([aeiou])', r'a_y\1', w)

    # 4. Doubled chch -> cch (చ్చ)
    w = re.sub(r'chch', 'cch', w)

    # 5. Word-final -am -> Sunna 'M' (ం)
    if w.endswith('am') and len(w) > 2:
        w = w[:-2] + 'aM'

    # 6. Word-final postpositions: -to -> -tO (తో), -lo -> -lO (లో), -ko -> -kO (కో)
    for p in ['to', 'tho']:
        if w.endswith(p):
            w = w[:-len(p)] + 'tO'
            break
    for p in ['lo', 'lho']:
        if w.endswith(p):
            w = w[:-len(p)] + 'lO'
            break
    if w.endswith('ko'):
        w = w[:-2] + 'kO'

    # 7. Sibilants: In words like manushulu, bhasha, 'sh' -> 'Sh' (ష)
    w = re.sub(r'sh([uUaAoOiI])', r'Sh\1', w)

    # Feed into exact engine with pre-processed keys
    out = exact_transliterate(w)
    
    # Remove any internal ZWNJ escape markers
    out = out.replace('\u200c', '')
    return out

def transliterate_word(word: str) -> str:
    """
    Transliterate a single word using CasualType rules:
    1. lowercase input
    2. direct lookup in CASUAL_DICT (58k+ entries + CONVERSATIONAL_LEXICON)
    3. universal morphological compound & declension decomposition
    4. typo_fixes (amdi->andi etc)
    5. smart casual-phonetic fallback
    """
    if not _INITIALIZED:
        load_dictionaries()

    w_lower = word.lower()

    # 1 & 2. Direct lookup in CASUAL_DICT
    if w_lower in CASUAL_DICT:
        return CASUAL_DICT[w_lower]

    # 3. Universal morphological compound & affix decomposition
    decomposed = decompose_compound(w_lower)
    if decomposed:
        return decomposed

    # 4. Typo fixes lookup
    # 4a. Direct whole-word typo match
    if w_lower in TYPO_FIXES:
        fix = TYPO_FIXES[w_lower]
        if fix in CASUAL_DICT:
            return CASUAL_DICT[fix]

    # 4b. Suffix-based typo match (e.g. cheppamdi -> cheppandi, undhi -> undi)
    for err, fix in SORTED_TYPO_FIXES:
        if w_lower.endswith(err):
            candidate = w_lower[:-len(err)] + fix
            if candidate in CASUAL_DICT:
                return CASUAL_DICT[candidate]

    # 4c. Substring-based typo match
    for err, fix in SORTED_TYPO_FIXES:
        if err in w_lower:
            candidate = w_lower.replace(err, fix)
            if candidate in CASUAL_DICT:
                return CASUAL_DICT[candidate]

    # 5. Smart Casual-Phonetic Fallback
    return casual_phonetic_transliterate(word)

def transliterate(input_text: str, casual_enabled: bool = True) -> str:
    """
    Engine logic:
    def transliterate(input_text, casual_enabled):
      if casual_enabled:
        # Tokenizes input into words & delimiters, applying casual logic per word.
      else:
        # exact capitals mapping (existing behavior)
    """
    if not input_text:
        return ""

    if not casual_enabled:
        return exact_transliterate(input_text)

    if not _INITIALIZED:
        load_dictionaries()

    # If single word without spaces or delimiters, transliterate directly
    if re.match(r'^[a-zA-Z0-9~_]+$', input_text):
        return transliterate_word(input_text)

    # For multi-word text, split by words and non-words (preserving spaces/punctuation)
    tokens = re.split(r'([^\w~_]+)', input_text)
    out = []
    for token in tokens:
        if not token:
            continue
        if re.match(r'^[a-zA-Z0-9~_]+$', token):
            out.append(transliterate_word(token))
        else:
            out.append(token)
    return "".join(out)
