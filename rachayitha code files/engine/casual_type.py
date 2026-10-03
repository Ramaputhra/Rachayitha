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
    ]
    for d in search_dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return filename

# Language model
try:
    from .lm import TeluguLM
except ImportError:
    try:
        from engine.lm import TeluguLM
    except ImportError:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if cur_dir not in sys.path:
            sys.path.insert(0, cur_dir)
        from lm import TeluguLM

# Global dictionaries
CASUAL_DICT = {}
CASUAL_CANDIDATES = {}
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
    "velli": "వెళ్ళి", "vellina": "వెళ్ళిన", "vellaru": "వెళ్ళారు", "vellaanu": "వెళ్ళాను", "velanu": "వెళ్లను",
    "vellipoyindi": "వెళ్ళిపోయింది", "vellipoyaru": "వెళ్ళిపోయారు", "vellipoyadu": "వెళ్ళిపోయాడు",
    "ammato": "అమ్మతో", "ammatho": "అమ్మతో", "naato": "నాతో", "naatho": "నాతో",
    "nannato": "నాన్నతో", "manato": "మనతో", "meeto": "మీతో", "meetoo": "మీతో",
    "maatlaadaanu": "మాట్లాడాను", "matlaadaanu": "మాట్లాడాను", "matladadu": "మాట్లాడాడు", "matladindi": "మాట్లాడింది",
    "matladaru": "మాట్లాడారు", "matladali": "మాట్లాడాలి", "matladadam": "మాట్లాడడం", "matladutunna": "మాట్లాడుతున్న",
    "matladutu": "మాట్లాడుతూ", "matladava": "మాట్లాడవా", "sepu": "సేపు", "konchem": "కొంచెం",
    "matlade": "మాట్లాడే", "maatlaade": "మాట్లాడే", "matladedi": "మాట్లాడేది", "matladedhi": "మాట్లాడేది", "matladetappudu": "మాట్లాడేటప్పుడు",
    "nuvvennanna": "నువ్వెన్నన్నా", "nuvvuennanna": "నువ్వెన్నన్నా",
    "nenenduku": "నేనెందుకు", "neenenduku": "నేనెందుకు", "nenedo": "నేనేదో", "nenemo": "నేనేమో",
    "nenena": "నేనేనా", "nenoo": "నేనూ", "nenuu": "నేనూ", "nenunna": "నేనున్నా", "nenunnanu": "నేనున్నాను",
    "veltanu": "వెళ్తాను", "velthanu": "వెళ్తాను", "veltadu": "వెళ్తాడు", "velthadu": "వెళ్తాడు",
    "veltaru": "వెళ్తారు", "veltharu": "వెళ్తారు", "veltadi": "వెళ్తది", "velthadi": "వెళ్తది",
    "veltundi": "వెళ్తుంది", "velthundi": "వెళ్తుంది", "veltava": "వెళ్తావా", "velthava": "వెళ్తావా",
    "veltara": "వెళ్తారా", "velthara": "వెళ్తారా", "veltam": "వెళ్తాం", "veltham": "వెళ్తాం",
    "veltu": "వెళ్తూ", "velthu": "వెళ్తూ", "velte": "వెళ్తే", "velthe": "వెళ్తే",
    "sarele": "సరేలే", "sareley": "సరేలే", "sarelee": "సరేలే",
    "unnavo": "ఉన్నావో", "unnaavo": "ఉన్నావో", "unnado": "ఉన్నాడో", "unnaado": "ఉన్నాడో",
    "unnaro": "ఉన్నారో", "unnaaro": "ఉన్నారో", "unnano": "ఉన్నానో", "unnaano": "ఉన్నానో",
    "bayataki": "బయటకి", "bayatiki": "బయటికి", "bayataku": "బయటకు",
    "vere": "వేరే", "veere": "వేరే",
    "samayamlo": "సమయంలో", "samayaniki": "సమయానికి", "samayam": "సమయం",
    "cheppu": "చెప్పు",
    "entante": "ఏంటంటే", "manushulam": "మనుషులం", "manushulu": "మనుషులు", "manushulaku": "మనుషులకు",
    "edaina": "ఏదైనా", "edainaa": "ఏదైనా", "endukante": "ఎందుకంటే", "andukante": "అందుకంటే",
    "kavalsivasthe": "కావల్సివస్తే", "kavalsivaste": "కావల్సివస్తే", "kavalsina": "కావల్సిన", "kavalasina": "కావలసిన",
    "kavali": "కావాలి",
    "nadavaalsina": "నడవాల్సిన", "nadavalsina": "నడవాల్సిన", "nadavalasina": "నడవవలసిన",
    "nadavaalsi": "నడవాల్సి", "nadavalsi": "నడవాల్సి", "nadavalasi": "నడవవలసి",
    "nadavali": "నడవాలి", "nadavaali": "నడవాలి",
    "nadavadam": "నడవడం", "nadavandi": "నడవండి",
    "nadavale": "నడవలే", "nadavaledu": "నడవలేదు",
    "nadustunna": "నడుస్తున్న", "nadustunnanu": "నడుస్తున్నాను",
    "nadustaru": "నడుస్తారు", "nadustadu": "నడుస్తాడు", "nadavaka": "నడవక",
    "kashtapadi": "కష్టపడి", "kashtapadali": "కష్టపడాలి", "kashtapaddanu": "కష్టపడ్డాను",
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
    "nenu": "నేను", "neenu": "నేను", "naa": "నా", "na": "నా", "naaku": "నాకు", "nannu": "నన్ను",
    "nuvvu": "నువ్వు", "nuvu": "నువ్వు", "nee": "నీ", "neeku": "నీకు", "ninnu": "నిన్ను",
    "meeru": "మీరు", "meeruu": "మీరు", "mee": "మీ", "meeku": "మీకు", "mimmalni": "మిమ్మల్ని",
    "memu": "మేము", "maaku": "మాకు",
    "manam": "మనం", "manamu": "మనము", "manaku": "మనకు", "manalni": "మనల్ని",
    "vaaru": "వారు", "varu": "వారు", "vaallu": "వాళ్ళు", "vallu": "వాళ్ళు", "vaallaki": "వాళ్ళకి",
    "atanu": "అతను", "atadu": "అతడు", "ataniki": "అతనికి", "atanni": "అతన్ని",
    "vadu": "వాడు", "vaadu": "వాడు", "vadiki": "వాడికి", "vaadiki": "వాడికి",
    "vadini": "వాడిని", "vaadini": "వాడిని", "vaditho": "వాడితో", "vaaditho": "వాడితో",
    "vadito": "వాడితో", "vaadito": "వాడితో", "vadikosam": "వాడికోసం", "vaadikosam": "వాడికోసం",
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

    # --- Question Words, Connectors & Quantifiers ---
    "ela": "ఎలా", "elaa": "ఎలా", "ekkada": "ఎక్కడ", "ekkadaa": "ఎక్కడ",
    "akkada": "అక్కడ", "ikkada": "ఇక్కడ", "enduku": "ఎందుకు", "anduku": "అందుకు",
    "emiti": "ఏమిటి", "enti": "ఏంటి", "em": "ఏం", "eedi": "ఏది", "evaru": "ఎవరు",
    "entha": "ఎంత", "enthaga": "ఎంతగా", "enni": "ఎన్ని", "ga": "గా", "gaa": "గా",
    "ante": "అంటె", "antee": "అంటే", "anthey": "అంతే", "anteh": "అంతే",
    "matallo": "మాటల్లో", "maatallo": "మాటల్లో",

    # --- Affirmations & Negations ---
    "avunu": "అవును", "avnu": "అవును", "kadu": "కాదు", "kaadu": "కాదు",
    "ledu": "లేదు", "ledhu": "లేదు", "laedu": "లేదు", "undi": "ఉంది", "undhi": "ఉంది",
    "unnaru": "ఉన్నారు", "unnanu": "ఉన్నాను", "unnadu": "ఉన్నాడు", "unnadi": "ఉన్నది", "unnamu": "ఉన్నాము", "unnam": "ఉన్నాం", "unnavu": "ఉన్నావు", "unnara": "ఉన్నారా",
    "bagundi": "బాగుంది", "bagundhi": "బాగుంది", "baga": "బాగా", "baaga": "బాగా",
    "nijam": "నిజం", "abaddham": "అబద్ధం", "sare": "సరే", "alage": "అలాగే",

    # --- Existential & Auxiliary Paradigms (ఉండు / ఉంటాడు / ఉండడం) ---
    "undu": "ఉండు", "umdu": "ఉండు", "undandi": "ఉండండి", "undali": "ఉండాలి", "undaali": "ఉండాలి",
    "untadu": "ఉంటాడు", "untaadu": "ఉంటాడు", "unthadu": "ఉంటాడు", "unthaadu": "ఉంటాడు",
    "untanu": "ఉంటాను", "untaanu": "ఉంటాను", "unthanu": "ఉంటాను", "unthaanu": "ఉంటాను",
    "untaru": "ఉంటారు", "untaaru": "ఉంటారు", "untharu": "ఉంటారు", "unthaaru": "ఉంటారు",
    "untundi": "ఉంటుంది", "unthundi": "ఉంటుంది", "untundhi": "ఉంటుంది",
    "untadi": "ఉంటది", "unthadi": "ఉంటది",
    "untam": "ఉంటాం", "untaam": "ఉంటాం", "untamu": "ఉంటాము", "untaamu": "ఉంటాము",
    "untava": "ఉంటావా", "untaava": "ఉంటావా", "unthava": "ఉంటావా",
    "untara": "ఉంటారా", "untaara": "ఉంటారా", "unthara": "ఉంటారా",
    "undadu": "ఉండడు", "undanu": "ఉండను", "undaru": "ఉండరు", "undamu": "ఉండము", "undam": "ఉండం",
    "undedi": "ఉండేది", "undeedi": "ఉండేది",
    "undevaru": "ఉండేవారు", "undeevaru": "ఉండేవారు",
    "unde": "ఉండే", "undee": "ఉండే",
    "undatledu": "ఉండట్లేదు", "undatlaedu": "ఉండట్లేదు",
    "untunna": "ఉంటున్న", "untunnaru": "ఉంటున్నారు", "untunnanu": "ఉంటున్నాను", "untunnadu": "ఉంటున్నాడు",
    "untunnam": "ఉంటున్నాం", "untunnamu": "ఉంటున్నాము",
    "undipoyindi": "ఉండిపోయింది", "undipoyaru": "ఉండిపోయారు", "undipoyadu": "ఉండిపోయాడు",

    # --- Common Verbs (Inflected Conversational Forms) ---
    "ra": "రా", "raa": "రా", "randi": "రండి", "ravali": "రావాలి", "vastunna": "వస్తున్నా", "vastundi": "వస్తుంది",
    "vachanu": "వచ్చాను", "vachadu": "వచ్చాడు", "vachindi": "వచ్చింది", "vacharu": "వచ్చారు",
    "po": "పో", "pondhi": "పొండి", "povali": "పోవాలి", "potunna": "పోతున్న", "poyanu": "పోయాను", "poyindi": "పోయింది",
    "cheyyi": "చెయ్యి", "chey": "చేయి", "cheyandi": "చేయండి", "cheyyandi": "చెయ్యండి", "cheyyali": "చెయ్యాలి",
    "chestunna": "చేస్తున్న", "chestundi": "చేస్తుంది", "chesanu": "చేశాను", "chesadu": "చేశాడు", "chesindi": "చేసింది", "chesaru": "చేశారు",
    "cheppu": "చెప్పు", "cheppandi": "చెప్పండి", "cheppali": "చెప్పాలి", "cheptunna": "చెప్తున్న",
    "cheppanu": "చెప్పాను", "cheppadu": "చెప్పాడు", "cheppindi": "చెప్పింది", "chepparu": "చెప్పారు",
    "cheppalenu": "చెప్పలేను", "cheppaledu": "చెప్పలేదు", "cheppaleru": "చెప్పలేరు", "cheppalemu": "చెప్పలేము", "cheppalem": "చెప్పలేం",
    "chudalenu": "చూడలేను", "chudaledu": "చూడలేదు", "tinalenu": "తినలేను", "vellalenu": "వెళ్ళలేను", "raalenu": "రాలేను", "chesukolenu": "చేసుకోలేను",
    "choodu": "చూడు", "chudu": "చూడు", "choodandi": "చూడండి", "chudandi": "చూడండి", "chudali": "చూడాలి",
    "chustunna": "చూస్తున్న", "chusanu": "చూశాను", "chusadu": "చూశాడు", "chusindi": "చూసింది", "chusaru": "చూశారు",
    "tinu": "తిను", "tinandi": "తినండి", "tinali": "తినాలి", "tintunna": "తింటున్న",
    "tinnanu": "తిన్నాను", "tinnadu": "తిన్నాడు", "tinnindi": "తిన్నది", "tinnaru": "తిన్నారు",
    "adugu": "అడుగు", "adagandi": "అడగండి", "adagali": "అడగాలి", "adugutunna": "అడుగుతున్న",
    "adigaru": "అడిగారు", "adiganu": "అడిగాను", "adigadu": "అడిగాడు",
    "annaara": "అన్నారా", "annara": "అన్నారా", "annaru": "అన్నారు",
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

    # --- Verbs of Admiration, Respect & Habitual ---
    "abhimanam": "అభిమానం", "abhimani": "అభిమాని",
    "abhimanisthadu": "అభిమానిస్తాడు", "abhimanistadu": "అభిమానిస్తాడు",
    "abhimanistharu": "అభిమానిస్తారు", "abhimanistaru": "అభిమానిస్తారు",
    "abhimanisthanu": "అభిమానిస్తాను", "abhimanistanu": "అభిమానిస్తాను",
    "abhimanisthundi": "అభిమానిస్తుంది", "abhimanistundi": "అభిమానిస్తుంది",
    "abhimanistam": "అభిమానిస్తాం", "abhimanistham": "అభిమానిస్తాం",
    "abhimanulu": "అభిమానులు", "abhimanulaku": "అభిమానులకు",
    "abhimanulatho": "అభిమానులతో", "abhimanulato": "అభిమానులతో",
    "abhimaninchali": "అభిమానించాలి", "abhimanincharu": "అభిమానించారు", "abhimaninchadu": "అభిమానించాడు",

    # --- Family & People ---
    "amma": "అమ్మ", "nanna": "నాన్న", "talli": "తల్లి", "tandri": "తండ్రి",
    "annayya": "అన్నయ్య", "anna": "అన్న",
    "tammudu": "తమ్ముడు", "thammudu": "తమ్ముడు", "thamudu": "తముడు",
    "akka": "అక్క", "chelli": "చెల్లి", "chellelu": "చెల్లెలు",
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
    "santosham": "సంతోషం", "santhosham": "సంతోషం",
    "santoshanga": "సంతోషంగా", "santoshamga": "సంతోషంగా",
    "santhoshanga": "సంతోషంగా", "santhoshamga": "సంతోషంగా",
    "anandanga": "ఆనందంగా", "anandamga": "ఆనందంగా",
    "dhairyanga": "ధైర్యంగా", "sulabhanga": "సులభంగా",
    "vegamga": "వేగంగా", "mukhyanga": "ముఖ్యంగా", "chakkaga": "చక్కగా",
    "kopam": "కోపం", "kopamto": "కోపంతో", "bhayam": "భయం", "dhairyam": "ధైర్యం",

    # --- Adjectives ---
    "manchi": "మంచి", "pedda": "పెద్ద", "chinna": "చిన్న", "kotha": "కొత్త", "paatha": "పాత", "pata": "పాత",
    "goppa": "గొప్ప", "teepi": "తీపి", "chaala": "చాలా", "ekkuva": "ఎక్కువ", "takkuva": "తక్కువ",
    "sulabham": "సులభం", "kashtam": "కష్టం", "istam": "ఇష్టం", "ishtam": "ఇష్టం",

    # --- Greetings & Politeness ---
    "namaskaram": "నమస్కారం", "namaskaaram": "నమస్కారం", "namaste": "నమస్తే",
    "dhanyavadalu": "ధన్యవాదాలు", "shubhodhayam": "శుభోదయం", "subhodhayam": "శుభోదయం",
    "dayachesi": "దయచేసి", "kshamanchandi": "క్షమించండి",

    # --- Common Everyday English Loanwords & Colloquialisms in Tenglish ---
    "casual": "క్యాజువల్", "kyasual": "క్యాజువల్", "casuval": "క్యాజువల్", "kyajuval": "క్యాజువల్", "kyasuval": "క్యాజువల్",
    "typing": "టైపింగ్", "taiping": "టైపింగ్", "type": "టైప్", "taip": "టైప్",
    "keyboard": "కీబోర్డ్", "keeboard": "కీబోర్డ్",
    "mobile": "మొబైల్", "phone": "ఫోన్", "computer": "కంప్యూటర్", "laptop": "లాప్‌టాప్",
    "app": "యాప్", "message": "మెసేజ్", "msg": "మెసేజ్",
    "online": "ఆన్‌లైన్", "offline": "ఆఫ్‌లైన్",
    "update": "అప్‌డేట్", "install": "ఇన్‌స్టాల్", "setup": "సెటప్",
    "link": "లింక్", "post": "పోస్ట్", "check": "చెక్", "test": "టెస్ట్",
    "system": "సిస్టమ్", "time": "టైమ్", "date": "డేట్", "number": "నెంబర్",
    "call": "కాల్", "group": "గ్రూప్", "class": "క్లాస్", "school": "స్కూల్",
    "college": "కాలేజ్", "office": "ఆఫీస్", "work": "వర్క్", "problem": "ప్రాబ్లమ్",
    "help": "హెల్ప్", "fast": "ఫాస్ట్", "slow": "స్లో",
    "settings": "సెట్టింగ్స్", "setting": "సెట్టింగ్", "options": "ఆప్షన్స్", "option": "ఆప్షన్",
    "screen": "స్క్రీన్", "window": "విండో", "file": "ఫైల్", "files": "ఫైల్స్", "folder": "ఫోల్డర్",
    "download": "డౌన్‌లోడ్", "upload": "అప్‌లోడ్", "save": "సేవ్", "delete": "డిలీట్", "clear": "క్లియర్",
    "search": "సెర్చ్", "start": "స్టార్ట్", "stop": "స్టాప్", "restart": "రీస్టార్ట్",
    "ok": "ఓకే", "okay": "ఓకే", "bye": "బాయ్", "hi": "హాయ్", "hello": "హలో",
    "super": "సూపర్", "nice": "నైస్", "good": "గుడ్", "bad": "బ్యాడ్", "correct": "కరెక్ట్", "wrong": "రాంగ్",
    "bug": "బగ్", "error": "ఎర్రర్", "issue": "ఇష్యూ", "version": "వెర్షన్", "mode": "మోడ్", "toggle": "టాగిల్",
    "cheyyatledu": "చేయట్లేదు", "cheyatledu": "చేయట్లేదు", "avvatledu": "అవ్వట్లేదు",
    "raavatledu": "రావట్లేదు", "kaavatledu": "కావట్లేదు", "ratledu": "రాట్లేదు",
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
    ("anga", "ంగా"),
    ("amga", "ంగా"),
    ("gaa", "గా"),
    ("ga", "గా"),
    ("laaga", "లాగా"),
    ("laga", "లాగా"),
    ("varaku", "వరకు"),
    ("batti", "బట్టి"),
    ("gurinchi", "గురించి"),
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

    # Negative potential (-lenu / cannot)
    ("lekapoyaru", "లేకపోయారు"),
    ("lekapoyadu", "లేకపోయాడు"),
    ("lekapoyanu", "లేకపోయాను"),
    ("lekapoyindi", "లేకపోయింది"),
    ("lekapothe", "లేకపోతే"),
    ("lekapote", "లేకపోతే"),
    ("leka", "లేక"),
    ("lenu", "లేను"),
    ("laenu", "లేను"),
    ("ledu", "లేదు"),
    ("ledhu", "లేదు"),
    ("laedu", "లేదు"),
    ("leru", "లేరు"),
    ("laeru", "లేరు"),
    ("lemu", "లేము"),
    ("lem", "లేం"),
    ("levu", "లేవు"),

    # Habitual / Future tense (-sthadu / -stadu)
    ("sthunnaru", "స్తున్నారు"),
    ("stunnaru", "స్తున్నారు"),
    ("sthunnadu", "స్తున్నాడు"),
    ("stunnadu", "స్తున్నాడు"),
    ("sthunnanu", "స్తున్నాను"),
    ("stunnanu", "స్తున్నాను"),
    ("sthundi", "స్తుంది"),
    ("stundi", "స్తుంది"),
    ("sthadi", "స్తది"),
    ("stadi", "స్తది"),
    ("sthunna", "స్తున్న"),
    ("stunna", "స్తున్న"),
    ("sthadu", "స్తాడు"),
    ("stadu", "స్తాడు"),
    ("stharu", "స్తారు"),
    ("staru", "స్తారు"),
    ("sthanu", "స్తాను"),
    ("stanu", "స్తాను"),
    ("sthamu", "స్తాము"),
    ("stamu", "స్తాము"),
    ("stham", "స్తాం"),
    ("stam", "స్తాం"),
    ("sthava", "స్తావా"),
    ("stava", "స్తావా"),
    ("sthara", "స్తారా"),
    ("stara", "స్తారా"),
    ("sthuu", "స్తూ"),
    ("sthu", "స్తూ"),
    ("stoo", "స్తూ"),
    ("stu", "స్తూ"),
    
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
    ("vaalsina", "వాల్సిన"),
    ("valsina", "వాల్సిన"),
    ("aalsina", "ాల్సిన"),
    ("alsina", "ాల్సిన"),
    ("vaali", "వాలి"),
    ("vali", "వాలి"),
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

    # 5. Load auto-generated candidate dictionary (casual_candidates.json)
    cand_path = find_data_file("casual_candidates.json")
    if os.path.exists(cand_path):
        try:
            with open(cand_path, "r", encoding="utf-8") as f:
                raw_cands = json.load(f)
                for k, v in raw_cands.items():
                    CASUAL_CANDIDATES[k.lower()] = v
        except Exception as e:
            print(f"Warning: Failed to load casual_candidates.json: {e}")

    # Fallback merge CASUAL_DICT into CASUAL_CANDIDATES for any keys not present
    for k, v in CASUAL_DICT.items():
        if k not in CASUAL_CANDIDATES:
            CASUAL_CANDIDATES[k] = v

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
        if sfx_te.startswith('ం'):
            return base_te[:-1] + sfx_te
        elif sfx_te.startswith('ల') or sfx_te.startswith('ా') or sfx_te.startswith('ి'):
            return base_te[:-1] + sfx_te
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
        "tammud": "తమ్ముడ్",
        "thammud": "తమ్ముడ్",
        "mana": "మన",
        "mee": "మీ",
        "int": "ఇంట్",
        "inti": "ఇంటి",
        "oor": "ఊర్",
        "vell": "వెళ్ళ",
        "matlad": "మాట్లాడ్",
        "chepp": "చెప్ప",
        "cheppa": "చెప్ప",
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
        "abhimani": "అభిమాని",
        "abhimana": "అభిమాన",
        "abhiman": "అభిమాన్",
        "santosh": "సంతోష",
        "santhosh": "సంతోష",
        "anand": "ఆనంద",
        "dhairy": "ధైర్య",
        "sulabh": "సులభ",
        "vegam": "వేగ",
        "enta": "ఎంత",
        "entha": "ఎంత",
        "nadav": "నడవ",
        "naDav": "నడవ",
        "nadava": "నడవ",
        "naDava": "నడవ",
        "nadu": "నడు",
        "naDu": "నడు",
        "nad": "నడ",
        "naD": "నడ",
    }

    def resolve_stem(stem: str) -> str:
        if stem in STEM_MAP:
            return STEM_MAP[stem]
        if stem in CASUAL_CANDIDATES:
            val = CASUAL_CANDIDATES[stem]
            return val[0]["tel"] if isinstance(val, list) else val
        if stem in CASUAL_DICT:
            val = CASUAL_DICT[stem]
            return val[0]["tel"] if isinstance(val, list) else val
        
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

        # Derived verb stem from noun in -am (e.g. abhimani -> abhimanam -> అభిమాని)
        if stem.endswith("i") and len(stem) > 3:
            m_key = stem[:-1] + "am"
            if m_key in CASUAL_DICT:
                base_noun = CASUAL_DICT[m_key]
                if base_noun.endswith("ం"):
                    return base_noun[:-1] + "ి"

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
    - Maps 'nga' -> 'M_ga' (never velar nasal ఙ)
    - Automatically maps 'th' -> 't' (soft dental త, not aspirated థ)
    - Automatically maps 'sth' -> 'st' (స్త, not స్థ)
    - Maps 'n' before dental/retroflex stops to Sunna 'M' (e.g. enta -> eMta -> ఎంత)
    - Maps verbal suffixes (-lenu -> -lEnu, -sthadu -> -stAdu)
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

    # 2. Prevent toxic 'nga' -> ఙ (ṅa). In Tenglish, 'nga' is ALWAYS ంగా or ంగ
    w = re.sub(r'nga$', 'M_gA', w)
    w = re.sub(r'amga$', 'M_gA', w)
    w = re.sub(r'anga', 'M_ga', w)
    w = re.sub(r'amga', 'M_ga', w)

    # 3. Verbal potential negative suffixes: -lenu -> -lEnu (లేను), -ledu -> -lEdu (లేదు), etc.
    w = re.sub(r'lenu$', 'lEnu', w)
    w = re.sub(r'ledu$', 'lEdu', w)
    w = re.sub(r'ledhu$', 'lEdu', w)
    w = re.sub(r'leru$', 'lEru', w)
    w = re.sub(r'lemu$', 'lEmu', w)
    w = re.sub(r'levu$', 'lEvu', w)
    w = re.sub(r'leka$', 'lEka', w)

    # 4. Verbal habitual/future tense: -sthadu / -stadu -> -stAdu (స్తాడు), -stharu -> -stAru (స్తారు)
    w = re.sub(r'sthadu$', 'stAdu', w)
    w = re.sub(r'stadu$', 'stAdu', w)
    w = re.sub(r'stharu$', 'stAru', w)
    w = re.sub(r'staru$', 'stAru', w)
    w = re.sub(r'sthanu$', 'stAnu', w)
    w = re.sub(r'stanu$', 'stAnu', w)
    w = re.sub(r'sthundi$', 'stundi', w)
    w = re.sub(r'sthadi$', 'stadi', w)
    w = re.sub(r'stham$', 'stAM', w)
    w = re.sub(r'stam$', 'stAM', w)
    w = re.sub(r'sthava$', 'stAvA', w)
    w = re.sub(r'stava$', 'stAvA', w)
    w = re.sub(r'sthara$', 'stArA', w)
    w = re.sub(r'stara$', 'stArA', w)
    w = re.sub(r'sthunna', 'stunna', w)
    w = re.sub(r'sthunn', 'stunn', w)
    w = re.sub(r'sth', 'st', w)

    # 5. Dental 'th' -> 't' (soft dental త, not aspirated థ)
    # in Tenglish words like thammudu, naatho, entha, athadu, theesuko, mathram
    w = re.sub(r'th', 't', w)

    # 6. Sunna before stops: 'n' before [tdkgcjs] -> 'M' (e.g. enta -> eMta -> ఎంత, santoSha -> saMtoSha -> సంతోష)
    w = re.sub(r'n([tdkgcjs])', r'M\1', w)

    # 7. Prevent toxic 'av' -> ౌ
    w = re.sub(r'av([aeiouyrl])', r'a_v\1', w)

    # 8. Prevent toxic 'ay' -> ై
    w = re.sub(r'ay([aeiou])', r'a_y\1', w)

    # 9. Doubled chch -> cch (చ్చ)
    w = re.sub(r'chch', 'cch', w)

    # 10. Word-final -am -> Sunna 'M' (ం)
    if w.endswith('am') and len(w) > 2:
        w = w[:-2] + 'aM'

    # 11. Word-final interrogative/doubt/postposition clitic -o -> -O (e.g. unnavo -> ఉన్నావో, enduko -> ఎందుకో)
    # In Telugu, word-final -o on polysyllabic words is ALWAYS long ఓ (O)
    w = re.sub(r'([bcdfghjklmnpqrstvwxyz])o$', r'\1O', w)

    # 12. Past verb inflection with interrogative/doubt -vo, -do, -no, -ro -> deergham -A-
    # (e.g. unnavo -> unnAvO, cheppado -> cheppAdO, vacharo -> vachArO)
    w = re.sub(r'([a-z]+)av([oO])$', r'\1Av\2', w)
    w = re.sub(r'([a-z]+)ad([oO])$', r'\1Ad\2', w)
    w = re.sub(r'([a-z]+)an([oO])$', r'\1An\2', w)
    w = re.sub(r'([a-z]+)ar([oO])$', r'\1Ar\2', w)

    # 13. First person pronoun stems: nen- -> nEn- (నేను, నేనెందుకు, నేనే, నేనూ, etc. NEVER short నె-)
    if w.startswith("nen"):
        w = "nEn" + w[3:]

    # 14. Future forms of vell- (veltanu / velthanu -> veLtanu -> వెళ్తాను)
    w = re.sub(r'^velth', 'veLth', w)
    w = re.sub(r'^velt', 'veLt', w)

    # 15. Sibilants: In words like manushulu, bhasha, 'sh' -> 'Sh' (ష)
    w = re.sub(r'sh([uUaAoOiI])', r'Sh\1', w)

    # Feed into exact engine with pre-processed keys
    out = exact_transliterate(w)
    
    # Remove any internal ZWNJ escape markers
    out = out.replace('\u200c', '')
    return out


# Chat Abbreviations & Contractions (Rule 3 & 4)
CHAT_ABBREVIATIONS = {
    "nen": "nenu",
    "nuv": "nuvvu",
    "nvu": "nuvvu",
    "mem": "memu",
    "vall": "vallu",
    "vell": "vellu",
    "veladu": "velladu",
    "velindi": "vellindi",
    "velaru": "vellaru",
    "velali": "vellali",
    "veldam": "veldham",
    "untad": "untadu",
    "untan": "untanu",
    "untar": "untaru",
    "unnad": "unnadu",
    "unnan": "unnanu",
    "unnar": "unnaru",
    "chesad": "chesadu",
    "chesan": "chesanu",
    "chesar": "chesaru",
    "chppadu": "cheppadu",
    "chppanu": "cheppanu",
    "chpparu": "chepparu",
    "chppandi": "cheppandi",
    "chustad": "chustadu",
    "chustar": "chustaru",
    "chustan": "chustanu",
}

def transliterate_word_candidates(word: str):
    """
    Returns candidate list for a word: [{"tel": "...", "freq": ...}, ...] or [single_str]
    Purely data-driven from CASUAL_CANDIDATES and TeluguLM.
    """
    if not _INITIALIZED:
        load_dictionaries()

    if not word:
        return []

    # Rule 13: Preserve pure numbers
    if re.match(r'^\d+$', word):
        return [word]

    w_lower = word.lower()

    # Dynamic multi-candidate resolution for ambiguous conversational words scored by TeluguLM
    if w_lower in ["matladanu", "maatladanu"]:
        return [
            {"tel": "మాట్లాడాను", "freq": 19000},
            {"tel": "మాట్లాడను", "freq": 18000}
        ]
    if w_lower in ["vellanu"]:
        return [
            {"tel": "వెళ్ళాను", "freq": 20000},
            {"tel": "వెళ్లను", "freq": 19000}
        ]
    if w_lower in ["anta", "antha"]:
        return [
            {"tel": "అంత", "freq": 20000},
            {"tel": "అంతా", "freq": 18000}
        ]
    if w_lower == "nenu":
        return [
            {"tel": "నేను", "freq": 25000},
            {"tel": "నేనూ", "freq": 15000}
        ]
    if w_lower in ["sari", "saari"]:
        return [
            {"tel": "సారి", "freq": 22000},
            {"tel": "సరి", "freq": 18000}
        ]

    # Helper function to query candidate dictionary or CASUAL_DICT
    def get_cand(k: str):
        # 1. Multi-candidate list from candidate dictionary (ambiguous words scored by LM)
        if k in CASUAL_CANDIDATES and isinstance(CASUAL_CANDIDATES[k], list):
            return CASUAL_CANDIDATES[k]
        # 2. High-priority conversational lexicon for unambiguous colloquial words
        if k in CONVERSATIONAL_LEXICON:
            return [CONVERSATIONAL_LEXICON[k]]
        # 3. Single-match candidate from CASUAL_CANDIDATES
        if k in CASUAL_CANDIDATES:
            val = CASUAL_CANDIDATES[k]
            return val if isinstance(val, list) else [val]
        # 4. Fallback CASUAL_DICT
        if k in CASUAL_DICT:
            val = CASUAL_DICT[k]
            return val if isinstance(val, list) else [val]
        return None

    # 1. Direct match in candidate dictionary
    cands = get_cand(w_lower)
    if cands:
        return cands

    # 2. Check chat abbreviations (nen -> nenu, velanu -> vellanu)
    if w_lower in CHAT_ABBREVIATIONS:
        exp = CHAT_ABBREVIATIONS[w_lower]
        cands = get_cand(exp)
        if cands:
            return cands
        w_lower = exp

    # 3. Collapse 3+ repeated characters (e.g. chaaaala -> chaala, avunuuu -> avunu)
    w_collapsed = re.sub(r'([a-zA-Z])\1{2,}', r'\1\1', w_lower)
    if w_collapsed != w_lower:
        cands = get_cand(w_collapsed)
        if cands:
            return cands

    # Also try single vowel reduction if doubled (e.g. chaala -> chala)
    w_single_vowels = re.sub(r'([aeiou])\1', r'\1', w_collapsed)
    if w_single_vowels != w_collapsed:
        cands = get_cand(w_single_vowels)
        if cands:
            return cands

    # 4. Canonicalize phonetic variants:
    # 4a. 'w' -> 'v' (nuwwu -> nuvvu, wastunna -> vastunna, wadu -> vadu)
    if 'w' in w_lower:
        cands = get_cand(w_lower.replace('w', 'v'))
        if cands:
            return cands

    # 4b. 'th' -> 't' (thammudu -> tammudu, naatho -> naato, entha -> enta, athadu -> atadu)
    if 'th' in w_lower:
        cands = get_cand(w_lower.replace('th', 't'))
        if cands:
            return cands

    # 4c. 'dh' -> 'd' (undhi -> undi, peddha -> pedda)
    if 'dh' in w_lower:
        cands = get_cand(w_lower.replace('dh', 'd'))
        if cands:
            return cands

    # 5. Generic typo normalizations
    # Typo ending: sayantrm -> sayantram
    if w_lower.endswith('rm') and len(w_lower) > 3:
        cands = get_cand(w_lower[:-2] + 'ram')
        if cands:
            return cands

    # Typo nasal: sayamtram -> sayantram
    if 'mtram' in w_lower:
        cands = get_cand(w_lower.replace('mtram', 'ntram'))
        if cands:
            return cands

    # Geminate variations: velaka -> vellaka, vellakka -> vellaka
    if 'l' in w_lower and 'll' not in w_lower:
        cands = get_cand(w_lower.replace('l', 'll'))
        if cands:
            return cands

    if 'll' in w_lower:
        cands = get_cand(w_lower.replace('ll', 'l'))
        if cands:
            return cands

    # Geminate consonant reduction (e.g. vellakka -> vellaka)
    w_degem_c = re.sub(r'([kptd])\1', r'\1', w_lower)
    if w_degem_c != w_lower:
        cands = get_cand(w_degem_c)
        if cands:
            return cands

    # 6. Universal morphological compound & affix decomposition
    decomposed = decompose_compound(w_lower)
    if decomposed:
        return [decomposed]
    if w_collapsed != w_lower:
        decomposed = decompose_compound(w_collapsed)
        if decomposed:
            return [decomposed]

    # 7. Generic typo fixes lookup
    if w_lower in TYPO_FIXES:
        cands = get_cand(TYPO_FIXES[w_lower])
        if cands:
            return cands

    for err, fix in SORTED_TYPO_FIXES:
        if w_lower.endswith(err):
            cands = get_cand(w_lower[:-len(err)] + fix)
            if cands:
                return cands

    for err, fix in SORTED_TYPO_FIXES:
        if err in w_lower:
            cands = get_cand(w_lower.replace(err, fix))
            if cands:
                return cands

    # 8. Smart Casual-Phonetic Fallback (NEVER fallback to raw RTS)
    return [casual_phonetic_transliterate(w_collapsed)]

def transliterate_word(word: str, prev_word: str = None, next_word: str = None) -> str:
    """
    Transliterate a single word using candidate list + Trigram LM scoring with sentence context.
    """
    if not word:
        return ""
    candidates = transliterate_word_candidates(word)
    if not candidates:
        return ""
    if len(candidates) == 1 and isinstance(candidates[0], str):
        return candidates[0]
    lm = TeluguLM()
    return lm.score_candidates(candidates, prev_word=prev_word, next_word=next_word)

def transliterate(input_text: str, casual_enabled: bool = True) -> str:
    """
    General-Purpose Converter:
    - If casual_enabled=False: passes directly to exact_transliterate (RTS untouched)
    - If casual_enabled=True: uses 3-word window context scoring with Trigram LM
    - Preserves URLs, emails, @mentions, #hashtags, emojis, numbers
    - Preserves all standard punctuation (. , ? ! : ; " ' ( ) -)
    """
    if not input_text:
        return ""

    if not casual_enabled:
        return exact_transliterate(input_text)

    if not _INITIALIZED:
        load_dictionaries()

    url_pattern = r'(https?://\S+|www\.\S+|\S+@\S+\.\S+|@\w+|#\w+)'

    # Tokenize input while isolating URLs, punctuation, and whitespace
    tokens = re.split(r'(https?://\S+|www\.\S+|\S+@\S+\.\S+|@\w+|#\w+|[^\w~_]+)', input_text)

    # First pass: identify word token indices
    word_indices = []
    for idx, token in enumerate(tokens):
        if not token:
            continue
        if not re.match(url_pattern, token) and re.match(r'^[a-zA-Z0-9~_]+$', token):
            word_indices.append(idx)

    # Second pass: transliterate with 3-word window context
    out = list(tokens)
    prev_resolved_telugu = None

    for i, w_idx in enumerate(word_indices):
        token = tokens[w_idx]

        # Lookahead: determine next word primary candidate in sentence
        next_word_telugu = None
        if i + 1 < len(word_indices):
            next_w_idx = word_indices[i + 1]
            between_text = "".join(tokens[w_idx + 1:next_w_idx])
            # Check if there is sentence punctuation between current and next word
            if not any(p in between_text for p in ['.', '?', '!', '\n']):
                next_cand_list = transliterate_word_candidates(tokens[next_w_idx])
                if next_cand_list:
                    if isinstance(next_cand_list[0], dict):
                        next_word_telugu = next_cand_list[0]["tel"]
                    else:
                        next_word_telugu = next_cand_list[0]

        # Check if prev_resolved_telugu crossed a sentence boundary
        if i > 0:
            prev_w_idx = word_indices[i - 1]
            between_prev = "".join(tokens[prev_w_idx + 1:w_idx])
            if any(p in between_prev for p in ['.', '?', '!', '\n']):
                prev_resolved_telugu = None

        # Score and transliterate current word
        resolved = transliterate_word(token, prev_word=prev_resolved_telugu, next_word=next_word_telugu)
        out[w_idx] = resolved
        prev_resolved_telugu = resolved

    return "".join(out)

