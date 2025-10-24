# Sprachausgabe 

## Bibliothek
Ein Kriterium für unsere Aplikation ist die Sprachausgabe, wir entschieden uns für die Bibliothek pyttsx3. Die Entscheidung viel auf diese Bibliothek da sie isoliert von Application Programming Interfaces funktioniert und dementsprechend auch Offline verfügbar ist. Zudem unerstützt pyttsx3 cross Platforming. 

## Funktionsweise 
Dokumentation: https://pyttsx3.readthedocs.io/en/latest/engine.html

Jede Sprachausgabe basiert auf einem angesteurten Sprachengine: Diese wiederum wird durch den User durch den pyttsx3.init() Befehl aufgerufen.


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
