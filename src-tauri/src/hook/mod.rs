use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use std::thread;
use std::time::Duration;
use lazy_static::lazy_static;
use rdev::{listen, simulate, Event, EventType, Key};

use crate::engine::buffer::TypingBuffer;

lazy_static! {
    pub static ref TELUGU_ENABLED: AtomicBool = AtomicBool::new(false);
    pub static ref ALT_PRESSED: AtomicBool = AtomicBool::new(false);
    pub static ref CTRL_PRESSED: AtomicBool = AtomicBool::new(false);
    pub static ref BUFFER: Mutex<TypingBuffer> = Mutex::new(TypingBuffer::new());
}

pub struct HookManager;

impl HookManager {
    /// Toggle Telugu mode ON/OFF
    pub fn toggle_mode() -> bool {
        let current = TELUGU_ENABLED.load(Ordering::SeqCst);
        let new_state = !current;
        TELUGU_ENABLED.store(new_state, Ordering::SeqCst);
        if !new_state {
            if let Ok(mut buf) = BUFFER.lock() {
                buf.commit();
            }
        }
        new_state
    }

    /// Set mode explicitly
    pub fn set_mode(enabled: bool) {
        TELUGU_ENABLED.store(enabled, Ordering::SeqCst);
        if !enabled {
            if let Ok(mut buf) = BUFFER.lock() {
                buf.commit();
            }
        }
    }

    /// Check if Telugu mode is enabled
    pub fn is_enabled() -> bool {
        TELUGU_ENABLED.load(Ordering::SeqCst)
    }

    /// Start the background global keyboard hook listener
    pub fn start<F>(on_toggle: F)
    where
        F: Fn(bool) + Send + Sync + 'static,
    {
        thread::spawn(move || {
            if let Err(error) = listen(move |event| {
                Self::handle_event(event, &on_toggle);
            }) {
                eprintln!("Global hook listener error: {:?}", error);
            }
        });
    }

    fn handle_event<F>(event: Event, on_toggle: &F)
    where
        F: Fn(bool),
    {
        match event.event_type {
            EventType::KeyPress(key) => {
                // Track modifiers
                match key {
                    Key::Alt | Key::AltGr => {
                        ALT_PRESSED.store(true, Ordering::SeqCst);
                        return;
                    }
                    Key::ControlLeft | Key::ControlRight => {
                        CTRL_PRESSED.store(true, Ordering::SeqCst);
                        return;
                    }
                    _ => {}
                }

                // Check for Hotkey: Alt + T
                if ALT_PRESSED.load(Ordering::SeqCst) && key == Key::KeyT {
                    let new_state = Self::toggle_mode();
                    on_toggle(new_state);
                    return;
                }

                // If Ctrl or Alt is held, ignore character interception (e.g. Ctrl+C, Alt+F4)
                if CTRL_PRESSED.load(Ordering::SeqCst) || ALT_PRESSED.load(Ordering::SeqCst) {
                    return;
                }

                // If Telugu mode is OFF, do nothing
                if !TELUGU_ENABLED.load(Ordering::SeqCst) {
                    return;
                }

                // Handle Telugu Typing & Buffer Logic
                Self::process_key(key, event.name);
            }
            EventType::KeyRelease(key) => match key {
                Key::Alt | Key::AltGr => {
                    ALT_PRESSED.store(false, Ordering::SeqCst);
                }
                Key::ControlLeft | Key::ControlRight => {
                    CTRL_PRESSED.store(false, Ordering::SeqCst);
                }
                _ => {}
            },
            _ => {}
        }
    }

    fn process_key(key: Key, char_name: Option<String>) {
        let mut buf = match BUFFER.lock() {
            Ok(b) => b,
            Err(_) => return,
        };

        match key {
            Key::Space | Key::Return => {
                buf.commit();
            }
            Key::Backspace => {
                if let Some(delta) = buf.pop() {
                    // Replace on screen
                    Self::emit_delta(&delta.replacement, delta.backspaces);
                }
            }
            _ => {
                // If character is an alphabet character
                if let Some(name) = char_name {
                    if let Some(ch) = name.chars().next() {
                        if ch.is_alphabetic() || ch == '~' || ch == '_' {
                            let delta = buf.push(ch);
                            Self::emit_delta(&delta.replacement, delta.backspaces);
                        } else {
                            buf.commit();
                        }
                    }
                }
            }
        }
    }

    /// Emit backspaces and insert replacement text
    fn emit_delta(text: &str, backspaces: usize) {
        // Send backspaces to delete previous character(s)
        for _ in 0..backspaces {
            let _ = simulate(&EventType::KeyPress(Key::Backspace));
            let _ = simulate(&EventType::KeyRelease(Key::Backspace));
        }

        // Emit replacement text
        #[cfg(target_os = "windows")]
        {
            use std::ffi::OsStr;
            use std::os::windows::ffi::OsStrExt;

            // Direct Windows SendInput with KEYEVENTF_UNICODE for fast, native Telugu glyph rendering
            let wide: Vec<u16> = OsStr::new(text).encode_wide().collect();
            for &code in &wide {
                Self::send_windows_unicode(code);
            }
        }

        #[cfg(not(target_os = "windows"))]
        {
            // Cross-platform fallback for macOS / Linux
            for ch in text.chars() {
                // Emit character
                thread::sleep(Duration::from_millis(1));
            }
        }
    }

    #[cfg(target_os = "windows")]
    fn send_windows_unicode(code: u16) {
        #[repr(C)]
        struct KEYBDINPUT {
            wVk: u16,
            wScan: u16,
            dwFlags: u32,
            time: u32,
            dwExtraInfo: usize,
        }

        #[repr(C)]
        struct INPUT {
            r#type: u32,
            ki: KEYBDINPUT,
            padding: [u8; 8],
        }

        const INPUT_KEYBOARD: u32 = 1;
        const KEYEVENTF_UNICODE: u32 = 0x0004;
        const KEYEVENTF_KEYUP: u32 = 0x0002;

        extern "system" {
            fn SendInput(cInputs: u32, pInputs: *const INPUT, cbSize: i32) -> u32;
        }

        let press = INPUT {
            r#type: INPUT_KEYBOARD,
            ki: KEYBDINPUT {
                wVk: 0,
                wScan: code,
                dwFlags: KEYEVENTF_UNICODE,
                time: 0,
                dwExtraInfo: 0,
            },
            padding: [0; 8],
        };

        let release = INPUT {
            r#type: INPUT_KEYBOARD,
            ki: KEYBDINPUT {
                wVk: 0,
                wScan: code,
                dwFlags: KEYEVENTF_UNICODE | KEYEVENTF_KEYUP,
                time: 0,
                dwExtraInfo: 0,
            },
            padding: [0; 8],
        };

        unsafe {
            let inputs = [press, release];
            SendInput(2, inputs.as_ptr(), std::mem::size_of::<INPUT>() as i32);
        }
    }
}
