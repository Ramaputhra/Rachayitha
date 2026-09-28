from .transliterator import transliterate

class TypingBuffer:
    def __init__(self):
        self.eng = ""
        self.last_telugu = ""
        self.last_out_len = 0

    def add(self, char):
        old_len = self.last_out_len
        self.eng += char
        new_telugu = transliterate(self.eng)
        self.last_telugu = new_telugu
        self.last_out_len = len(new_telugu)
        return old_len, new_telugu

    def backspace(self):
        if not self.eng:
            return 0, ""
        old_len = self.last_out_len
        self.eng = self.eng[:-1]
        new_telugu = transliterate(self.eng) if self.eng else ""
        self.last_telugu = new_telugu
        self.last_out_len = len(new_telugu)
        return old_len, new_telugu

    def commit(self):
        self.eng = ""
        self.last_telugu = ""
        self.last_out_len = 0

    def is_active(self):
        return bool(self.eng)

    def get_eng(self):
        return self.eng

    def get_telugu(self):
        return self.last_telugu
