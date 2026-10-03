// --- Official Download URLs (Vercel Blob Storage CDN & GitHub Releases v2.0) ---
window.RACHAYITHA_DOWNLOADS = {
  installer: "https://hoahsw3mekzqivuy.public.blob.vercel-storage.com/Rachayitha_Setup.exe",
  installer_v2: "https://hoahsw3mekzqivuy.public.blob.vercel-storage.com/Rachayitha_Setup.exe",
  portable: "https://github.com/Ramaputhra/Rachayitha/releases/download/v2.0.0/Rachayitha_v2.exe",
  portable_v2: "https://github.com/Ramaputhra/Rachayitha/releases/download/v2.0.0/Rachayitha_v2.exe"
};

// --- 1. Authentic Telugu Rules Engine ---
const VIRAMA = '్';
const ZWNJ = '\u200c';

const CONSONANTS_MAP = {
  // Ligatures & Conjuncts
  "ksha": "క్ష", "Ksha": "క్ష", "kSha": "క్ష", "KSHA": "క్ష",
  "ksh": "క్ష", "Ksh": "క్ష", "kSh": "క్ష", "KSH": "క్ష",
  "jnya": "జ్ఞ", "Jnya": "జ్ఞ", "dnya": "జ్ఞ", "Dnya": "జ్ఞ", "gnya": "జ్ఞ",
  "nga": "ఙ", "~g": "ఙ",
  "nya": "ఞ", "~n": "ఞ",
  "yy": "య్య",

  // Velars
  "kh": "ఖ", "Kh": "ఖ", "KH": "ఖ", "K": "ఖ",
  "k": "క",
  "gh": "ఘ", "Gh": "ఘ", "GH": "ఘ", "G": "ఘ",
  "g": "గ",

  // Palatals
  "ch": "చ", "Ch": "ఛ", "CH": "ఛ", "c": "చ", "C": "ఛ",
  "jh": "ఝ", "Jh": "ఝ", "JH": "ఝ", "J": "ఝ",
  "j": "జ",

  // Retroflexes
  "Th": "ఠ", "TH": "ఠ",
  "T": "ట",
  "Dh": "ఢ", "DH": "ఢ",
  "D": "డ",
  "N": "ణ",

  // Dentals
  "th": "థ",
  "t": "త",
  "dh": "ధ",
  "d": "ద",
  "n": "న",

  // Labials
  "ph": "ఫ", "Ph": "ఫ", "PH": "ఫ", "P": "ఫ", "f": "ఫ", "F": "ఫ",
  "p": "ప",
  "bh": "భ", "Bh": "భ", "BH": "భ", "B": "భ",
  "b": "బ",
  "m": "మ",

  // Semivowels & Liquids
  "y": "య", "Y": "య",
  "r": "ర",
  "l": "ల",
  "v": "వ", "w": "వ", "V": "వ", "W": "వ",
  "L": "ళ",
  "R": "ఱ",

  // Sibilants & Aspirate
  "sh": "శ", "Sh": "ష", "SH": "ష", "S": "శ",
  "s": "స",
  "h": "హ"
};

// Vowel Modifiers (Guninthalu Matras)
const VOWEL_MODS = {
  "aa": "ా", "A": "ా",
  "a": "",     // Inherent vowel: removes halant/virama
  "ii": "ీ", "I": "ీ", "ee": "ీ",
  "i": "ి",
  "uu": "ూ", "U": "ూ", "oo": "ూ",
  "u": "ు",
  "R^I": "ౄ", "RU": "ౄ",
  "R^i": "ృ", "Ru": "ృ",
  "E": "ే", "ea": "ే",
  "e": "ె",
  "ai": "ై", "ay": "ై",
  "O": "ో", "oa": "ో",
  "o": "ొ",
  "au": "ౌ", "ou": "ౌ", "av": "ౌ"
};

// Independent Vowels (అచ్చులు)
const INDEPENDENT_VOWELS = {
  "aa": "ఆ", "A": "ఆ",
  "a": "అ",
  "ii": "ఈ", "I": "ఈ", "ee": "ఈ",
  "i": "ఇ",
  "uu": "ఊ", "U": "ఊ", "oo": "ఊ",
  "u": "ఉ",
  "R^I": "ౠ", "RU": "ౠ",
  "R^i": "ఋ", "Ru": "ఋ",
  "E": "ఏ", "ea": "ఏ",
  "e": "ఎ",
  "ai": "ఐ", "ay": "ఐ",
  "O": "ఓ", "oa": "ఓ",
  "o": "ఒ",
  "au": "ఔ", "ou": "ఔ", "av": "ఔ"
};

// Special Markers
const SPECIAL_MAP = {
  "MDI": "ండి",
  "MDi": "ండి",
  "mdi": "ండి",
  "M": "ం",
  "H": "ః",
  "~": VIRAMA,
  "_": ZWNJ
};

// Pre-sort keys descending by length for greedy prefix matches
const SORTED_SPECIAL = Object.keys(SPECIAL_MAP).sort((a, b) => b.length - a.length);
const SORTED_CONSONANTS = Object.keys(CONSONANTS_MAP).sort((a, b) => b.length - a.length);
const SORTED_VOWEL_MODS = Object.keys(VOWEL_MODS).sort((a, b) => b.length - a.length);
const SORTED_INDEP_VOWELS = Object.keys(INDEPENDENT_VOWELS).sort((a, b) => b.length - a.length);

// Common Tenglish colloquial shortcuts to ensure both casual and strict transliteration work
const WORD_OVERRIDES = {
  "namaskaaram": "నమస్కారం",
  "namaskaram": "నమస్కారం",
  "namaskaaraM": "నమస్కారం",
  "namaskaraM": "నమస్కారం",
  "namaskAram": "నమస్కారం",
  "namaskAraM": "నమస్కారం",
  "namaskaaramu": "నమస్కారము",
  "namaskaramu": "నమస్కారము",
  "rachayitha": "రచయిత",
  "rachayita": "రచయిత",
  "tho": "తో",
  "tO": "తో",
  "telugulo": "తెలుగులో",
  "telugulO": "తెలుగులో",
  "type": "టైప్",
  "taip": "టైప్",
  "Taip": "టైప్",
  "cheyandi": "చేయండి",
  "chEyandi": "చేయండి",
  "cheyaMDI": "చేయండి",
  "chEyaMDI": "చేయండి",
  "cheyyandi": "చేయండి",
  "chEyyaMDI": "చేయండి",
  "chEyyandi": "చేయండి"
};
const SORTED_WORD_OVERRIDES = Object.keys(WORD_OVERRIDES).sort((a, b) => b.length - a.length);

/**
 * Halant-First Authentic Transliteration Engine matching Rachayitha's Desktop Code
 */
/**
 * Classic Halant-First Authentic Transliteration Engine (RTS High-Key Mode)
 */
function exactTransliterate(text) {
  if (!text) return "";
  let out = "";
  let i = 0;
  const n = text.length;

  while (i < n) {
    const sliceText = text.slice(i);

    // 0. Word-level overrides at word boundary
    const isWordStart = (i === 0 || /[\s.,!?;:()\[\]{}"'\-]/.test(text[i - 1]));
    if (isWordStart) {
      let matchedOverride = null;
      for (const word of SORTED_WORD_OVERRIDES) {
        if (sliceText.toLowerCase().startsWith(word.toLowerCase())) {
          const nextChar = sliceText[word.length];
          if (!nextChar || /[\s.,!?;:()\[\]{}"'\-]/.test(nextChar)) {
            matchedOverride = word;
            break;
          }
        }
      }
      if (matchedOverride) {
        out += WORD_OVERRIDES[matchedOverride];
        i += matchedOverride.length;
        continue;
      }
    }

    // 1. Check Special Markers (e.g. MDI -> ండి, M -> ం, H -> ః)
    let matchedSpecial = null;
    for (const sm of SORTED_SPECIAL) {
      if (sliceText.startsWith(sm)) {
        matchedSpecial = sm;
        break;
      }
    }
    if (matchedSpecial) {
      out += SPECIAL_MAP[matchedSpecial];
      i += matchedSpecial.length;
      continue;
    }

    // 2. Check Consonants
    let matchedCons = null;
    for (const ck of SORTED_CONSONANTS) {
      if (sliceText.startsWith(ck)) {
        matchedCons = ck;
        break;
      }
    }

    if (matchedCons) {
      const base = CONSONANTS_MAP[matchedCons];
      const afterCons = text.slice(i + matchedCons.length);

      // If key already ended in inherent vowel like 'ksha'
      if (matchedCons.endsWith('a') && matchedCons.length > 2) {
        out += base;
        i += matchedCons.length;
        continue;
      }

      // Check if vowel modifier follows
      let matchedVmod = null;
      for (const vk of SORTED_VOWEL_MODS) {
        if (afterCons.startsWith(vk)) {
          matchedVmod = vk;
          break;
        }
      }

      if (matchedVmod) {
        if (matchedVmod === 'a') {
          // Inherent vowel 'a' removes virama, forming base consonant (e.g. n + a -> న)
          out += base;
        } else {
          out += base + VOWEL_MODS[matchedVmod];
        }
        i += matchedCons.length + matchedVmod.length;
      } else {
        // Halant-first: No vowel follows -> attach virama (e.g. n -> న్, k -> క్)
        out += base + VIRAMA;
        i += matchedCons.length;
      }
      continue;
    }

    // 3. Check Independent Vowels (at start of text or after space/vowel)
    let matchedIndep = null;
    for (const ivk of SORTED_INDEP_VOWELS) {
      if (sliceText.startsWith(ivk)) {
        matchedIndep = ivk;
        break;
      }
    }

    if (matchedIndep) {
      out += INDEPENDENT_VOWELS[matchedIndep];
      i += matchedIndep.length;
      continue;
    }

    // 4. Verbatim passthrough for punctuation, symbols, whitespace
    out += text[i];
    i += 1;
  }

  return out;
}

// ==========================================================================
// Casual Typing Engine (Colloquial Lexicon + Morphological Sandhi + Phonetic)
// 100% Matching Rachayitha Desktop Engine
// ==========================================================================

const CONVERSATIONAL_LEXICON = {
  // --- Sentential Benchmark Core ---
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
  "phone": "ఫోన్", "phon": "ఫోన్", "fone": "ఫోన్", "fon": "ఫోన్",
  "samayamlo": "సమయంలో", "samayaniki": "సమయానికి", "samayam": "సమయం",
  "cheppu": "చెప్పు",
  "inko": "ఇంకో", "inkosari": "ఇంకోసారి", "sari": "సారి", "saari": "సారి",
  "vellanu": "వెళ్లను", "velanu": "వెళ్లను",
  "kopanga": "కోపంగా", "kopam": "కోపం", "anta": "అంత", "antha": "అంత",
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

  // --- Pronouns & Demonstratives ---
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

  // --- Time & Calendar Adverbs ---
  "eroju": "ఈరోజు", "eeroju": "ఈరోజు", "repu": "రేపు", "ninna": "నిన్న", "monna": "మొన్న",
  "ellundi": "ఎల్లుండి", "ippude": "ఇప్పుడే", "eppudo": "ఎప్పుడో", "appude": "అప్పుడే",
  "roju": "రోజు", "roojuu": "రోజు", "rojulu": "రోజులు", "samvatsaram": "సంవత్సరం",
  "nela": "నెల", "vaaram": "వారం", "udayam": "ఉదయం", "madhyahnam": "మధ్యాహ్నం",
  "raatri": "రాత్రి", "shubharatri": "శుభరాత్రి", "malli": "మళ్ళీ", "mallee": "మళ్ళీ",
  "tvaraga": "త్వరగా", "mundu": "ముందు", "munduku": "ముందుకు", "venuka": "వెనుక", "venakki": "వెనక్కి",

  // --- Question Words (ప్రశ్నార్థకాలు) ---
  "ela": "ఎలా", "elaa": "ఎలా", "ekkada": "ఎక్కడ", "ekkadaa": "ఎక్కడ",
  "akkada": "అక్కడ", "ikkada": "ఇక్కడ", "enduku": "ఎందుకు", "anduku": "అందుకు",
  "emiti": "ఏమిటి", "enti": "ఏంటి", "em": "ఏం", "eedi": "ఏది", "evaru": "ఎవరు",
  "entha": "ఎంత", "enni": "ఎన్ని",

  // --- Affirmations & Negations ---
  "avunu": "అవును", "avnu": "అవును", "kadu": "కాదు", "kaadu": "కాదు",
  "ledu": "లేదు", "ledhu": "లేదు", "laedu": "లేదు", "undi": "ఉంది", "undhi": "ఉంది",
  "unnaru": "ఉన్నారు", "unnanu": "ఉన్నాను", "unnadu": "ఉన్నాడు", "unnadi": "ఉన్నది", "unnamu": "ఉన్నాము", "unnam": "ఉన్నాం", "unnavu": "ఉన్నావు", "unnara": "ఉన్నారా",
  "bagundi": "బాగుంది", "bagundhi": "బాగుంది", "baga": "బాగా", "baaga": "బాగా",
  "nijam": "నిజం", "abaddham": "అబద్ధం", "sare": "సరే", "alage": "అలాగే",

  // --- Common Verbs (Inflected Conversational Forms) ---
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

  // --- Family & People ---
  "amma": "అమ్మ", "nanna": "నాన్న", "talli": "తల్లి", "tandri": "తండ్రి",
  "annayya": "అన్నయ్య", "anna": "అన్న", "tammudu": "తమ్ముడు", "akka": "అక్క", "chelli": "చెల్లి", "chellelu": "చెల్లెలు",
  "pillalu": "పిల్లలు", "pilla": "పిల్ల", "babu": "బాబు", "papa": "పాప",
  "koduku": "కొడుకు", "kuthuru": "కూతురు", "bharya": "భార్య", "bhatta": "భర్త",
  "snehithudu": "స్నేహితుడు", "snehitudu": "స్నేహితుడు", "snehithulu": "స్నేహితులు", "snehitulu": "స్నేహితులు", "snehitulato": "స్నేహితులతో", "snehitulatho": "స్నేహితులతో", "snehithulato": "స్నేహితులతో", "snehithulatho": "స్నేహితులతో",
  "mitrudu": "మిత్రుడు", "manishi": "మనిషి", "prajalu": "ప్రజలు",

  // --- Nouns & Everyday Objects ---
  "illu": "ఇల్లు", "ooru": "ఊరు", "badi": "బడి", "gudi": "గుడి",
  "pustakam": "పుస్తకం", "pustakalu": "పుస్తకాలు", "kalam": "కలం", "kagitham": "కాగితం",
  "annam": "అన్నం", "bhojanam": "భోజనం", "neellu": "నీళ్ళు", "neeru": "నీరు", "paalu": "పాలు",
  "pani": "పని", "panulu": "పనులు", "vishayam": "విషయం", "prashna": "ప్రశ్న", "samadhanam": "సమాధానం",
  "bhasha": "భాష", "desham": "దేశం", "raashtram": "రాష్ట్రం", "nagaram": "నగరం", "graamam": "గ్రామం",
  "varsham": "వర్షం", "gaali": "గాలి", "velugu": "వెలుగు", "cheekati": "చీకటి",
  "prema": "ప్రేమ", "sneham": "స్నేహం", "snehamto": "స్నేహంతో", "shanti": "శాంతి", "sukham": "సుఖం",
  "santosham": "సంతోషం", "kopam": "కోపం", "kopamto": "కోపంతో", "bhayam": "భయం", "dhairyam": "ధైర్యం",

  // --- Adjectives ---
  "manchi": "మంచి", "pedda": "పెద్ద", "chinna": "చిన్న", "kotha": "కొత్త", "paatha": "పాత", "pata": "పాత",
  "goppa": "గొప్ప", "teepi": "తీపి", "chaala": "చాలా", "ekkuva": "ఎక్కువ", "takkuva": "తక్కువ",
  "sulabham": "సులభం", "kashtam": "కష్టం", "istam": "ఇష్టం", "ishtam": "ఇష్టం",

  // --- Greetings & Politeness ---
  "namaskaram": "నమస్కారం", "namaskaaram": "నమస్కారం", "namaste": "నమస్తే",
  "dhanyavadalu": "ధన్యవాదాలు", "shubhodhayam": "శుభోదయం", "subhodhayam": "శుభోదయం",
  "dayachesi": "దయచేసి", "kshamanchandi": "క్షమించండి",
};

const NOUN_DECLENSIONS = [
  ["nunchi", "నుంచి"],
  ["nundi", "నుండి"],
  ["kosam", "కోసం"],
  ["looki", "లోకి"],
  ["loki", "లోకి"],
  ["looni", "లోని"],
  ["loni", "లోని"],
  ["kante", "కంటే"],
  ["thoo", "తో"],
  ["too", "తో"],
  ["tho", "తో"],
  ["to", "తో"],
  ["loo", "లో"],
  ["lo", "లో"],
  ["pai", "పై"],
  ["ki", "కి"],
  ["ku", "కు"],
];

const VERB_DECLENSIONS = [
  ["kovadam", "కోవడం"],
  ["kovali", "కోవాలి"],
  ["koni", "కొని"],
  ["kuni", "కుని"],
  ["kondi", "కోండి"],
  ["kuntunnaaru", "కుంటున్నారు"],
  ["kuntunnaru", "కుంటున్నారు"],
  ["kuntunnaanu", "కుంటున్నాను"],
  ["kuntunnanu", "కుంటున్నాను"],
  ["kuntunnaadu", "కుంటున్నాడు"],
  ["kuntunnadu", "కుంటున్నాడు"],
  ["kuntundi", "కుంటుంది"],
  ["kuntunna", "కుంటున్న"],
  ["kuntaru", "కుంటారు"],
  ["kuntadu", "కుంటాడు"],
  ["kuntanu", "కుంటాను"],
  ["kuntamu", "కుంటాము"],
  ["kuntam", "కుంటాం"],
  ["kuntuu", "కుంటూ"],
  ["kuntoo", "కుంటూ"],
  ["kuntu", "కుంటూ"],
  ["kunnaru", "కున్నారు"],
  ["kunnanu", "కున్నాను"],
  ["kunnadu", "కున్నాడు"],
  ["kunna", "కున్న"],
  ["kune", "కునే"],
  ["vasthe", "వస్తే"],
  ["vaste", "వస్తే"],
  ["ochchi", "ఒచ్చి"],
  ["ochi", "ఒచ్చి"],
  ["padali", "పడాలి"],
  ["paddanu", "పడ్డాను"],
  ["padadu", "పడ్డాడు"],
  ["padindi", "పడింది"],
  ["padaru", "పడ్డారు"],
  ["padi", "పడి"],
  ["the", "తే"],
  ["te", "తే"],
  ["aka", "ఆక"],
  ["tunnaaru", "తున్నారు"],
  ["tunnaru", "తున్నారు"],
  ["tunnaanu", "తున్నాను"],
  ["tunnanu", "తున్నాను"],
  ["tunnaadu", "తున్నాడు"],
  ["tunnadu", "తున్నాడు"],
  ["tunnayi", "తున్నాయి"],
  ["tunnaayi", "తున్నాయి"],
  ["thundi", "తుంది"],
  ["tundi", "తుంది"],
  ["thunna", "తున్న"],
  ["tunna", "తున్న"],
  ["tuu", "తూ"],
  ["too", "తూ"],
  ["tu", "తూ"],
  ["aanu", "ాను"],
  ["aadu", "ాడు"],
  ["indi", "ింది"],
  ["indhi", "ింది"],
  ["aaru", "ారు"],
  ["aamu", "ాము"],
  ["anu", "ాను"],
  ["adu", "ాడు"],
  ["aru", "ారు"],
  ["amu", "ాము"],
  ["aalsina", "ాల్సిన"],
  ["alsina", "ాల్సిన"],
  ["aali", "ాలి"],
  ["ali", "ాలి"],
  ["andi", "ండి"],
  ["amdi", "ండి"],
  ["adam", "డం"],
  ["aadam", "ాడం"],
];

const STEM_MAP = {
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
};

const TYPO_FIXES = {
  "amdi": "andi",
  "anndi": "andi",
  "andhi": "andi",
  "amdhi": "andi",
  "nndi": "ndi",
  "ndhi": "ndi",
  "nddhi": "ndi",
  "nndhi": "ndi",
  "undhi": "undi",
  "umdi": "undi",
  "unndi": "undi",
  "umdhi": "undi",
  "ledhu": "ledu",
  "lethu": "ledu",
  "laedu": "ledu",
  "leduu": "ledu",
  "vasthunna": "vastunna",
  "vastunnaa": "vastunna",
  "vastuna": "vastunna",
  "vastunnaaa": "vastunna",
  "vachchindhi": "vachchindi",
  "vellindhi": "vellindi",
  "cheppindhi": "cheppindi",
  "thunna": "tunna",
  "tunnaa": "tunna",
  "tuna": "tunna",
  "nuvu": "nuvvu",
  "nen": "nenu",
  "avnu": "avunu",
  "kadu": "kaadu",
  "bagundhi": "bagundi",
  "bagundh": "bagundi",
  "cheyandi": "cheyandi",
  "cheyyamdi": "cheyyandi",
  "choodamdi": "choodandi",
  "randhi": "randi",
  "ramdi": "randi"
};

const SORTED_TYPO_FIXES = Object.entries(TYPO_FIXES).sort((a, b) => b[0].length - a[0].length);

// Top word mappings (high frequency collision winners)
const TOP_WORD_MAPPINGS = [
  ["వస్తున్నా", ["vastunna", "vasthunna", "vastunnaa", "vastuna", "vastunnaaa"]],
  ["చెప్పండి", ["cheppandi", "cheppamdi"]],
  ["చేయండి", ["cheyandi", "cheeyandi"]],
  ["చెయ్యండి", ["cheyyandi", "cheyyamdi"]],
  ["రండి", ["randi", "randhi", "ramdi"]],
  ["చూడండి", ["choodandi", "chudandi", "chuudandi", "choodamdi"]],
  ["నువ్వు", ["nuvvu", "nuvu"]],
  ["అక్కడే", ["akkade", "akkadae"]],
  ["ఉండు", ["undu", "umdu"]],
  ["ఉంది", ["undi", "undhi", "umdi"]],
  ["లేదు", ["ledu", "ledhu", "laedu"]],
  ["బాగుంది", ["bagundi", "bagundhi", "bagundh"]],
  ["అవును", ["avunu", "avnu"]],
  ["కాదు", ["kaadu", "kadu"]],
  ["వచ్చింది", ["vachindi", "vachchindi", "vachchindhi"]],
  ["వెళ్ళింది", ["vellindi", "vellindhi"]],
];

// Initialize CASUAL_DICT with full offline dictionary if present, then high-priority mappings
const CASUAL_DICT = {};
if (typeof window !== "undefined" && window.RACHAYITHA_CASUAL_DICT && typeof window.RACHAYITHA_CASUAL_DICT === "object") {
  for (const [k, v] of Object.entries(window.RACHAYITHA_CASUAL_DICT)) {
    CASUAL_DICT[k.toLowerCase()] = v;
  }
}
for (const [telWord, romanKeys] of TOP_WORD_MAPPINGS) {
  for (const rk of romanKeys) {
    CASUAL_DICT[rk.toLowerCase()] = telWord;
  }
}
for (const [k, v] of Object.entries(CONVERSATIONAL_LEXICON)) {
  CASUAL_DICT[k.toLowerCase()] = v;
}

// Sandhi Rules Function
function applySandhi(baseTe, sfxTe, sfxEn) {
  if (!baseTe || !sfxTe) return (baseTe || "") + (sfxTe || "");

  // Case A: Base ends with Virama / Halant (e.g. మాట్లాడ్, చెప్ప్)
  if (baseTe.endsWith(VIRAMA)) {
    const consBase = baseTe.slice(0, -1);
    const vowelToMatra = {
      'అ': '', 'ఆ': 'ా', 'ఇ': 'ి', 'ఈ': 'ీ', 'ఉ': 'ు', 'ఊ': 'ూ',
      'ఎ': 'ె', 'ఏ': 'ే', 'ఐ': 'ై', 'ఒ': 'ొ', 'ఓ': 'ో', 'ఔ': 'ౌ'
    };
    const firstChar = sfxTe[0];
    if (vowelToMatra[firstChar] !== undefined) {
      return consBase + vowelToMatra[firstChar] + sfxTe.slice(1);
    } else if (['ా', 'ి', 'ీ', 'ు', 'ూ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ'].includes(firstChar)) {
      return consBase + sfxTe;
    }
  }

  // Case B: Base ends with Anusvara (Sunna 'ం')
  if (baseTe.endsWith('ం')) {
    return baseTe + sfxTe;
  }

  // Case C: Suffix starts with a matra
  if (['ా', 'ి', 'ీ', 'ు', 'ూ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ'].includes(sfxTe[0])) {
    return baseTe + sfxTe;
  }

  return baseTe + sfxTe;
}

// Morphological Compound Decomposer
function decomposeCompound(w) {
  if (w.length < 4) return null;

  function resolveStem(stem) {
    if (STEM_MAP[stem]) return STEM_MAP[stem];
    if (CASUAL_DICT[stem]) return CASUAL_DICT[stem];

    // Plural oblique stem (pillala -> pillalu -> పిల్లల)
    if (stem.endsWith("la") && stem.length > 3) {
      const nomKey = stem.slice(0, -1) + "u";
      if (CASUAL_DICT[nomKey]) {
        const nomVal = CASUAL_DICT[nomKey];
        if (nomVal.endsWith("లు")) {
          return nomVal.slice(0, -1) + "ల";
        }
      }
    }

    // Anusvara stem (snehan- -> sneham -> స్నేహం)
    if (stem.endsWith("n") && stem.length > 2) {
      const mKey = stem.slice(0, -1) + "m";
      if (CASUAL_DICT[mKey]) {
        return CASUAL_DICT[mKey];
      }
    }

    return null;
  }

  // 1. Verb Declensions
  for (const [sfxEn, sfxTe] of VERB_DECLENSIONS) {
    if (w.endsWith(sfxEn) && w.length > sfxEn.length + 1) {
      const stem = w.slice(0, -sfxEn.length);
      const baseTe = resolveStem(stem);
      if (baseTe) return applySandhi(baseTe, sfxTe, sfxEn);
    }
  }

  // 2. Noun Declensions
  for (const [sfxEn, sfxTe] of NOUN_DECLENSIONS) {
    if (w.endsWith(sfxEn) && w.length > sfxEn.length + 1) {
      const stem = w.slice(0, -sfxEn.length);
      const baseTe = resolveStem(stem);
      if (baseTe) return applySandhi(baseTe, sfxTe, sfxEn);
    }
  }

  return null;
}

// Dedicated Casual-Phonetic Fallback
function casualPhoneticTransliterate(word) {
  if (!word) return "";
  let w = word.toLowerCase();

  // 1. Retroflex clusters
  w = w.replace(/sht/g, 'ShTa');
  w = w.replace(/tl/g, 'Tla');
  w = w.replace(/dl/g, 'Dla');

  // 2. Prevent toxic 'av' -> ౌ
  w = w.replace(/av([aeiouyrl])/g, 'a_v$1');

  // 3. Prevent toxic 'ay' -> ై
  w = w.replace(/ay([aeiou])/g, 'a_y$1');

  // 4. Doubled chch -> cch (చ్చ)
  w = w.replace(/chch/g, 'cch');

  // 5. Word-final -am -> Sunna 'M' (ం)
  if (w.endsWith('am') && w.length > 2) {
    w = w.slice(0, -2) + 'aM';
  }

  // 6. Word-final postpositions & verb suffixes
  if (w.endsWith('to') || w.endsWith('tho')) {
    const pLen = w.endsWith('tho') ? 3 : 2;
    w = w.slice(0, -pLen) + 'tO';
  } else if (w.endsWith('lo') || w.endsWith('lho')) {
    const pLen = w.endsWith('lho') ? 3 : 2;
    w = w.slice(0, -pLen) + 'lO';
  } else if (w.endsWith('ko')) {
    w = w.slice(0, -2) + 'kO';
  } else if (w.endsWith('ali') && w.length > 3) {
    w = w.slice(0, -3) + 'Ali';
  } else if (w.endsWith('anu') && w.length > 3) {
    w = w.slice(0, -3) + 'Anu';
  } else if (w.endsWith('adu') && w.length > 3) {
    w = w.slice(0, -3) + 'Adu';
  } else if (w.endsWith('aru') && w.length > 3) {
    w = w.slice(0, -3) + 'Aru';
  } else if (w.endsWith('kosam') && w.length > 5) {
    w = w.slice(0, -5) + 'kOsaM';
  }

  // 7. Sibilants: sh + vowel -> Sh (ష)
  w = w.replace(/sh([uUaAoOiI])/g, 'Sh$1');

  // 8. Word-final -o clitic -> O (e.g. unnavo -> ఉన్నావో, enduko -> ఎందుకో)
  w = w.replace(/([bcdfghjklmnpqrstvwxyz])o$/, '$1O');
  w = w.replace(/([a-z]+)av([oO])$/, '$1Av$2');
  w = w.replace(/([a-z]+)ad([oO])$/, '$1Ad$2');
  w = w.replace(/([a-z]+)an([oO])$/, '$1An$2');
  w = w.replace(/([a-z]+)ar([oO])$/, '$1Ar$2');

  // 9. Pronoun nen- -> nEn- (నేను, నేనెందుకు, etc.)
  if (w.startsWith("nen")) {
    w = "nEn" + w.slice(3);
  }

  // 10. Future velt- -> veLt- (వెళ్తాను)
  w = w.replace(/^velth/, 'veLth');
  w = w.replace(/^velt/, 'veLt');

  // 11. Inherent long vowels for open syllables like 'repu', 'roju'
  w = w.replace(/^re([pbtdkmnsvlrjg])/, 'rE$1');
  w = w.replace(/^ro([pbtdkmnsvlrjg])/, 'rO$1');

  let out = exactTransliterate(w);
  out = out.replace(/\u200c/g, '');
  return out;
}

// Single word casual transliterator
function transliterateWord(word) {
  const wLower = word.toLowerCase();

  // 1 & 2. Direct lookup in CASUAL_DICT
  if (CASUAL_DICT[wLower]) {
    return CASUAL_DICT[wLower];
  }

  // 3. Morphological compound decomposition
  const decomposed = decomposeCompound(wLower);
  if (decomposed) {
    return decomposed;
  }

  // 4. Typo fixes
  if (TYPO_FIXES[wLower] && CASUAL_DICT[TYPO_FIXES[wLower]]) {
    return CASUAL_DICT[TYPO_FIXES[wLower]];
  }

  for (const [err, fix] of SORTED_TYPO_FIXES) {
    if (wLower.endsWith(err)) {
      const candidate = wLower.slice(0, -err.length) + fix;
      if (CASUAL_DICT[candidate]) {
        return CASUAL_DICT[candidate];
      }
    }
  }

  for (const [err, fix] of SORTED_TYPO_FIXES) {
    if (wLower.includes(err)) {
      const candidate = wLower.replace(err, fix);
      if (CASUAL_DICT[candidate]) {
        return CASUAL_DICT[candidate];
      }
    }
  }

  // 5. Dedicated Casual-Phonetic Fallback
  return casualPhoneticTransliterate(word);
}

// Multi-word casual transliterator
function transliterateCasual(inputText) {
  if (!inputText) return "";
  const tokens = inputText.split(/([^\w~_]+)/);
  const out = [];
  for (const token of tokens) {
    if (!token) continue;
    if (/^[a-zA-Z0-9~_]+$/.test(token)) {
      out.push(transliterateWord(token));
    } else {
      out.push(token);
    }
  }
  return out.join("");
}

/**
 * Universal Transliterate Gateway
 * @param {string} text - The input Tenglish string
 * @param {boolean} casualEnabled - Whether Casual Mode is active
 */
function transliterate(text, casualEnabled = true) {
  if (!text) return "";
  if (casualEnabled) {
    return transliterateCasual(text);
  } else {
    return exactTransliterate(text);
  }
}

// --- 2. Key Map Data ---
const KEYMAP_DATA = [
  // Vowels (Achulu)
  { eng: "a", tel: "అ", type: "vowel" },
  { eng: "aa / A", tel: "ఆ", type: "vowel" },
  { eng: "i", tel: "ఇ", type: "vowel" },
  { eng: "ii / I / ee", tel: "ఈ", type: "vowel" },
  { eng: "u", tel: "ఉ", type: "vowel" },
  { eng: "uu / U / oo", tel: "ఊ", type: "vowel" },
  { eng: "Ru", tel: "ఋ", type: "vowel" },
  { eng: "e", tel: "ఎ", type: "vowel" },
  { eng: "E / ee", tel: "ఏ", type: "vowel" },
  { eng: "ai", tel: "ఐ", type: "vowel" },
  { eng: "o", tel: "ఒ", type: "vowel" },
  { eng: "O / oo", tel: "ఓ", type: "vowel" },
  { eng: "au / ou", tel: "ఔ", type: "vowel" },
  { eng: "am / M", tel: "అం", type: "vowel" },
  { eng: "aha / H", tel: "అః", type: "vowel" },

  // Consonants (Hallulu - Halant first)
  { eng: "k", tel: "క్", type: "consonant" },
  { eng: "ka", tel: "క", type: "consonant" },
  { eng: "kh / K", tel: "ఖ్", type: "consonant" },
  { eng: "kha", tel: "ఖ", type: "consonant" },
  { eng: "g", tel: "గ్", type: "consonant" },
  { eng: "ga", tel: "గ", type: "consonant" },
  { eng: "gh / G", tel: "ఘ్", type: "consonant" },
  { eng: "ch / c", tel: "చ్", type: "consonant" },
  { eng: "cha", tel: "చ", type: "consonant" },
  { eng: "j", tel: "జ్", type: "consonant" },
  { eng: "ja", tel: "జ", type: "consonant" },
  { eng: "T", tel: "ట్", type: "consonant" },
  { eng: "Ta", tel: "ట", type: "consonant" },
  { eng: "D", tel: "డ్", type: "consonant" },
  { eng: "Da", tel: "డ", type: "consonant" },
  { eng: "N", tel: "ణ్", type: "consonant" },
  { eng: "Na", tel: "ణ", type: "consonant" },
  { eng: "t", tel: "త్", type: "consonant" },
  { eng: "ta", tel: "త", type: "consonant" },
  { eng: "d", tel: "ద్", type: "consonant" },
  { eng: "da", tel: "ద", type: "consonant" },
  { eng: "n", tel: "న్", type: "consonant" },
  { eng: "na", tel: "న", type: "consonant" },
  { eng: "p", tel: "ప్", type: "consonant" },
  { eng: "pa", tel: "ప", type: "consonant" },
  { eng: "b", tel: "బ్", type: "consonant" },
  { eng: "ba", tel: "బ", type: "consonant" },
  { eng: "bh / B", tel: "భ్", type: "consonant" },
  { eng: "bha", tel: "భ", type: "consonant" },
  { eng: "m", tel: "మ్", type: "consonant" },
  { eng: "ma", tel: "మ", type: "consonant" },
  { eng: "y", tel: "య్", type: "consonant" },
  { eng: "ya", tel: "య", type: "consonant" },
  { eng: "r", tel: "ర్", type: "consonant" },
  { eng: "ra", tel: "ర", type: "consonant" },
  { eng: "l", tel: "ల్", type: "consonant" },
  { eng: "la", tel: "ల", type: "consonant" },
  { eng: "v / w", tel: "వ్", type: "consonant" },
  { eng: "va", tel: "వ", type: "consonant" },
  { eng: "s", tel: "స్", type: "consonant" },
  { eng: "sa", tel: "స", type: "consonant" },
  { eng: "h", tel: "హ్", type: "consonant" },
  { eng: "ha", tel: "హ", type: "consonant" },

  // Conjuncts (Vatthulu & Samyukta)
  { eng: "ksha", tel: "క్ష", type: "conjunct" },
  { eng: "ksh", tel: "క్ష్", type: "conjunct" },
  { eng: "nna", tel: "న్న", type: "conjunct" },
  { eng: "kka", tel: "క్క", type: "conjunct" },
  { eng: "mma", tel: "మ్మ", type: "conjunct" },
  { eng: "tta", tel: "ట్ట", type: "conjunct" },
  { eng: "ppa", tel: "ప్ప", type: "conjunct" },
  { eng: "lla", tel: "ల్ల", type: "conjunct" },
  { eng: "jnya", tel: "జ్ఞ", type: "conjunct" },
  { eng: "shra", tel: "శ్ర", type: "conjunct" }
];

// --- 3. DOM Binding & Initialization ---
document.addEventListener("DOMContentLoaded", () => {
  const demoInput = document.getElementById("demo-input");
  const demoOutput = document.getElementById("demo-output");
  const copyBtn = document.getElementById("copy-btn");
  const keymapGrid = document.getElementById("keymap-grid");
  const searchInput = document.getElementById("keymap-search");
  const tabBtns = document.querySelectorAll(".tab-btn");

  // 0. Bind Centralized Download Links
  if (window.RACHAYITHA_DOWNLOADS) {
    document.querySelectorAll(".btn-installer-download").forEach(el => {
      if (window.RACHAYITHA_DOWNLOADS.installer) el.href = window.RACHAYITHA_DOWNLOADS.installer;
    });
    document.querySelectorAll(".btn-portable-download").forEach(el => {
      if (window.RACHAYITHA_DOWNLOADS.portable) el.href = window.RACHAYITHA_DOWNLOADS.portable;
    });
  }

  // Showcase Tab Switcher (Casual Mode vs High-Key Comparison)
  window.switchShowcaseTab = function(mode) {
    const tabCasual = document.getElementById("tab-casual-view");
    const tabCompare = document.getElementById("tab-compare-view");
    const slideCasual = document.getElementById("slide-casual");
    const slideCompare = document.getElementById("slide-compare");

    if (mode === "casual") {
      if (tabCasual) tabCasual.classList.add("active");
      if (tabCompare) tabCompare.classList.remove("active");
      if (slideCasual) slideCasual.classList.add("active");
      if (slideCompare) slideCompare.classList.remove("active");
    } else {
      if (tabCasual) tabCasual.classList.remove("active");
      if (tabCompare) tabCompare.classList.add("active");
      if (slideCasual) slideCasual.classList.remove("active");
      if (slideCompare) slideCompare.classList.add("active");
    }
  };

  // A. Live Transliteration Playground & Mode Toggle
  const casualToggle = document.getElementById("casual-toggle");
  const casualBadge = document.getElementById("casual-badge");
  const modeExplainer = document.getElementById("mode-explainer");
  const modeExplainerText = document.getElementById("mode-explainer-text");

  const isCasualActive = () => {
    return casualToggle ? casualToggle.checked : true;
  };

  let updateDemo = () => {
    if (demoInput && demoOutput) {
      const text = demoInput.value;
      if (!text.trim()) {
        demoOutput.textContent = "తెలుగులో రాయండి...";
        demoOutput.style.opacity = "0.4";
      } else {
        demoOutput.textContent = transliterate(text, isCasualActive());
        demoOutput.style.opacity = "1";
      }
    }
  };

  const updateModeUI = () => {
    const active = isCasualActive();
    if (casualBadge) {
      if (active) {
        casualBadge.className = "casual-mode-badge active";
        casualBadge.innerHTML = "⚡ Casual Mode ON";
      } else {
        casualBadge.className = "casual-mode-badge disabled";
        casualBadge.innerHTML = "⌨️ High-Key (Classic RTS)";
      }
    }
    if (modeExplainer && modeExplainerText) {
      if (active) {
        modeExplainer.className = "mode-explainer";
        modeExplainerText.innerHTML = "<strong>Casual Mode (Active):</strong> Natural lowercase Tenglish typing with 58k+ vocabulary, Telugu Sandhi conjugations, and colloquial speech. No strict Shift keys needed.";
      } else {
        modeExplainer.className = "mode-explainer disabled";
        modeExplainerText.innerHTML = "<strong>High-Key Mode (Active):</strong> Classic RTS rules with strict case sensitivity (e.g. 'mATlADAnu', 'telugulO', 'Taip', 'ShTa').";
      }
    }
    updateDemo();
  };

  if (casualToggle) {
    casualToggle.addEventListener("change", updateModeUI);
  }

  if (casualBadge) {
    casualBadge.addEventListener("click", () => {
      if (casualToggle) {
        casualToggle.checked = !casualToggle.checked;
        updateModeUI();
      }
    });
  }

  if (demoInput) {
    demoInput.addEventListener("input", updateDemo);
  }
  updateModeUI();

  // Attempt to asynchronously load extended 58,421 casual words dictionary from data folder
  fetch("data/casual_type_dict.json")
    .then(res => {
      if (res.ok) return res.json();
      throw new Error("Using integrated high-frequency lexicon.");
    })
    .then(data => {
      let count = 0;
      for (const [k, v] of Object.entries(data)) {
        const kLower = k.toLowerCase();
        if (!CASUAL_DICT[kLower]) {
          CASUAL_DICT[kLower] = v;
          count++;
        }
      }
      console.log(`[Rachayitha] Successfully loaded ${count} extended casual words from dictionary.`);
      updateDemo();
    })
    .catch(() => {
      // High-frequency lexicon & phonetic Sandhi engine already active
    });

  // B. Preset Buttons
  window.setPreset = function(text) {
    if (demoInput) {
      demoInput.value = text;
      demoInput.dispatchEvent(new Event("input"));
      demoInput.focus();
    }
  };

  // C. Clear Button
  const clearBtn = document.getElementById("clear-btn");
  if (clearBtn && demoInput) {
    clearBtn.addEventListener("click", () => {
      demoInput.value = "";
      demoInput.dispatchEvent(new Event("input"));
      demoInput.focus();
    });
  }

  // D. Copy Button
  if (copyBtn && demoOutput) {
    copyBtn.addEventListener("click", () => {
      const text = demoOutput.textContent;
      if (text && text !== "తెలుగులో రాయండి...") {
        navigator.clipboard.writeText(text).then(() => {
          const originalText = copyBtn.innerHTML;
          copyBtn.innerHTML = "✓ Copied!";
          copyBtn.style.borderColor = "var(--accent-emerald)";
          copyBtn.style.color = "var(--accent-emerald)";
          setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.borderColor = "";
            copyBtn.style.color = "";
          }, 1800);
        });
      }
    });
  }

  // E. Render Key Map Explorer
  let activeFilter = "all";
  let searchQuery = "";

  function renderKeyMap() {
    if (!keymapGrid) return;
    keymapGrid.innerHTML = "";

    const filtered = KEYMAP_DATA.filter(item => {
      const matchesType = activeFilter === "all" || item.type === activeFilter;
      const matchesSearch = !searchQuery || 
        item.eng.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.tel.includes(searchQuery);
      return matchesType && matchesSearch;
    });

    if (filtered.length === 0) {
      keymapGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-subtle); font-family: var(--font-mono);">
          No letter matches found for "${searchQuery}"
        </div>
      `;
      return;
    }

    filtered.forEach(item => {
      const card = document.createElement("div");
      card.className = "key-card";
      card.title = `Click to test '${item.eng}' in playground`;
      card.innerHTML = `
        <div class="key-english">${item.eng}</div>
        <div class="key-telugu">${item.tel}</div>
      `;
      card.addEventListener("click", () => {
        window.setPreset(item.eng);
        const playgroundEl = document.getElementById("playground");
        if (playgroundEl) {
          playgroundEl.scrollIntoView({ behavior: "smooth" });
        }
      });
      keymapGrid.appendChild(card);
    });
  }

  renderKeyMap();

  // Tabs
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.dataset.filter;
      renderKeyMap();
    });
  });

  // Search
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.trim();
      renderKeyMap();
    });
  }

  // F. Reactive Mobile Navigation Drawer
  const mobileToggle = document.getElementById("mobile-toggle");
  const navLinks = document.getElementById("nav-links");
  const navBackdrop = document.getElementById("nav-backdrop");
  const siteHeader = document.querySelector(".site-header");

  function closeMobileNav() {
    if (!siteHeader) return;
    siteHeader.classList.remove("nav-open");
    if (mobileToggle) {
      mobileToggle.setAttribute("aria-expanded", "false");
      mobileToggle.setAttribute("aria-label", "Open Navigation Menu");
    }
    document.body.classList.remove("mobile-nav-lock");
  }

  function openMobileNav() {
    if (!siteHeader) return;
    siteHeader.classList.add("nav-open");
    if (mobileToggle) {
      mobileToggle.setAttribute("aria-expanded", "true");
      mobileToggle.setAttribute("aria-label", "Close Navigation Menu");
    }
    document.body.classList.add("mobile-nav-lock");
  }

  function toggleMobileNav() {
    if (siteHeader && siteHeader.classList.contains("nav-open")) {
      closeMobileNav();
    } else {
      openMobileNav();
    }
  }

  if (mobileToggle) {
    mobileToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleMobileNav();
    });
  }

  if (navBackdrop) {
    navBackdrop.addEventListener("click", closeMobileNav);
  }

  // Auto-close drawer when clicking any link
  if (navLinks) {
    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", closeMobileNav);
    });
  }

  // Close with Esc key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && siteHeader && siteHeader.classList.contains("nav-open")) {
      closeMobileNav();
    }
  });

  // Auto-reset when resizing to desktop
  window.addEventListener("resize", () => {
    if (window.innerWidth > 1024 && siteHeader && siteHeader.classList.contains("nav-open")) {
      closeMobileNav();
    }
  });

  // --- 4. Interactive FAQ Accordion ---
  const faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach((item) => {
    const questionBtn = item.querySelector(".faq-question");
    if (!questionBtn) return;
    questionBtn.addEventListener("click", () => {
      const isActive = item.classList.contains("active");
      // Optional: close other open items for cleaner reading
      faqItems.forEach((other) => {
        if (other !== item) {
          other.classList.remove("active");
          const otherBtn = other.querySelector(".faq-question");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
        }
      });
      item.classList.toggle("active", !isActive);
      questionBtn.setAttribute("aria-expanded", !isActive ? "true" : "false");
    });
  });

  // --- 5. Vercel Web Analytics & Conversion Tracking ---
  window.trackAnalyticsEvent = function(name, data = {}) {
    if (typeof window.va === "function") {
      try {
        window.va("event", { name, ...data });
      } catch (err) {
        console.warn("[Vercel Analytics] Track warning:", err);
      }
    }
  };

  // Track all Windows Installer and Portable downloads
  document.querySelectorAll('a[href$=".exe"], .btn-installer-download').forEach(link => {
    link.addEventListener("click", () => {
      const href = link.getAttribute("href") || "";
      const isSetup = href.includes("Setup") || link.classList.contains("btn-installer-download");
      window.trackAnalyticsEvent("download_click", {
        file: isSetup ? "Rachayitha_Setup.exe" : "Rachayitha_Portable.exe",
        type: isSetup ? "installer" : "portable",
        element_id: link.id || "download_btn"
      });
    });
  });

  // Track GitHub visits
  document.querySelectorAll('a[href*="github.com"]').forEach(link => {
    link.addEventListener("click", () => {
      window.trackAnalyticsEvent("github_visit", {
        target: link.getAttribute("href")
      });
    });
  });

  // Track Blog navigation clicks
  document.querySelectorAll('a[href*="best-telugu-typing-tools"]').forEach(link => {
    link.addEventListener("click", () => {
      window.trackAnalyticsEvent("blog_read_click");
    });
  });

  // Track Demo Copy interactions
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      window.trackAnalyticsEvent("demo_text_copied");
    });
  }
});

