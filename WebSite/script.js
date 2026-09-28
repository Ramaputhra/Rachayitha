// --- Official Download URLs (Vercel Blob Storage CDN) ---
window.RACHAYITHA_DOWNLOADS = {
  installer: "https://hoahsw3mekzqivuy.public.blob.vercel-storage.com/Rachayitha_Setup.exe",
  portable: "https://github.com/Ramaputhra/Rachayitha/releases/download/v1.0.0/Rachayitha.exe"
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
function transliterate(text) {
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

  // A. Live Transliteration Playground
  if (demoInput && demoOutput) {
    const updateDemo = () => {
      const text = demoInput.value;
      if (!text.trim()) {
        demoOutput.textContent = "తెలుగులో రాయండి...";
        demoOutput.style.opacity = "0.4";
      } else {
        demoOutput.textContent = transliterate(text);
        demoOutput.style.opacity = "1";
      }
    };

    demoInput.addEventListener("input", updateDemo);
    updateDemo(); // initial run
  }

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
    if (window.innerWidth > 868 && siteHeader && siteHeader.classList.contains("nav-open")) {
      closeMobileNav();
    }
  });

  // --- 4. Analytics & Conversion Tracking ---
  function trackEvent(name, data = {}) {
    if (window.va) {
      window.va('event', { name, ...data });
    }
    console.log(`[Rachayitha Analytics] ${name}`, data);
  }

  // Track all .exe download button clicks
  document.querySelectorAll('a[href$=".exe"]').forEach(link => {
    link.addEventListener("click", () => {
      const fileName = link.getAttribute("href").split("/").pop();
      trackEvent("app_download", {
        file: fileName,
        platform: "windows"
      });
    });
  });

  // Track GitHub visits
  document.querySelectorAll('a[href*="github.com"]').forEach(link => {
    link.addEventListener("click", () => {
      trackEvent("github_visit");
    });
  });
});

