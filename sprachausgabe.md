# Sprachausgabe 

## Bibliothek
Ein Kriterium für unsere Aplikation ist die Sprachausgabe, wir entschieden uns für die Bibliothek pyttsx3. Die Entscheidung viel auf diese Bibliothek da sie isoliert von Application Programming Interfaces funktioniert und dementsprechend auch Offline verfügbar ist. Zudem unerstützt pyttsx3 cross Platforming. 

## Funktionsweise 
Dokumentation: https://pyttsx3.readthedocs.io/en/latest/engine.html

Jede Sprachausgabe basiert auf einem angesteurten Sprachengine: Diese wiederum wird durch den User durch den pyttsx3.init() Befehl aufgerufen.
