# pyright: reportAttributeAccessIssue=false
import os, sys
from typing import Literal

# TODO: Generate "Zeugnis"
#from PyQt6.QtCore import pyqtSlot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QCoreApplication, Slot, Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
#from PyQt6.uic import loadUi
from qt_material import apply_stylesheet

import DataManager, TTS

GUI_FILENAMES = {"de": "de_DE.ui", "en": "en_GB.ui"}
LANGUAGE: Literal["de", "en"] = "de"
GUI_FILENAME = GUI_FILENAMES[LANGUAGE]
DECIMAL_SEPARATOR = lambda : {"de": ",", "en": "."}[LANGUAGE]
GRADE_AVERAGE_TEXT = lambda : {"de": "Durchschnittsnote: ", "en": "Average grade: "}[LANGUAGE]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app = None


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.loader = QUiLoader()
        print(os.path.join(SCRIPT_DIR, GUI_FILENAME))
        self.ui : QWidget = self.loader.load(os.path.join(SCRIPT_DIR, GUI_FILENAME), None)
        self.ui.show()
        self._initialize_actions()
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
            self.ui.lblFe1Output.setText(str(self.dataManager.fe1_ItWorkstation_Grade).replace(".", DECIMAL_SEPARATOR()))
        if self.dataManager.fe2_PlanningASoftwareProduct_Grade:
            self.ui.lblFe2Output1.setText(str(self.dataManager.fe2_PlanningASoftwareProduct_Grade).replace(".", DECIMAL_SEPARATOR()))
        if self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade:
            self.ui.lblFe2Output2.setText(str(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade).replace(".", DECIMAL_SEPARATOR()))
        if self.dataManager.fe2_EconomicsAndSocialStudies_Grade:
            self.ui.lblFe2Output3.setText(str(self.dataManager.fe2_EconomicsAndSocialStudies_Grade).replace(".", DECIMAL_SEPARATOR()))
        if self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade:
            self.ui.lblFe2Output1_3.setText(str(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade).replace(".", DECIMAL_SEPARATOR()))

        self.set_success()


    def set_success(self):
        passed = self.dataManager.has_passed()
        self.ui.lblSuccessPassed.setHidden(not passed)
        self.ui.lblSuccessFailed.setHidden(passed)
        self.ui.lblAverageGrade.setText(f"{GRADE_AVERAGE_TEXT()}{str(self.dataManager.overall_average_grade).replace('.', DECIMAL_SEPARATOR())}")


    @Slot()
    def on_numValue_changed(self):
        self.load_ui_values_to_data_manager()
        self.set_ui_values_by_data_manager()

    @Slot()
    def set_stylesheet(self, stylesheet_file: str, action_element: QWidget):
        apply_stylesheet(app, f"{stylesheet_file}.xml")
        self.enable_all_styles()
        action_element.setEnabled(False)


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
        global LANGUAGE; LANGUAGE = language
        position = self.ui.pos()
        old_ui = self.ui
        self.ui = self.loader.load(os.path.join(SCRIPT_DIR, GUI_FILENAMES[LANGUAGE]), None)
        self.ui.move(position)
        self.ui.show()
        old_ui.close()
        self._initialize_actions()
        self.connect_slots()
        self.set_ui_values_by_data_manager()


    def _initialize_actions(self):

        self._numberFields = [
            self.ui.numFe1,
            self.ui.numFe2_1,
            self.ui.numFe2_2,
            self.ui.numFe2_3,
            self.ui.numFe2_7,
            self.ui.numFe2_8
        ]

        self._appearanceActions = [
            ( self.ui.actionDarkAmber,    lambda : self.set_stylesheet("dark_amber", self.ui.actionDarkAmber) ),
            ( self.ui.actionDarkBlue,     lambda : self.set_stylesheet("dark_blue", self.ui.actionDarkBlue) ),
            ( self.ui.actionDarkCyan,     lambda : self.set_stylesheet("dark_cyan", self.ui.actionDarkCyan) ),
            ( self.ui.actionDarkGreen,    lambda : self.set_stylesheet("dark_lightgreen", self.ui.actionDarkGreen) ),
            ( self.ui.actionDarkPink,     lambda : self.set_stylesheet("dark_pink", self.ui.actionDarkPink) ),
            ( self.ui.actionDarkPurple,   lambda : self.set_stylesheet("dark_purple", self.ui.actionDarkPurple) ),
            ( self.ui.actionDarkRed,      lambda : self.set_stylesheet("dark_red", self.ui.actionDarkRed) ),
            ( self.ui.actionDarkTeal,     lambda : self.set_stylesheet("dark_teal", self.ui.actionDarkTeal) ),
            ( self.ui.actionDarkYellow,   lambda : self.set_stylesheet("dark_yellow", self.ui.actionDarkYellow) ),
            ( self.ui.actionBrightAmber,  lambda : self.set_stylesheet("light_amber", self.ui.actionBrightAmber) ),
            ( self.ui.actionBrightBlue,   lambda : self.set_stylesheet("light_blue", self.ui.actionBrightBlue) ),
            ( self.ui.actionBrightCyan,   lambda : self.set_stylesheet("light_cyan", self.ui.actionBrightCyan) ),
            ( self.ui.actionBrightGreen,  lambda : self.set_stylesheet("light_lightgreen", self.ui.actionBrightGreen) ),
            ( self.ui.actionBrightPink,   lambda : self.set_stylesheet("light_pink", self.ui.actionBrightPink) ),
            ( self.ui.actionBrightPurple, lambda : self.set_stylesheet("light_purple", self.ui.actionBrightPurple) ),
            ( self.ui.actionBrightRed,    lambda : self.set_stylesheet("light_red", self.ui.actionBrightRed) ),
            ( self.ui.actionBrightTeal,   lambda : self.set_stylesheet("light_teal", self.ui.actionBrightTeal) ),
            ( self.ui.actionBrightYellow, lambda : self.set_stylesheet("light_yellow", self.ui.actionBrightYellow) )
        ]

        self._miscallaneousActions = [
            ( self.ui.actionLoad, self.load_from_file_action ),
            ( self.ui.actionSave, self.save_to_file_action ),
            ( self.ui.actionEnglish, lambda: self.change_ui_file("en") ),
            ( self.ui.actionGerman, lambda: self.change_ui_file("de") ),
        ]

        self._triggeredActions = self._appearanceActions + self._miscallaneousActions


    def enable_all_styles(self):
        for action, _ in self._appearanceActions:
            action.setEnabled(True)

    def _connect_number_slots(self):
        for numField in self._numberFields:
            numField.valueChanged.connect(lambda num: self.on_numValue_changed())

    def _connect_action_slots(self):
        for action, handler in self._triggeredActions:
            action.triggered.connect(handler)

    def connect_slots(self):
        self._connect_number_slots()
        self._connect_action_slots()

    def _disconnect_number_slots(self):
        for numField in self._numberFields:
            numField.valueChanged.disconnect()

    def _disconnect_action_slots(self):
        for action, _ in self._triggeredActions:
            action.triggered.disconnect()

    def disconnect_slots(self):
        self._disconnect_number_slots()
        self._disconnect_action_slots()


def main():
    global app
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MainWindow()

    # from qt_material
    apply_stylesheet(app, "dark_teal.xml")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
