# pyright: reportAttributeAccessIssue=false
import os, sys
from typing import Literal

# TODO: Generate "Zeugnis"
# TODO: Save configuration
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
from PyQt6.uic.load_ui import loadUi
from qt_material import apply_stylesheet

import DataManager
from HoverEventFilter import HoverEventFilter
from Config import Config
from TTS import TTS

CONFIGURATION = "telosCalc.conf"
DECIMAL_SEPARATOR = lambda : {"de": ",", "en": "."}[Config.LANGUAGE]
MSG_FILTER = lambda : {"de" : "Alle Typen (*);;JSON (*.json)", "en": "All types (*);;JSON (*.json)"}[Config.LANGUAGE]
MSG_LOAD_FILE = lambda : {"de" : "Bitte Eingabeparameterdatei auswählen", "en": "Please select a file to load input data from . . ."}[Config.LANGUAGE]
MSG_SAVE_FILE = lambda : {"de" : "Bitte Eingabeparameter in Datei speichern", "en": "Please save the input data to a file . . ."}[Config.LANGUAGE]
GRADE_AVERAGE_TEXT = lambda : {"de": "Durchschnittsnote: ", "en": "Average grade: "}[Config.LANGUAGE]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app = None


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui : QWidget = loadUi(os.path.join(SCRIPT_DIR, Config.GUI_SRC[Config.LANGUAGE]), None)

        self._oralSupplementaryExaminationEnabled: bool = False
        self._selectedSupplementaryExam: Literal["PlanningASoftwareProduct", "DevelopmentAndImplementationOfAlgorithms", "EconomicsAndSocialStudies"] | None = None

        self._initialize_actions()
        self.connect_slots()

        self.dataManager = DataManager.DataManager(0,0,0,0,0,0,0, None)
        self.dataManager.calculate_all_grades()  
        self.set_ui_values_by_data_manager()
        self.ui.show()


    def load_ui_values_to_data_manager(self):
        self.dataManager.set_all_values(
            fe1_ItWorkstation=self.ui.numFe1.value(),
            fe2_PlanningASoftwareProduct=self.ui.numFe2_1.value(),
            fe2_DevelopmentAndImplementationOfAlgorithms=self.ui.numFe2_2.value(),
            fe2_EconomicsAndSocialStudies=self.ui.numFe2_3.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Oral=self.ui.numFe2_8.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Written=self.ui.numFe2_7.value(),
            fe2_OralSupplementaryExamination=self.ui.numFe2_supplementary.value(),
            fe2_OralSupplementaryExaminationSubject=self._selectedSupplementaryExam
        )


    def set_ui_values_by_data_manager(self):

        if len(self.dataManager.may_take_supplementary_exam()):
            self._switchOralSupplementaryExamination(True)
        else:
            self._switchOralSupplementaryExamination(False)
            self.dataManager.fe2_OralSupplementaryExamination = 0
            self.dataManager.fe2_OralSupplementaryExaminationSubject = None

        self.ui.numFe1.setValue(self.dataManager.fe1_ItWorkstation) 
        self.ui.numFe2_1.setValue(self.dataManager.fe2_PlanningASoftwareProduct) 
        self.ui.numFe2_2.setValue(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms) 
        self.ui.numFe2_3.setValue(self.dataManager.fe2_EconomicsAndSocialStudies) 
        self.ui.numFe2_7.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Written) 
        self.ui.numFe2_8.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Oral) 
        self.ui.numFe2_out.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Score)
        self.ui.numFe2_supplementary.setValue(self.dataManager.fe2_OralSupplementaryExamination)


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


    def _enable_eligible_supplementary_exams(self, eligible_exams):
        if self._selectedSupplementaryExam in eligible_exams: eligible_exams.remove(self._selectedSupplementaryExam)

        self.ui.actionPlanningASoftwareProduct.setEnabled(
            self._oralSupplementaryExaminationEnabled and "PlanningASoftwareProduct" in eligible_exams)
        self.ui.actionDevelopmentAndImplementationOfAlgorithms.setEnabled(
            self._oralSupplementaryExaminationEnabled and "DevelopmentAndImplementationOfAlgorithms" in eligible_exams)
        self.ui.actionEconomicsAndSocialStudies.setEnabled(
            self._oralSupplementaryExaminationEnabled and "EconomicsAndSocialStudies" in eligible_exams)
        self.ui.actionNoSupplementaryExam.setEnabled(self._oralSupplementaryExaminationEnabled and self._selectedSupplementaryExam is not None)


    def _switchOralSupplementaryExamination(self, is_enabled: bool):
        if self._oralSupplementaryExaminationEnabled == is_enabled: pass
        self._oralSupplementaryExaminationEnabled = is_enabled
        self.ui.tbtnSupplementary.setEnabled(self._oralSupplementaryExaminationEnabled)
        #self.ui.numFe2_supplementary.setEnabled(self._oralSupplementaryExaminationEnabled)

        eligible_exams = self.dataManager.may_take_supplementary_exam()
        self._enable_eligible_supplementary_exams(eligible_exams)

        if not self._oralSupplementaryExaminationEnabled:
            self.ui.numFe2_supplementary.setValue(0)
            return


    def set_success(self):
        passed = self.dataManager.has_passed()
        self.ui.lblSuccessPassed.setHidden(not passed)
        self.ui.lblSuccessFailed.setHidden(passed)
        self.ui.lblAverageGrade.setText(f"{GRADE_AVERAGE_TEXT()}{str(self.dataManager.overall_average_grade).replace('.', DECIMAL_SEPARATOR())}")


    @pyqtSlot()
    def on_numValue_changed(self):
        self.load_ui_values_to_data_manager()
        self.set_ui_values_by_data_manager()


    @pyqtSlot()
    def set_stylesheet(self, stylesheet_file: str, action_element: QWidget):
        Config.STYLE = stylesheet_file
        apply_stylesheet(app, f"{stylesheet_file}.xml")
        self.enable_all_styles()
        action_element.setEnabled(False)


    @pyqtSlot()
    def load_from_file_action(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, caption=MSG_LOAD_FILE(), filter=MSG_FILTER())
        if fileName:
            self._disconnect_number_slots()
            self.dataManager.loadFromFile(fileName)
            self.dataManager.calculate_all_grades()
            self._selectedSupplementaryExam = self.dataManager.fe2_OralSupplementaryExaminationSubject
            self.set_ui_values_by_data_manager()
            self._connect_number_slots()


    @pyqtSlot()
    def save_to_file_action(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, caption=MSG_SAVE_FILE(), filter=MSG_FILTER())
        if fileName:
            self.dataManager.saveToFile(fileName)


    def say(self):
        TTS.speak("Hello, this is a test.", language="fr-fr")
        TTS.speak("Hallo, dies ist ein Test.", language="de-de")

    def _speak_text(self, text: str):
        """Speak the given text using TTS in the current language."""
        language = "de-de" if Config.LANGUAGE == "de" else "en-us"
        try:
            TTS.speak(text, language=language)
        except Exception as e:
            print(f"[TTS-ERROR] {e}")

    def _stop_tts(self):
        """Stop current TTS playback immediately."""
        try:
            TTS.stop()
        except Exception as e:
            print(f"[TTS-STOP-ERROR] {e}")


    def change_ui_file(self, language: Literal["de", "en"]):
        self.disconnect_slots()
        Config.LANGUAGE = language
        position = self.ui.pos()
        old_ui = self.ui
        self.ui = loadUi(os.path.join(SCRIPT_DIR, Config.GUI_SRC[Config.LANGUAGE]), None)
        self.ui.move(position)
        self._initialize_actions()
        self.connect_slots()
        self.set_ui_values_by_data_manager()
        self.ui.show()
        old_ui.close()


    def set_supplementary_exam(self, exam: Literal["PlanningASoftwareProduct", "DevelopmentAndImplementationOfAlgorithms", "EconomicsAndSocialStudies"] | None, element):
        self.dataManager.fe2_OralSupplementaryExaminationSubject = exam
        self._selectedSupplementaryExam = exam
        exams = self.dataManager.may_take_supplementary_exam()
        self._enable_eligible_supplementary_exams(exams)
        self.ui.numFe2_supplementary.setEnabled(exam is not None)
        if exam is None: self.ui.numFe2_supplementary.setValue(0)
        element.setEnabled(False)
        self.load_ui_values_to_data_manager()
        self.set_ui_values_by_data_manager()


    def _initialize_actions(self):

        self._numberFields = [
            self.ui.numFe1,
            self.ui.numFe2_1,
            self.ui.numFe2_2,
            self.ui.numFe2_3,
            self.ui.numFe2_7,
            self.ui.numFe2_8,
            self.ui.numFe2_supplementary
        ]


        # Install hover event filters on all number fields
        self._hoverFilters = []
        field_configs = [
            ("numFe1", self.ui.numFe1, self.ui.lblDescr1),
            ("numFe2_1", self.ui.numFe2_1, self.ui.lblDescr2),
            ("numFe2_2", self.ui.numFe2_2, self.ui.lblDescr3),
            ("numFe2_3", self.ui.numFe2_3, self.ui.lblDescr3_2),
            ("numFe2_7", self.ui.numFe2_7, self.ui.lblDescr3_5),
            ("numFe2_8", self.ui.numFe2_8, self.ui.lblDescr3_6),
            ("numFe2_supplementary", self.ui.numFe2_supplementary, self.ui.label),
        ]
        for name, field, label_widget in field_configs:
            hover_filter = HoverEventFilter(name, label_widget, self._speak_text, self._stop_tts)
            field.installEventFilter(hover_filter)
            self._hoverFilters.append(hover_filter)

        # Make QToolButton keyboard-accessible (Tab + Enter/Space to open menu)
        #self.ui.tbtnSupplementary.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Connect button click to show menu (works with Tab + Space/Enter via pressed signal)
        self.ui.tbtnSupplementary.pressed.connect(self.ui.tbtnSupplementary.showMenu)


        self._supplementaryExamActions = [
            (self.ui.actionNoSupplementaryExam,                       lambda : self.set_supplementary_exam(None, self.ui.actionNoSupplementaryExam)),
            (self.ui.actionPlanningASoftwareProduct,                  lambda : self.set_supplementary_exam("PlanningASoftwareProduct", self.ui.actionPlanningASoftwareProduct)),
            (self.ui.actionDevelopmentAndImplementationOfAlgorithms,  lambda : self.set_supplementary_exam("DevelopmentAndImplementationOfAlgorithms", self.ui.actionDevelopmentAndImplementationOfAlgorithms)),
            (self.ui.actionEconomicsAndSocialStudies,                 lambda : self.set_supplementary_exam("EconomicsAndSocialStudies", self.ui.actionEconomicsAndSocialStudies))
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

        self._miscellaneousActions = [
            ( self.ui.actionLoad, self.load_from_file_action ),
            ( self.ui.actionSave, self.save_to_file_action ),
            ( self.ui.actionEnglish, lambda: self.change_ui_file("en") ),
            ( self.ui.actionGerman, lambda: self.change_ui_file("de") ),
        ]

        self._triggeredActions = self._appearanceActions + self._miscellaneousActions + self._supplementaryExamActions


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
    Config.load(CONFIGURATION)
    app = QApplication(sys.argv)
    

    # from qt_material
    apply_stylesheet(app, f"{Config.STYLE}.xml")
    window = MainWindow()

    res = app.exec()
    Config.save(CONFIGURATION)
    sys.exit(res)

if __name__ == "__main__":
    main()

