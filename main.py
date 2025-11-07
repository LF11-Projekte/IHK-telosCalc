import time
import os, sys, math, pathlib, ctypes
from typing import Literal


#from PyQt6.QtCore import pyqtSlot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QCoreApplication, Signal, Slot, Qt, QFile, QObject
from PySide6.QtWidgets import QApplication, QFileDialog, QSpinBox, QLabel, QWidget, QMainWindow
#from PyQt6.uic import loadUi
from qt_material import apply_stylesheet

import DataManager, TTS

GUI_FILENAMES = {"de": "de_DE.ui", "en": "en_EN.ui"}
LANGUAGE: Literal["de", "en"] = "de"
GUI_FILENAME = GUI_FILENAMES[LANGUAGE]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app = None


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        #super(self.__class__, self).__init__(parent)
        super(MainWindow, self).__init__()
        self.loader = QUiLoader()
        print(os.path.join(SCRIPT_DIR, GUI_FILENAME))
        #loadUi(os.path.join(SCRIPT_DIR, GUI_FILENAME), self)
        self.ui = self.loader.load(os.path.join(SCRIPT_DIR, GUI_FILENAME), None)
        self.ui.show()
        self.connect_slots()
        self.dataManager = DataManager.DataManager(0,0,0,0,0,0,0, None)
        self.dataManager.calculate_all_grades()
        self.set_ui_values_by_data_manager()


    def load_ui_values_to_data_manager(self):
        self.dataManager.set_all_values(
            fe1_ItWorkstation=self.ui.numFe1.value(),
            fe2_PlanningASoftwareProduct=self.ui.numFe2_1.value(),
            fe2_DevelopmentAndImplementationOfAlgorithms=self.ui.numFe2_2.value(),
            fe2_EconomicsAndSocialStudies=self.ui.numFe2_3.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Oral=self.ui.numFe2_8.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Written=self.ui.numFe2_7.value(),
            fe2_OralSupplementaryExamination=None,
            fe2_OralSupplementaryExaminationSubject=None
        )


    def set_ui_values_by_data_manager(self):
        self.ui.numFe1.setValue(self.dataManager.fe1_ItWorkstation)
        self.ui.numFe2_1.setValue(self.dataManager.fe2_PlanningASoftwareProduct)
        self.ui.numFe2_2.setValue(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms)
        self.ui.numFe2_3.setValue(self.dataManager.fe2_EconomicsAndSocialStudies)
        self.ui.numFe2_7.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Written)
        self.ui.numFe2_8.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Oral)
        self.ui.numFe2_out.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Score)

        if self.dataManager.fe1_ItWorkstation_Grade:
            self.ui.lblFe1Output.setText(str(self.dataManager.fe1_ItWorkstation_Grade))
        if self.dataManager.fe2_PlanningASoftwareProduct_Grade:
            self.ui.lblFe2Output1.setText(str(self.dataManager.fe2_PlanningASoftwareProduct_Grade))
        if self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade:
            self.ui.lblFe2Output2.setText(str(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade))
        if self.dataManager.fe2_EconomicsAndSocialStudies_Grade:
            self.ui.lblFe2Output3.setText(str(self.dataManager.fe2_EconomicsAndSocialStudies_Grade))
        if self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade:
            self.ui.lblFe2Output1_3.setText(str(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade))

        self.set_success()


    def set_success(self):
        self.ui.lblSuccess.setText("Die Prüfung wurde bestanden." if self.dataManager.has_passed() else "Die Prüfung wurde nicht bestanden.")

    @Slot()
    def on_numValue_changed(self):
        self.load_ui_values_to_data_manager()
        self.set_ui_values_by_data_manager()

    @Slot()
    def set_dark_mode(self):
        apply_stylesheet(app, "dark_teal.xml")

    @Slot()
    def set_bright_mode(self):
        apply_stylesheet(app, "light_blue.xml")

    @Slot()
    def load_from_file_action(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 
                                                  caption="Eingabeparameter aus Datei laden",
                                                  filter="Alle Typen (*);;JSON (*.json)")
        if fileName:
            self._disconnect_number_slots()
            self.dataManager.loadFromFile(fileName)
            self.dataManager.calculate_all_grades()
            self.set_ui_values_by_data_manager()
            self._connect_number_slots()

    @Slot()
    def save_to_file_action(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  caption="Eingabeparameter in Datei speichern",
                                                  filter="Alle Typen (*);;JSON (*.json)")
        if fileName:
            self.dataManager.saveToFile(fileName)

    def say(self):
        TTS.TTS.speak("Hello, this is a test.", language="fr-fr")
        TTS.TTS.speak("Hallo, dies ist ein Test.", language="de-de")

    def change_ui_file(self, language: Literal["de", "en"]):
        self.disconnect_slots()
        LANGUAGE = language
        #self.ui.close()
        self.ui = self.loader.load(os.path.join(SCRIPT_DIR, GUI_FILENAMES[LANGUAGE]), None)
        self.ui.show()
        self.connect_slots()
        self.set_ui_values_by_data_manager()

    def connect_slots(self):
        self._connect_number_slots()
        self.ui.actionBright.triggered.connect(self.set_bright_mode)
        self.ui.actionDark.triggered.connect(self.set_dark_mode)
        self.ui.actionLoad.triggered.connect(self.load_from_file_action)
        self.ui.actionSave.triggered.connect(self.save_to_file_action)
        self.ui.actionEnglish.triggered.connect(lambda: self.change_ui_file("en"))
        self.ui.actionGerman.triggered.connect(lambda: self.change_ui_file("de"))

    def disconnect_slots(self):
        self._disconnect_number_slots()
        self.ui.actionBright.triggered.disconnect()
        self.ui.actionDark.triggered.disconnect()
        self.ui.actionLoad.triggered.disconnect()
        self.ui.actionSave.triggered.disconnect()
        self.ui.actionEnglish.triggered.disconnect()

    def _connect_number_slots(self):
        self.ui.numFe1.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.ui.numFe1.valueChanged.connect(lambda num: self.say()) 
        self.ui.numFe2_1.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.ui.numFe2_2.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.ui.numFe2_3.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.ui.numFe2_7.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.ui.numFe2_8.valueChanged.connect(lambda num: self.on_numValue_changed())


    def _disconnect_number_slots(self):
        self.ui.numFe1.valueChanged.disconnect()
        self.ui.numFe2_1.valueChanged.disconnect()
        self.ui.numFe2_2.valueChanged.disconnect()
        self.ui.numFe2_3.valueChanged.disconnect()
        self.ui.numFe2_7.valueChanged.disconnect()
        self.ui.numFe2_8.valueChanged.disconnect()



def main():
    global app
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    #os.chdir(sys.path[1])
    window = MainWindow()

    # from qt_material
    #apply_stylesheet(app, "dark_teal.xml")
    apply_stylesheet(app, "light_blue.xml")

    #window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
