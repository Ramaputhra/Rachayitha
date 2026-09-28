use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;
use directories::ProjectDirs;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub enabled: bool,
    pub hotkey_toggle: String,
    pub auto_start: bool,
    pub show_notifications: bool,
    pub current_language: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            enabled: false,
            hotkey_toggle: "alt+t".to_string(),
            auto_start: true,
            show_notifications: true,
            current_language: "telugu".to_string(),
        }
    }
}

impl AppConfig {
    /// Return the OS-standard configuration file path for Rachayitha
    pub fn config_path() -> PathBuf {
        if let Some(proj_dirs) = ProjectDirs::from("com", "ramaputhra", "Rachayitha") {
            let dir = proj_dirs.config_dir();
            dir.join("config.json")
        } else {
            PathBuf::from("config.json")
        }
    }

    /// Load config from file or return defaults if not found
    pub fn load() -> Self {
        let path = Self::config_path();
        if path.exists() {
            if let Ok(content) = fs::read_to_string(&path) {
                if let Ok(cfg) = serde_json::from_str::<AppConfig>(&content) {
                    return cfg;
                }
            }
        }
        let default_cfg = Self::default();
        let _ = default_cfg.save();
        default_cfg
    }

    /// Save current config to the OS-standard directory
    pub fn save(&self) -> Result<(), String> {
        let path = Self::config_path();
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|e| e.to_string())?;
        }
        let json = serde_json::to_string_pretty(self).map_err(|e| e.to_string())?;
        fs::write(&path, json).map_err(|e| e.to_string())?;
        Ok(())
    }
}
