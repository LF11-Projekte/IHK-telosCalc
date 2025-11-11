import json
from typing import List, Literal, Optional, Dict

class Config:

    LANGUAGE: Literal["en", "de"] = "de"
    GUI_SRC: Dict[Literal["en", "de"], str] = { "de": "de_DE.ui", "en": "en_GB.ui" }
    STYLE: str = "dark_lightgreen"
    SPEECH_ON: bool = False


    @staticmethod
    def save(conf_file: str) -> None:
        with open(conf_file, "w") as file:
            json_txt = json.dumps({
                "lang": Config.LANGUAGE,
                "gui_src": Config.GUI_SRC,
                "style": Config.STYLE,
                "speech_on": Config.SPEECH_ON
            }, indent=4)

            file.write(json_txt)


    @staticmethod
    def load(conf_file: str) -> None:
        try:
            with open(conf_file, "r") as file:
                json_txt = file.read()
                data = json.loads(json_txt)

                Config.LANGUAGE = data["lang"]
                Config.GUI_SRC = data["gui_src"]
                Config.STYLE = data["style"]
                Config.SPEECH_ON = data["speech_on"]
        except:
            Config.LANGUAGE = "de"
            Config.GUI_SRC = { "de": "de_DE.ui", "en": "en_GB.ui" }
            Config.STYLE= "dark_lightgreen"
            Config.SPEECH_ON = False
