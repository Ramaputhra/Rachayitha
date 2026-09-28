use super::transliterator::Transliterator;

#[derive(Debug, Clone, Default)]
pub struct TypingBuffer {
    eng: String,
    last_telugu: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BufferDelta {
    pub backspaces: usize,
    pub replacement: String,
}

impl TypingBuffer {
    pub fn new() -> Self {
        Self {
            eng: String::new(),
            last_telugu: String::new(),
        }
    }

    /// Add an English character to the buffer, recalculate transliteration,
    /// and return the delta (backspaces to delete old output + new text to write)
    pub fn push(&mut self, ch: char) -> BufferDelta {
        let old_len = self.last_telugu.chars().count();
        self.eng.push(ch);
        let new_telugu = Transliterator::transliterate(&self.eng);
        self.last_telugu = new_telugu.clone();

        BufferDelta {
            backspaces: old_len,
            replacement: new_telugu,
        }
    }

    /// Handle Backspace: chop the last English character and recalculate
    pub fn pop(&mut self) -> Option<BufferDelta> {
        if self.eng.is_empty() {
            return None;
        }

        let old_len = self.last_telugu.chars().count();
        self.eng.pop();

        let new_telugu = if self.eng.is_empty() {
            String::new()
        } else {
            Transliterator::transliterate(&self.eng)
        };

        self.last_telugu = new_telugu.clone();

        Some(BufferDelta {
            backspaces: old_len,
            replacement: new_telugu,
        })
    }

    /// Commit the current word and reset the buffer state
    pub fn commit(&mut self) {
        self.eng.clear();
        self.last_telugu.clear();
    }

    /// Return true if the buffer currently contains typed characters
    pub fn is_active(&self) -> bool {
        !self.eng.is_empty()
    }

    pub fn current_english(&self) -> &str {
        &self.eng
    }

    pub fn current_telugu(&self) -> &str {
        &self.last_telugu
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_buffer_push_and_commit() {
        let mut buf = TypingBuffer::new();
        assert!(!buf.is_active());

        let delta1 = buf.push('t');
        assert_eq!(delta1.backspaces, 0);
        assert_eq!(delta1.replacement, "త");

        let delta2 = buf.push('e');
        assert_eq!(delta2.backspaces, 1);
        assert_eq!(delta2.replacement, "తె");

        buf.commit();
        assert!(!buf.is_active());
        assert_eq!(buf.current_english(), "");
    }

    #[test]
    fn test_buffer_pop() {
        let mut buf = TypingBuffer::new();
        buf.push('a');
        buf.push('m');
        buf.push('m');
        let delta = buf.pop().unwrap();
        assert_eq!(delta.replacement, "అమ");
    }
}
