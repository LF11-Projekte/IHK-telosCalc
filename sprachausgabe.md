# Sprachausgabe 

## Auswahl der Python-Bibliothek der Sprachausgabe
Die Sprachausgabe ist eine Kundenanforderung. Wir entschideden uns für die Bibliothek pyttsx3, da sie, im gegensatz zu den meisten anderen Alternativen, auch isoliert von Application Programming Interfaces funktioniert. Dementsprechend ist sie auch Offline verfügbar. Zudem unerstützt pyttsx3 cross Platforming. 

## Nutzer Bedienung
Der Nutzer muss die Sprachausgabe lediglich in der Menübar der Applikation aktivieren um sprachunterstützung zu zu erhalten.

*scrrenshot*

## Sprachen
Die Verfügbaren Sprachen sind entsprechend des Kundenwunsches Deutsch sowie Englisch. Die Sprachausgabe ist an die Ausgabe Sprache des User Interface gekoppelt. 

## Funktionsweise 
Dokumentation: https://pyttsx3.readthedocs.io/en/latest/engine.html

Jede Sprachausgabe basiert auf einem angesteurten Sprachengine: Diese wiederum wird durch den User durch den pyttsx3.init() Befehl aufgerufen.

Sprachausgabe mit suchfunktion in den systemsprachen
```
import pyttsx3

class TTS:

    lang_id_table = None
    engine = None


    @staticmethod
    def get_language_id(language):
        """
        function searches for the possible languages, if param language exists it set the engine language to the wished
        :param language: wanted language
        :return: path (voice id)
        """
        for voice in TTS.engine.getProperty('voices'):
            if language.lower() in voice.name.lower():
                return voice.id
        raise RuntimeError("Language not installed")


    @staticmethod
    def tts_stop():
        if TTS.engine.isBusy():
            TTS.engine.stop()

    @staticmethod
    def tts_output(text, language=None):
        """
        speaks the wanted text
        :param language: defines the wanted language
        :param text: speaks the wished text
        :return: voice
        """

        if language is not None:
            TTS.tts_set_language(language)
        TTS.engine.say(text)
        TTS.engine.startLoop()
        TTS.engine.endLoop()

    @staticmethod
    def tts_set_language(language):
       TTS.engine.setProperty("voice", TTS.lang_id_table[language])

    @staticmethod
    def tts_setup():

        TTS.engine = pyttsx3.init()
        TTS.lang_id_table = {
            "de": TTS.get_language_id("german"),
            "en": TTS.get_language_id("english")
        }

TTS.tts_setup()
TTS.tts_output("Tamam", 'en')
TTS.tts_output("Tamam", 'de')
```

Code Versuche (keine qualitative Dokumentation)
```
import pyttsx3

engine = pyttsx3.init()

def getLanguageId(language):
    """
    function searches for the possible languages, if param language exists it set the engine language to the wished
    :param language: wanted language
    :return: path (voice id)
    """
    for voice in engine.getProperty('voices'):
        if language in voice.name.lower():
            return voice.id
    raise RuntimeError("Language not installed")




def speaker(language, text):
    """
    speaks the wanted text
    :param language: defines the wanted language
    :param text: speaks the wished text
    :return: voice
    """
    engine.setProperty('voice', language)
    engine.say(text)
    engine.runAndWait()

speaker("german", "zu sprechender Text")

---------

import pyttsx3

"""
Funktion -> Text annehmen und Sprache (Maybe Voice/Volume)
"""

engine = pyttsx3.init()
textToBeSpoken = "Aubrey Drake Graham (born October 24, 1986), professionally known by his middle name Drake, is a Canadian rapper, singer, songwriter, record producer, actor, and entrepreneur."

for voice in engine.getProperty('voices'):
    print(voice.name)

def speaker():
    engine.say(textToBeSpoken)
    engine.runAndWait()


def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))




change_voice(engine,"en", 'VoiceGenderMale')
speaker()

print(engine.getProperty('voices'))
```
