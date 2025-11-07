import time
import os, sys, math, pathlib, ctypes
from typing import Literal


#from PyQt6.QtCore import pyqtSlot
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QCoreApplication, Signal, Slot, Qt
from PySide6.QtWidgets import QApplication, QFileDialog
from qt_material import apply_stylesheet

import DataManager

#GUI_FILENAME = "Frontend.ui"
DE_UI_FILENAME = "de_DE.ui"
EN_UI_FILENAME = "en_EN.ui"
GUI_FILENAME = "de_DE.ui"
LANGUAGE: Literal["DE", "EN"] = "DE"
Form, Base = loadUiType(os.path.join(pathlib.Path(__file__).parent.resolve(), GUI_FILENAME)) # type: ignore
app = None


class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.connect_slots()
        self.dataManager = DataManager.DataManager(0,0,0,0,0,0,0, None)
        self.dataManager.calculate_all_grades()
        self.set_ui_values_by_data_manager()


    def load_ui_values_to_data_manager(self):
        self.dataManager.set_all_values(
            fe1_ItWorkstation=self.numFe1.value(),
            fe2_PlanningASoftwareProduct=self.numFe2_1.value(),
            fe2_DevelopmentAndImplementationOfAlgorithms=self.numFe2_2.value(),
            fe2_EconomicsAndSocialStudies=self.numFe2_3.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Oral=self.numFe2_8.value(),
            fe2_PlanningAndImplementingASoftwareProduct_Written=self.numFe2_7.value(),
            fe2_OralSupplementaryExamination=None,
            fe2_OralSupplementaryExaminationSubject=None
        )


    def set_ui_values_by_data_manager(self):
        self.numFe1.setValue(self.dataManager.fe1_ItWorkstation)
        self.numFe2_1.setValue(self.dataManager.fe2_PlanningASoftwareProduct)
        self.numFe2_2.setValue(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms)
        self.numFe2_3.setValue(self.dataManager.fe2_EconomicsAndSocialStudies)
        self.numFe2_7.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Written)
        self.numFe2_8.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Oral)
        self.numFe2_out.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Score)

        if self.dataManager.fe1_ItWorkstation_Grade:
            self.lblFe1Output.setText(str(self.dataManager.fe1_ItWorkstation_Grade))
        if self.dataManager.fe2_PlanningASoftwareProduct_Grade:
            self.lblFe2Output1.setText(str(self.dataManager.fe2_PlanningASoftwareProduct_Grade))
        if self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade:
            self.lblFe2Output2.setText(str(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade))
        if self.dataManager.fe2_EconomicsAndSocialStudies_Grade:
            self.lblFe2Output3.setText(str(self.dataManager.fe2_EconomicsAndSocialStudies_Grade))
        if self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade:
            self.lblFe2Output1_3.setText(str(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade))

        self.set_success()


    def set_success(self):
        self.lblSuccess.setText("Die Prüfung wurde bestanden." if self.dataManager.has_passed() else "Die Prüfung wurde nicht bestanden.")


    def on_numValue_changed(self):
        self.load_ui_values_to_data_manager()
        self.set_ui_values_by_data_manager()


    def set_dark_mode(self):
        apply_stylesheet(app, "dark_teal.xml")


    def set_bright_mode(self):
        apply_stylesheet(app, "light_blue.xml")


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


    def save_to_file_action(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  caption="Eingabeparameter in Datei speichern",
                                                  filter="Alle Typen (*);;JSON (*.json)")
        if fileName:
            self.dataManager.saveToFile(fileName)


    def connect_slots(self):
        self._connect_number_slots()
        self.actionBright.triggered.connect(self.set_bright_mode)
        self.actionDark.triggered.connect(self.set_dark_mode)
        self.actionLoad.triggered.connect(self.load_from_file_action)
        self.actionSave.triggered.connect(self.save_to_file_action)


    def _connect_number_slots(self):
        self.numFe1.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.numFe2_1.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.numFe2_2.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.numFe2_3.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.numFe2_7.valueChanged.connect(lambda num: self.on_numValue_changed())
        self.numFe2_8.valueChanged.connect(lambda num: self.on_numValue_changed())


    def _disconnect_number_slots(self):
        self.numFe1.valueChanged.disconnect()
        self.numFe2_1.valueChanged.disconnect()
        self.numFe2_2.valueChanged.disconnect()
        self.numFe2_3.valueChanged.disconnect()
        self.numFe2_7.valueChanged.disconnect()
        self.numFe2_8.valueChanged.disconnect()



def main():
    global app
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    #os.chdir(sys.path[1])
    widget = MainWindow()

    # from qt_material
    #apply_stylesheet(app, "dark_teal.xml")
    apply_stylesheet(app, "light_blue.xml")

    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
