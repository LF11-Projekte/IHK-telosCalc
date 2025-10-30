# Sprachausgabe 

## Bibliothek
Ein Kriterium für unsere Aplikation ist die Sprachausgabe, wir entschieden uns für die Bibliothek pyttsx3. Die Entscheidung viel auf diese Bibliothek da sie isoliert von Application Programming Interfaces funktioniert und dementsprechend auch Offline verfügbar ist. Zudem unerstützt pyttsx3 cross Platforming. 

## Funktionsweise 
Dokumentation: https://pyttsx3.readthedocs.io/en/latest/engine.html

Jede Sprachausgabe basiert auf einem angesteurten Sprachengine: Diese wiederum wird durch den User durch den pyttsx3.init() Befehl aufgerufen.

Sprachausgabe mit suchfunktion in den systemsprachen
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
```

Code Versuche (keine qualitative Dokumentation)
```
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
