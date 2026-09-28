import ctypes
import os
import keyboard

from engine.buffer import TypingBuffer
from engine.transliterator import transliterate

is_telugu_on = False
buffer = TypingBuffer()
user32 = ctypes.windll.user32 if os.name == 'nt' else None

def is_caps_active():
    if user32:
        return bool(user32.GetKeyState(0x14) & 1)
    return False

def toggle():
    global is_telugu_on
    is_telugu_on = not is_telugu_on
    buffer.commit()
    status = "Telugu ON" if is_telugu_on else "English ON"
    print(f"\n[Mode: {status}] - Press Alt+T to toggle")

def set_mode(tel):
    global is_telugu_on
    is_telugu_on = tel
    buffer.commit()
    print(f"\n[Mode: {'Telugu ON' if is_telugu_on else 'English ON'}]")

keyboard.add_hotkey('alt+t', toggle)
keyboard.add_hotkey('alt+e', lambda: set_mode(False))

def handle(e):
    if not is_telugu_on:
        return True

    if e.event_type != 'down':
        return True

    if keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt'):
        return True

    if e.name in ['space', 'enter']:
        buffer.commit()
        return True

    if e.name == 'backspace':
        if buffer.is_active():
            backspaces_needed, new_out = buffer.backspace()
            for _ in range(backspaces_needed):
                keyboard.send('backspace')
            if new_out:
                keyboard.write(new_out)
            return False
        return True

    if len(e.name) == 1:
        is_alpha = e.name.isalpha()
        is_special = e.name in ['~', '_']

        if is_alpha or is_special:
            shift_held = keyboard.is_pressed('shift')
            caps = is_caps_active()
            is_upper = shift_held ^ caps

            char = e.name.upper() if is_upper else e.name.lower()

            backspaces_needed, new_out = buffer.add(char)
            for _ in range(backspaces_needed):
                keyboard.send('backspace')
            keyboard.write(new_out)
            return False

    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  రచయిత (Rachayitha) - Console Prototype")
    print("  Press Alt+T to toggle Telugu ON/OFF")
    print("  Type 'telugu' -> తెలుగు, 'amma' -> అమ్మ, 'kRuShNa' -> కృష్ణ")
    print("=" * 60)

    keyboard.hook(handle, suppress=True)
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nExiting Rachayitha...")
