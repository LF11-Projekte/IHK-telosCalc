import pyttsx3

class TTS:

    _engine = pyttsx3.init()
    _language_codes = {
        voice.languages[0].lower() : voice.id for voice in _engine.getProperty('voices') # type: ignore
    }
    
    @staticmethod
    def speak(text: str, language: str) -> None: #Literal["en", "de"] = "en") -> None:

        print(TTS._language_codes)

        language_code = TTS._language_codes.get(language, "en-gb")
        if not language_code: raise ValueError(f"Language '{language}' not supported.")

        TTS.stop()

        TTS._engine.setProperty('voice', language_code)
        TTS._engine.say(text)
        TTS._engine.startLoop()

        TTS.stop()

    @staticmethod
    def stop() -> None:
        try:
            TTS._engine.endLoop()
            TTS._engine.stop()
        except Exception as e:
            print(f"Error stopping TTS engine: {e}")
        