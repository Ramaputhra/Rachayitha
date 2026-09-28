// --- Official Download URLs (Vercel Blob Storage CDN) ---
window.RACHAYITHA_DOWNLOADS = {
  installer: "https://hoahsw3mekzqivuy.public.blob.vercel-storage.com/Rachayitha_Setup.exe",
  portable: "https://github.com/Ramaputhra/Rachayitha/releases/download/v1.0.0/Rachayitha.exe"
};

// --- 1. Authentic Telugu Rules Engine ---
const VOWELS = {
  "a": "అ", "aa": "ఆ", "A": "ఆ",
  "i": "ఇ", "ii": "ఈ", "I": "ఈ", "ee": "ఈ",
  "u": "ఉ", "uu": "ఊ", "U": "ఊ", "oo": "ఊ",
  "Ru": "ఋ", "RU": "ౠ", "R": "ఋ",
  "e": "ఎ", "ee": "ఏ", "E": "ఏ",
  "ai": "ఐ",
  "o": "ఒ", "oo": "ఓ", "O": "ఓ",
  "au": "ఔ", "ou": "ఔ"
};

const MATRAS = {
  "a": "",
  "aa": "ా", "A": "ా",
  "i": "ి",
  "ii": "ీ", "I": "ీ", "ee": "ీ",
  "u": "ు",
  "uu": "ూ", "U": "ూ", "oo": "ూ",
  "Ru": "ృ", "RU": "ౄ", "R": "ృ",
  "e": "ె",
  "ee": "ే", "E": "ే",
  "ai": "ై",
  "o": "ొ",
  "oo": "ో", "O": "ో",
  "au": "ౌ", "ou": "ౌ"
};

const CONSONANTS = {
  "k": "క్", "kh": "ఖ్", "K": "ఖ్",
  "g": "గ్", "gh": "ఘ్", "G": "ఘ్",
  "ch": "చ్", "c": "చ్", "Ch": "ఛ్",
  "j": "జ్", "jh": "ఝ్", "J": "ఝ్",
  "T": "ట్", "Th": "ఠ్",
  "D": "డ్", "Dh": "ఢ్",
  "N": "ణ్",
  "t": "త్", "th": "థ్",
  "d": "ద్", "dh": "ధ్",
  "n": "న్",
  "p": "ప్", "ph": "ఫ్", "P": "ఫ్", "f": "ఫ్",
  "b": "బ్", "bh": "భ్", "B": "భ్",
  "m": "మ్",
  "y": "య్",
  "r": "ర్",
  "l": "ల్",
  "v": "వ్", "w": "వ్",
  "sh": "శ్", "S": "శ్",
  "Sh": "ష్",
  "s": "స్",
  "h": "హ్",
  "L": "ళ్",
  "ksh": "క్ష్", "Ksh": "క్ష్", "ksha": "క్ష"
};

const SPECIALS = {
  "M": "ం",
  "H": "ః"
};

/**
 * Phonetic Transliteration implementation matching Rachayitha's Desktop Engine
 */
function transliterate(text) {
  if (!text) return "";
  let out = "";
  let i = 0;
  const n = text.length;

  while (i < n) {
    // 1. Lookahead 4 chars (e.g. ksha)
    let m4 = text.substr(i, 4);
    if (m4.toLowerCase() === "ksha") {
      out += "క్ష";
      i += 4;
      continue;
    }

    // 2. Lookahead 3 chars (e.g. ksh, nna, kka, mma)
    let m3 = text.substr(i, 3);
    if (m3.toLowerCase() === "ksh") {
      out += "క్ష్";
      i += 3;
      continue;
    }
    if (m3 === "nna") { out += "న్న"; i += 3; continue; }
    if (m3 === "kka") { out += "క్క"; i += 3; continue; }
    if (m3 === "mma") { out += "మ్మ"; i += 3; continue; }
    if (m3 === "tta") { out += "ట్ట"; i += 3; continue; }
    if (m3 === "ppa") { out += "ప్ప"; i += 3; continue; }
    if (m3 === "lla") { out += "ల్ల"; i += 3; continue; }

    // 3. Lookahead 2 chars
    let m2 = text.substr(i, 2);
    if (VOWELS[m2] && (i === 0 || text[i - 1] === " ")) {
      out += VOWELS[m2];
      i += 2;
      continue;
    }

    // Consonant + Vowel combinations (e.g. ka -> క, kA -> కా, ku -> కు)
    let c1 = text[i];
    let v1 = text[i + 1];
    if (CONSONANTS[c1] && v1 && (MATRAS[v1] !== undefined)) {
      let base = CONSONANTS[c1].replace("్", "");
      let matra = MATRAS[v1];
      out += base + matra;
      i += 2;
      continue;
    }

    // Lookahead for 2-char consonants + vowel (e.g. tha, dhi, shu)
    let c2 = text.substr(i, 2);
    let vAfterC2 = text[i + 2];
    if (CONSONANTS[c2] && vAfterC2 && (MATRAS[vAfterC2] !== undefined)) {
      let base = CONSONANTS[c2].replace("్", "");
      let matra = MATRAS[vAfterC2];
      out += base + matra;
      i += 3;
      continue;
    }

    if (CONSONANTS[c2]) {
      out += CONSONANTS[c2];
      i += 2;
      continue;
    }

    // 4. Lookahead 1 char
    if (VOWELS[c1] && (i === 0 || text[i - 1] === " ")) {
      out += VOWELS[c1];
      i += 1;
      continue;
    }

    if (CONSONANTS[c1]) {
      out += CONSONANTS[c1];
      i += 1;
      continue;
    }

    if (SPECIALS[c1]) {
      out += SPECIALS[c1];
      i += 1;
      continue;
    }

    // Pass-through symbols, numbers, punctuation, spaces
    out += c1;
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

