// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod config;
mod engine;
mod hook;

use config::AppConfig;
use engine::rules::{RuleEntry, Rules};
use engine::transliterator::Transliterator;
use hook::HookManager;

use std::sync::Mutex;
use tauri::menu::{Menu, MenuItem};
use tauri::tray::{TrayIconBuilder, TrayIconEvent};
use tauri::{AppHandle, Manager, State};

struct AppState {
    config: Mutex<AppConfig>,
}

#[tauri::command]
fn transliterate_text(input: String) -> String {
    Transliterator::transliterate(&input)
}

#[tauri::command]
fn get_rules() -> Vec<RuleEntry> {
    Rules::get_all_entries()
}

#[tauri::command]
fn get_status() -> bool {
    HookManager::is_enabled()
}

#[tauri::command]
fn toggle_telugu() -> bool {
    HookManager::toggle_mode()
}

#[tauri::command]
fn set_telugu(enabled: bool) {
    HookManager::set_mode(enabled);
}

#[tauri::command]
fn get_config(state: State<'_, AppState>) -> AppConfig {
    state.config.lock().unwrap().clone()
}

#[tauri::command]
fn save_config(new_config: AppConfig, state: State<'_, AppState>) -> Result<(), String> {
    let mut cfg = state.config.lock().unwrap();
    *cfg = new_config.clone();
    cfg.save()
}

fn main() {
    let initial_config = AppConfig::load();
    let app_state = AppState {
        config: Mutex::new(initial_config),
    };

    tauri::Builder::default()
        .manage(app_state)
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_notification::init())
        .setup(|app| {
            let handle = app.handle().clone();

            // 1. Build Native System Tray Menu
            let toggle_telugu_item = MenuItem::with_id(app, "toggle", "Toggle Telugu (Alt+T)", true, None::<&str>)?;
            let sep1 = tauri::menu::PredefinedMenuItem::separator(app)?;
            let settings_item = MenuItem::with_id(app, "settings", "Settings & Playground...", true, None::<&str>)?;
            let sep2 = tauri::menu::PredefinedMenuItem::separator(app)?;
            let quit_item = MenuItem::with_id(app, "quit", "Quit Rachayitha", true, None::<&str>)?;

            let menu = Menu::with_items(
                app,
                &[
                    &toggle_telugu_item,
                    &sep1,
                    &settings_item,
                    &sep2,
                    &quit_item,
                ],
            )?;

            // 2. Setup System Tray Icon
            let tray_handle = handle.clone();
            let _tray = TrayIconBuilder::new()
                .menu(&menu)
                .tooltip("Rachayitha: Telugu Transliteration (Alt+T)")
                .on_menu_event(move |app, event| match event.id.as_ref() {
                    "toggle" => {
                        let new_state = HookManager::toggle_mode();
                        let _ = app.emit("status-changed", new_state);
                    }
                    "settings" => {
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                    "quit" => {
                        app.exit(0);
                    }
                    _ => {}
                })
                .on_tray_icon_event(move |tray, event| {
                    if let TrayIconEvent::Click { button: tauri::tray::MouseButton::Left, .. } = event {
                        let app = tray.app_handle();
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                })
                .build(app)?;

            // 3. Start Global Keyboard Hook
            let hook_app_handle = handle.clone();
            HookManager::start(move |is_telugu| {
                let _ = hook_app_handle.emit("status-changed", is_telugu);
            });

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            transliterate_text,
            get_rules,
            get_status,
            toggle_telugu,
            set_telugu,
            get_config,
            save_config
        ])
        .run(tauri::generate_context!())
        .expect("error while running Rachayitha");
}
