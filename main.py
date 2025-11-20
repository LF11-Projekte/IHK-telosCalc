# pyright: reportAttributeAccessIssue=false
import os, sys
from typing import Literal
#import random
import subprocess

# TODO: Generate "Zeugnis"
# TODO: Save configuration
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QMessageBox
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtGui import QKeySequence
from qt_material import apply_stylesheet

import DataManager
from HoverEventFilter import HoverEventFilter
from Config import Config
from TTS import TTS
from PyQt6.QtCore import QEvent, QObject

CONFIGURATION = "telosCalc.conf"
DECIMAL_SEPARATOR = lambda : {"de": ",", "en": "."}[Config.LANGUAGE]
MSG_FILTER = lambda : {"de" : "Alle Typen (*);;JSON (*.json)", "en": "All types (*);;JSON (*.json)"}[Config.LANGUAGE]
MSG_LOAD_FILE = lambda : {"de" : "Bitte Eingabeparameterdatei auswählen", "en": "Please select a file to load input data from . . ."}[Config.LANGUAGE]
MSG_SAVE_FILE = lambda : {"de" : "Bitte Eingabeparameter in Datei speichern", "en": "Please save the input data to a file . . ."}[Config.LANGUAGE]
MSG_LOAD_FILE_CRITICAL = lambda : {"de": "Fehler beim Öffnen der Datei", "en": "Error opening the file"}[Config.LANGUAGE]
MSG_LOAD_FILE_CRITICAL_TEXT = lambda : {"de": "Datei konnte nicht geladen werden.\nBitte sicherstellen, dass Datei vom Programm stammt.", "en": "The file could not be loaded.\nPlease ensure that the file originates from the program."}[Config.LANGUAGE]
GRADE_AVERAGE_TEXT = lambda : {"de": "Durchschnittsnote: ", "en": "Average grade: "}[Config.LANGUAGE]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_FILE = lambda : os.path.join(SCRIPT_DIR, f"{(lambda: {"de": "de_DE", "en" : "en_GB"}[Config.LANGUAGE])()}.pdf")
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
            try:
                self._disconnect_number_slots()
                self.dataManager.loadFromFile(fileName)
                self.dataManager.calculate_all_grades()
                self._selectedSupplementaryExam = self.dataManager.fe2_OralSupplementaryExaminationSubject
                self.set_ui_values_by_data_manager()
                self._connect_number_slots()
            except Exception as e:
                _ = QMessageBox.critical(self,
                    MSG_LOAD_FILE_CRITICAL(),
                    MSG_LOAD_FILE_CRITICAL_TEXT())


    @pyqtSlot()
    def save_to_file_action(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, caption=MSG_SAVE_FILE(), filter=MSG_FILTER())
        if fileName:
            self.dataManager.saveToFile(fileName)


    def _speak_text(self, text: str):
        """Speak the given text using TTS in the current language."""
        #print(f"Config.SPEECH_ON: {Config.SPEECH_ON}")
        if not Config.SPEECH_ON: return

        language = "de-de" if Config.LANGUAGE == "de" else "en-us"
        try:
            TTS.speak(text, language=language)
        except Exception as e:
            #print(f"[TTS-ERROR] {e}")
            pass

    def _stop_tts(self):
        """Stop current TTS playback immediately."""
        try:
            TTS.stop()
        except Exception as e:
            #print(f"[TTS-STOP-ERROR] {e}")
            pass

    def _toggle_speech_and_sync_button(self):
        """Toggle speech output and sync the Announce Grades button state."""
        Config.toggle_speech_on()
        # Update button enabled state
        if self.ui.btnAnnounceGrades:
            self.ui.btnAnnounceGrades.setEnabled(Config.SPEECH_ON)


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


    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("telosCalc.exe")
        msg.setInformativeText((lambda : {"de": "Version: 1.0\nLetztes Release 2025-11-13\nAutoren: Karl Jahn, Damian Carstens, Kai Weißenborn",
                                          "en": "Version: 1.0\nLast Release 2025-11-13\nAuthors: Karl Jahn, Damian Carstens, Kai Weißenborn"}[Config.LANGUAGE])())
        msg.setWindowTitle((lambda : {"de": "Informationen über die Anwendung", "en": "Information about the application"}[Config.LANGUAGE])())
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()


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

        # Make menu bar keyboard-accessible and provide TTS feedback
        try:
            menu_bar = getattr(self.ui, 'menuBar', None)
            if menu_bar:
                # Some UI objects expose menuBar as a method; call it if so.
                if callable(menu_bar):
                    menu_bar = menu_bar()

                menu_bar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

                # F10 focuses the menu bar (common convention). Some PyQt6
                # builds don't expose QShortcut as expected, so use a fallback
                # that creates an QAction with a shortcut when QShortcut is
                # unavailable.
                try:
                    from PyQt6.QtWidgets import QShortcut
                    shortcut = QShortcut(QKeySequence('F10'), self)
                    shortcut.activated.connect(lambda mb=menu_bar: self._focus_menubar(mb))
                except Exception:
                    # If QShortcut isn't available we still support F10 via
                    # keyPressEvent override (see MainWindow.keyPressEvent)
                    #print("[MENU-SHORTCUT-INIT] QShortcut unavailable; using keyPressEvent fallback")
                    pass

                # Speak menu titles and actions on hover (works with keyboard nav)
                for top_action in menu_bar.actions():
                    # speak top-level menu title when highlighted
                    top_action.hovered.connect(lambda a=top_action: (self._stop_tts(), self._speak_text(a.text().replace('&', ''))))
                    menu = top_action.menu()
                    if menu:
                        for act in menu.actions():
                            # speak each submenu/action when hovered (keyboard or mouse)
                            act.hovered.connect(lambda aa=act: (self._stop_tts(), self._speak_text(aa.text().replace('&', ''))))
        except Exception as e:
            #print(f"[MENU-TTS-INIT-ERROR] {e}")
            pass


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

        hover_filter = HoverEventFilter("btnAnnounceGrades", self.ui.lblAnnounce, self._speak_text, self._stop_tts)
        self.ui.btnAnnounceGrades.installEventFilter(hover_filter)
        self._hoverFilters.append(hover_filter)
        self.ui.btnAnnounceGrades.pressed.connect(self._announce_grades)

        # Keep a mapping from field widget -> label widget for announcements
        self._fieldLabelMap = { field: label_widget for name, field, label_widget in field_configs }

        self.ui.tbtnSupplementary.pressed.connect(self.ui.tbtnSupplementary.showMenu)
        self.ui.actionVoiceOutput.setChecked(Config.SPEECH_ON)
        self.ui.btnAnnounceGrades.setEnabled(Config.SPEECH_ON)


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
            ( self.ui.actionVoiceOutput, self._toggle_speech_and_sync_button ),
            ( self.ui.actionAbout, self.show_info_messagebox),
            ( self.ui.actionOpenDocs,  lambda : subprocess.Popen(DOC_FILE(), shell=True) )
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

    def _focus_menubar(self, menu_bar):
        """Set keyboard focus to the menu bar and activate the first menu."""
        try:
            menu_bar.setFocus()
            actions = menu_bar.actions()
            if actions:
                menu_bar.setActiveAction(actions[0])
        except Exception as e:
            #print(f"[MENU-FOCUS-ERROR] {e}")
            pass

    def _announce_grades(self):
        """Collect grades and announce them via TTS (localized)."""
        lang = Config.LANGUAGE
        # Localized labels

        assults = [
            "Mal ist man der Hund, mal ist man der Baum.",
            "Man kann nicht immer der Held sein, manchmal ist man der Statist im Hintergrund.",
            "Manche Menschen lernen aus Fehlern, du scheinst sie zu sammeln.",
            "Keine Sorge, der Tiefpunkt ist erreicht – jetzt geht’s nur noch bergauf … oder bergab, je nachdem, wie man's sieht",
            "Glückwunsch, du hast den Beweis geliefert, dass Intelligenz optional ist.",
            "Prüfung nicht bestanden? Keine Panik, man kann auch später Millionär werden … als Reality-TV-Star.",
            "Herzlichen Glückwunsch! Du hast es geschafft, mehr zu scheitern als erwartet."
        ]

        labels = {
            'de': {
                'title': 'Noten . . ',
                'fe1': 'Einrichten eines IT-gestützten Arbeitsplatzes. ',
                'fe2_1': 'Planen eines Softwareproduktes. ',
                'fe2_2': 'Entwicklung und Umsetzung von Algorithmen. ',
                'fe2_3': 'Wirtschaft und Sozialkunde. ',
                'fe2_proj': 'Planen und Umsetzen eines Softwareprojektes. ',
                'average': 'Durchschnitts-Nohte. ',      # Er würde anstatt "Durchschnittsnote" "Durchschnittsnot" sagen "Durchschnitts-Notä" klingt dem eigentlichen Wort am nächsten
                'passed': 'Die Prüfung wurde damit bestanden. Herzlichen Glückwunsch!',
                'failed': 'Prüfung wurde damit nicht bestanden. Mal ist man der Hund, mal ist man der Baum . . . Ha .  Ha .  Ha',
                'na': 'nicht vorhanden'
            },
            'en': {
                'title': 'Grades',
                'fe1': 'IT workstation',
                'fe2_1': 'Planning a Software Product',
                'fe2_2': 'Development and Implementation of Algorithms',
                'fe2_3': 'Economics and Social Studies',
                'fe2_proj': 'Company Project',
                'average': 'Average grade',
                'passed': 'Examination passed',
                'failed': 'Examination failed',
                'na': 'not available'
            }
        }

        loc = labels['de'] if Config.LANGUAGE == 'de' else labels['en']

        def fmt(g):
            if g is None:
                return loc['na']
            # Use comma for German decimal separator
            s = f"{g:.1f}"
            if Config.LANGUAGE == 'de':
                s = s.replace('.', ',')
            return s

        parts = [f"{loc['title']}: "]
        parts.append(f"{loc['fe1']}: {fmt(self.dataManager.fe1_ItWorkstation_Grade)}")
        parts.append(f"{loc['fe2_1']}: {fmt(self.dataManager.fe2_PlanningASoftwareProduct_Grade)}")
        parts.append(f"{loc['fe2_2']}: {fmt(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade)}")
        parts.append(f"{loc['fe2_3']}: {fmt(self.dataManager.fe2_EconomicsAndSocialStudies_Grade)}")
        parts.append(f"{loc['fe2_proj']}: {fmt(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade)}")
        avg = self.dataManager.overall_average_grade
        parts.append(f"{loc['average']}: {fmt(avg)}")

        passed = self.dataManager.has_passed()
        parts.append(loc['passed'] if passed else loc['failed'])

        # Use longer separator for better pause between grades
        separator = ". " if lang == 'en' else ". . . "
        text = separator.join(parts)
        self._stop_tts()
        self._speak_text(text)

    def _announce_current_field_value(self):
        """Announce the currently focused number field's point value (localized)."""
        fw = QApplication.focusWidget()
        # If focus widget is one of our number fields or a child, match it
        matched_field = None
        for f in self._fieldLabelMap.keys():
            if fw is f:
                matched_field = f
                break

        if matched_field is None:
            # Try parent chain (sometimes focus is on spinbox's lineEdit)
            p = fw
            while p is not None:
                if p in self._fieldLabelMap:
                    matched_field = p
                    break
                p = getattr(p, 'parent', lambda: None)()

        if matched_field is None:
            # Nothing to announce
            return

        label_widget = self._fieldLabelMap.get(matched_field)
        label_text = label_widget.text() if label_widget is not None else matched_field.objectName()
        value = None
        try:
            value = matched_field.value()
        except Exception:
            # Fallback: try to get text
            try:
                value = int(matched_field.text())
            except Exception:
                value = None

        if Config.LANGUAGE == 'de':
            unit = 'Punkte'
        else:
            unit = 'points'

        if value is None:
            speak_text = f"{label_text}: { 'nicht vorhanden' if Config.LANGUAGE=='de' else 'not available' }"
        else:
            speak_text = f"{label_text}: {value} {unit}"

        self._stop_tts()
        self._speak_text(speak_text)

    def keyPressEvent(self, a0):
        """Catch F10 as fallback to focus the menu bar when QShortcut isn't
        available in this PyQt build.
        """
        try:
            if a0 is not None and a0.key() == Qt.Key.Key_F10:
                menu_bar = getattr(self.ui, 'menuBar', None)
                if callable(menu_bar):
                    menu_bar = menu_bar()
                if menu_bar:
                    self._focus_menubar(menu_bar)
                    return
            # Ctrl+G -> announce grades
            if a0 is not None and a0.key() == Qt.Key.Key_G and a0.modifiers() & Qt.KeyboardModifier.ControlModifier:
                try:
                    self._announce_grades()
                except Exception as e:
                    #print(f"[ANNOUNCE-GRADES-ERROR] {e}")
                    pass
                return
            # Enter/Return -> if a number field is focused, announce its points
            if a0 is not None and (a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter):
                try:
                    self._announce_current_field_value()
                except Exception as e:
                    #print(f"[ANNOUNCE-FIELD-ERROR] {e}")
                    pass
                return
        except Exception:
            pass

        # Delegate to base class for other keys
        return super().keyPressEvent(a0)

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

