import pyttsx3
import threading
import re


class TTS:

    _engine = pyttsx3.init()
    _language_codes = {
        voice.languages[0].lower(): voice.id for voice in _engine.getProperty('voices')  # type: ignore
    }
    _speech_thread = None

    @staticmethod
    def _normalize_text_for_tts(text: str, language: str) -> str:
        """Normalize text for better TTS pronunciation.

        For English and German, spell the abbreviation IT as "I T" so the
        TTS pronounces the letters instead of the word "it". We deliberately
        avoid expanding to the full phrase (e.g. "Information Technology").
        """
        if not text:
            return text

        lang = (language or "").lower()
        out = text

        # Handle English and German by default; add other languages as needed
        if lang.startswith('en'):
            # English: spell letters (I T) so the voice says the letters
            out = re.sub(r"\bIT\b|IT(?=-)", "I T", out, flags=re.IGNORECASE)
        elif lang.startswith('de'):
            # German UI but prefer English letter names: expand to explicit
            out = re.sub(r"\bIT\b|IT(?=-)", "ay-ti", out, flags=re.IGNORECASE)

        return out

    @staticmethod
    def speak(text: str, language: str) -> None:

        # Stop any previous speech before starting new one
        TTS.stop()
        #language = "fr-fr"
        language_code = TTS._language_codes.get(language, "en-gb")
        if not language_code:
            raise ValueError(f"Language '{language}' not supported.")

        # Normalize text so abbreviations are pronounced sensibly
        normalized = TTS._normalize_text_for_tts(text, language)

        # Print normalized text for debugging / verification
        #try:
        #    print(f"[TTS] speaking (lang={language}): {normalized}")
        #except Exception:
        #    pass

        # Run TTS in background thread to avoid blocking UI
        def speak_async():
            try:
                TTS._engine.setProperty('voice', language_code)
                TTS._engine.say(normalized)
                TTS._engine.startLoop()  # Blocks but in background thread
            except Exception as e:
                print(f"Error speaking: {e}")

        TTS._speech_thread = threading.Thread(target=speak_async, daemon=True)
        TTS._speech_thread.start()

    @staticmethod
    def stop() -> None:
        try:
            TTS._engine.endLoop()
            TTS._engine.stop()
        except Exception:
            # Silently ignore stop errors (common if no loop running)
            pass
