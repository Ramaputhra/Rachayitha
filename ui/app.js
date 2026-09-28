// Rachayitha UI & IPC Logic

// Check if Tauri is present
const hasTauri = window.__TAURI__ !== undefined;
const invoke = hasTauri ? window.__TAURI__.core.invoke : async (cmd, args) => mockInvoke(cmd, args);
const listen = hasTauri ? window.__TAURI__.event.listen : null;

// Embedded Rules fallback for browser preview
const FALLBACK_RULES = [
  // Vowels
  { key: "a", telugu: "అ", category: "Vowels (అచ్చులు)", example: "a -> అ" },
  { key: "aa / A", telugu: "ఆ", category: "Vowels (అచ్చులు)", example: "aa -> ఆ" },
  { key: "i", telugu: "ఇ", category: "Vowels (అచ్చులు)", example: "i -> ఇ" },
  { key: "ii / I", telugu: "ఈ", category: "Vowels (అచ్చులు)", example: "ii -> ఈ" },
  { key: "u", telugu: "ఉ", category: "Vowels (అచ్చులు)", example: "u -> ఉ" },
  { key: "uu / U", telugu: "ఊ", category: "Vowels (అచ్చులు)", example: "uu -> ఊ" },
  { key: "Ru / R^i", telugu: "ఋ", category: "Vowels (అచ్చులు)", example: "Ru -> ఋ" },
  { key: "e", telugu: "ఎ", category: "Vowels (అచ్చులు)", example: "e -> ఎ" },
  { key: "ee / E", telugu: "ఏ", category: "Vowels (అచ్చులు)", example: "ee -> ఏ" },
  { key: "ai / ay", telugu: "ఐ", category: "Vowels (అచ్చులు)", example: "ai -> ఐ" },
  { key: "o", telugu: "ఒ", category: "Vowels (అచ్చులు)", example: "o -> ఒ" },
  { key: "oo / O", telugu: "ఓ", category: "Vowels (అచ్చులు)", example: "oo -> ఓ" },
  { key: "au / ou", telugu: "ఔ", category: "Vowels (అచ్చులు)", example: "au -> ఔ" },
  // Consonants
  { key: "k", telugu: "క", category: "Consonants (హల్లులు)", example: "ka -> క" },
  { key: "kh / K", telugu: "ఖ", category: "Consonants (హల్లులు)", example: "kha -> ఖ" },
  { key: "g", telugu: "గ", category: "Consonants (హల్లులు)", example: "ga -> గ" },
  { key: "gh / G", telugu: "ఘ", category: "Consonants (హల్లులు)", example: "gha -> ఘ" },
  { key: "c / ch", telugu: "చ", category: "Consonants (హల్లులు)", example: "cha -> చ" },
  { key: "C / Ch", telugu: "ఛ", category: "Consonants (హల్లులు)", example: "Cha -> ఛ" },
  { key: "j", telugu: "జ", category: "Consonants (హల్లులు)", example: "ja -> జ" },
  { key: "jh / J", telugu: "ఝ", category: "Consonants (హల్లులు)", example: "jha -> ఝ" },
  { key: "T", telugu: "ట", category: "Consonants (హల్లులు)", example: "Ta -> ట" },
  { key: "Th", telugu: "ఠ", category: "Consonants (హల్లులు)", example: "Tha -> ఠ" },
  { key: "D", telugu: "డ", category: "Consonants (హల్లులు)", example: "Da -> డ" },
  { key: "Dh", telugu: "ఢ", category: "Consonants (హల్లులు)", example: "Dha -> ఢ" },
  { key: "N", telugu: "ణ", category: "Consonants (హల్లులు)", example: "Na -> ణ" },
  { key: "t", telugu: "త", category: "Consonants (హల్లులు)", example: "ta -> త" },
  { key: "th", telugu: "థ", category: "Consonants (హల్లులు)", example: "tha -> థ" },
  { key: "d", telugu: "ద", category: "Consonants (హల్లులు)", example: "da -> ద" },
  { key: "dh", telugu: "ధ", category: "Consonants (హల్లులు)", example: "dha -> ధ" },
  { key: "n", telugu: "న", category: "Consonants (హల్లులు)", example: "na -> న" },
  { key: "p", telugu: "ప", category: "Consonants (హల్లులు)", example: "pa -> ప" },
  { key: "ph / f", telugu: "ఫ", category: "Consonants (హల్లులు)", example: "pha -> ఫ" },
  { key: "b", telugu: "బ", category: "Consonants (హల్లులు)", example: "ba -> బ" },
  { key: "bh / B", telugu: "భ", category: "Consonants (హల్లులు)", example: "bha -> భ" },
  { key: "m", telugu: "మ", category: "Consonants (హల్లులు)", example: "ma -> మ" },
  { key: "y", telugu: "య", category: "Consonants (హల్లులు)", example: "ya -> య" },
  { key: "r", telugu: "ర", category: "Consonants (హల్లులు)", example: "ra -> ర" },
  { key: "l", telugu: "ల", category: "Consonants (హల్లులు)", example: "la -> ల" },
  { key: "v / w", telugu: "వ", category: "Consonants (హల్లులు)", example: "va -> వ" },
  { key: "sh / S", telugu: "శ", category: "Consonants (హల్లులు)", example: "sha -> శ" },
  { key: "Sh", telugu: "ష", category: "Consonants (హల్లులు)", example: "Sha -> ష" },
  { key: "s", telugu: "స", category: "Consonants (హల్లులు)", example: "sa -> స" },
  { key: "h", telugu: "హ", category: "Consonants (హల్లులు)", example: "ha -> హ" },
  { key: "L", telugu: "ళ", category: "Consonants (హల్లులు)", example: "La -> ళ" },
  { key: "R", telugu: "ఱ", category: "Consonants (హల్లులు)", example: "Ra -> ఱ (బండిర)" },
  { key: "ksh", telugu: "క్ష", category: "Consonants (హల్లులు)", example: "ksha -> క్ష" },
  { key: "jnya", telugu: "జ్ఞ", category: "Consonants (హల్లులు)", example: "jnya -> జ్ఞ" },
  // Guninthalu
  { key: "aa / A", telugu: "ా", category: "Guninthalu (గుణింతాలు)", example: "kaa -> కా" },
  { key: "i", telugu: "ి", category: "Guninthalu (గుణింతాలు)", example: "ki -> కి" },
  { key: "ii / I", telugu: "ీ", category: "Guninthalu (గుణింతాలు)", example: "kii -> కీ" },
  { key: "u", telugu: "ు", category: "Guninthalu (గుణింతాలు)", example: "ku -> కు" },
  { key: "uu / U", telugu: "ూ", category: "Guninthalu (గుణింతాలు)", example: "kuu -> కూ" },
  { key: "Ru", telugu: "ృ", category: "Guninthalu (గుణింతాలు)", example: "kRu -> కృ" },
  { key: "e", telugu: "ె", category: "Guninthalu (గుణింతాలు)", example: "ke -> కె" },
  { key: "ee / E", telugu: "ే", category: "Guninthalu (గుణింతాలు)", example: "kee -> కే" },
  { key: "ai / ay", telugu: "ై", category: "Guninthalu (గుణింతాలు)", example: "kai -> కై" },
  { key: "o", telugu: "ొ", category: "Guninthalu (గుణింతాలు)", example: "ko -> కొ" },
  { key: "oo / O", telugu: "ో", category: "Guninthalu (గుణింతాలు)", example: "koo -> కో" },
  { key: "au / ou", telugu: "ౌ", category: "Guninthalu (గుణింతాలు)", example: "kau -> కౌ" },
  // Special
  { key: "M", telugu: "ం", category: "Special (ప్రత్యేక గుర్తులు)", example: "kaM -> కం (సున్నా)" },
  { key: "H", telugu: "ః", category: "Special (ప్రత్యేక గుర్తులు)", example: "kaH -> కః (విసర్గ)" },
  { key: "~", telugu: "్", category: "Special (ప్రత్యేక గుర్తులు)", example: "k~ -> క్ (పొల్లు)" },
  { key: "_", telugu: "ZWNJ", category: "Special (ప్రత్యేక గుర్తులు)", example: "k_k -> క్‌క (విభాజకం)" },
];

let allRules = [];
let currentCategory = 'all';

// Mock transliterator for client-side preview when not inside Tauri
function clientTransliterate(text) {
  // Simple demonstration transliterator for UI playground
  let out = text;
  const map = {
    'telugu': 'తెలుగు',
    'amma': 'అమ్మ',
    'namaskAram': 'నమస్కారం',
    'rachayitha': 'రచయిత',
    'kRuShNa': 'కృష్ణ',
    'bhAratadEsham': 'భారతదేశం',
  };
  for (const [k, v] of Object.entries(map)) {
    out = out.split(k).join(v);
  }
  return out;
}

async function mockInvoke(cmd, args) {
  if (cmd === 'get_rules') return FALLBACK_RULES;
  if (cmd === 'transliterate_text') return clientTransliterate(args.input);
  if (cmd === 'get_status') return true;
  if (cmd === 'toggle_telugu') return false;
  if (cmd === 'get_config') return { enabled: true, hotkey_toggle: "alt+t", auto_start: true, show_notifications: true };
  if (cmd === 'save_config') return true;
  return null;
}

// DOM Elements
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  setupPlayground();
  await setupKeyMap();
  await setupStatus();
  await setupPreferences();
});

// 1. Navigation Tabs
function setupTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const panes = document.querySelectorAll('.tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = `tab-${tab.dataset.tab}`;
      tabs.forEach(t => t.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// 2. Interactive Playground
function setupPlayground() {
  const input = document.getElementById('playground-input');
  const output = document.getElementById('playground-output');
  const clearBtn = document.getElementById('clear-btn');
  const copyBtn = document.getElementById('copy-btn');
  const chips = document.querySelectorAll('.chip');

  const updateTransliteration = async () => {
    const text = input.value;
    if (!text.trim()) {
      output.innerHTML = '<span class="placeholder">మీ తెలుగు అక్షరాలు ఇక్కడ కనిపిస్తాయి...</span>';
      return;
    }
    const telugu = await invoke('transliterate_text', { input: text });
    output.textContent = telugu;
  };

  input.addEventListener('input', updateTransliteration);

  clearBtn.addEventListener('click', () => {
    input.value = '';
    output.innerHTML = '<span class="placeholder">మీ తెలుగు అక్షరాలు ఇక్కడ కనిపిస్తాయి...</span>';
    input.focus();
  });

  copyBtn.addEventListener('click', () => {
    const text = output.textContent;
    if (text && !output.querySelector('.placeholder')) {
      navigator.clipboard.writeText(text);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => copyBtn.textContent = 'Copy Text', 1500);
    }
  });

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      input.value = chip.dataset.text;
      updateTransliteration();
      input.focus();
    });
  });
}

// 3. Key Map Search & Categories
async function setupKeyMap() {
  try {
    allRules = await invoke('get_rules');
  } catch (e) {
    allRules = FALLBACK_RULES;
  }

  const searchInput = document.getElementById('keymap-search');
  const filterBtns = document.querySelectorAll('.filter-btn');

  renderKeyMap();

  searchInput.addEventListener('input', () => {
    renderKeyMap();
  });

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      renderKeyMap();
    });
  });
}

function renderKeyMap() {
  const grid = document.getElementById('keymap-grid');
  const searchTerm = document.getElementById('keymap-search').value.toLowerCase().trim();

  const filtered = allRules.filter(rule => {
    // Category match
    const categoryMatches = (currentCategory === 'all') || rule.category.toLowerCase().includes(currentCategory.toLowerCase());
    if (!categoryMatches) return false;

    // Search match
    if (!searchTerm) return true;
    return rule.key.toLowerCase().includes(searchTerm) ||
           rule.telugu.includes(searchTerm) ||
           rule.example.toLowerCase().includes(searchTerm) ||
           rule.category.toLowerCase().includes(searchTerm);
  });

  grid.innerHTML = filtered.map(rule => `
    <div class="key-card">
      <div class="key-telugu">${rule.telugu}</div>
      <div class="key-badge">${rule.key}</div>
      <div class="key-example">${rule.example}</div>
    </div>
  `).join('');
}

// 4. Status Indicator & Toggle
async function setupStatus() {
  const indicator = document.getElementById('status-indicator');
  const label = document.getElementById('status-label');
  const toggleBtn = document.getElementById('toggle-status-btn');

  const updateUI = (isEnabled) => {
    if (isEnabled) {
      indicator.classList.remove('off');
      label.textContent = 'Telugu ON';
    } else {
      indicator.classList.add('off');
      label.textContent = 'English ON';
    }
  };

  const initialStatus = await invoke('get_status');
  updateUI(initialStatus);

  toggleBtn.addEventListener('click', async () => {
    const newState = await invoke('toggle_telugu');
    updateUI(newState);
  });

  if (listen) {
    listen('status-changed', (event) => {
      updateUI(event.payload);
    });
  }
}

// 5. Preferences
async function setupPreferences() {
  const hotkeyInput = document.getElementById('hotkey-input');
  const autostartToggle = document.getElementById('autostart-toggle');
  const notificationsToggle = document.getElementById('notifications-toggle');
  const saveBtn = document.getElementById('save-settings-btn');
  const saveMsg = document.getElementById('save-msg');

  try {
    const cfg = await invoke('get_config');
    if (cfg) {
      hotkeyInput.value = cfg.hotkey_toggle || 'alt+t';
      autostartToggle.checked = cfg.auto_start !== false;
      notificationsToggle.checked = cfg.show_notifications !== false;
    }
  } catch (e) {
    console.error(e);
  }

  saveBtn.addEventListener('click', async () => {
    const newConfig = {
      enabled: true,
      hotkey_toggle: hotkeyInput.value.trim().toLowerCase(),
      auto_start: autostartToggle.checked,
      show_notifications: notificationsToggle.checked,
      current_language: "telugu"
    };

    await invoke('save_config', { newConfig });
    saveMsg.style.display = 'inline';
    setTimeout(() => saveMsg.style.display = 'none', 2500);
  });
}
