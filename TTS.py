import pyttsx3
import threading

class TTS:

    _engine = pyttsx3.init()
    _language_codes = {
        voice.languages[0].lower() : voice.id for voice in _engine.getProperty('voices') # type: ignore
    }
    _speech_thread = None
    
    @staticmethod
    def speak(text: str, language: str) -> None: #Literal["en", "de"] = "en") -> None:

        # Stop any previous speech before starting new one
        TTS.stop()

        language_code = TTS._language_codes.get(language, "en-gb")
        if not language_code: raise ValueError(f"Language '{language}' not supported.")

        # Run TTS in background thread to avoid blocking UI
        def speak_async():
            try:
                TTS._engine.setProperty('voice', language_code)
                TTS._engine.say(text)
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
        except Exception as e:
            pass  # Silent fail OK here
        