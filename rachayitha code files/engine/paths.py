import os
import sys
import json

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundled .exe
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # relative to the project root of rachayitha code files
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_config_dir():
    """
    Get the writable configuration directory in %APPDATA%/Rachayitha
    """
    appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
    cfg_dir = os.path.join(appdata, 'Rachayitha')
    os.makedirs(cfg_dir, exist_ok=True)
    return cfg_dir

def get_config_path():
    return os.path.join(get_config_dir(), 'config.json')

DEFAULT_CONFIG = {
    "hotkeys": {
        "telugu_toggle": "alt+t",
        "english": "alt+e"
    },
    "current_language": "telugu",
    "casual_type": True,
    "auto_start": True,
    "show_notifications": True
}

def load_config():
    path = get_config_path()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    # If not found in APPDATA, copy from bundled default or use DEFAULT_CONFIG
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    path = get_config_path()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
