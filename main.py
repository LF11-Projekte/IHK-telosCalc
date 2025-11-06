import os, sys, math

from PyQt6.QtCore import pyqtSlot
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QCoreApplication, Signal, Slot, Qt
from PySide6.QtWidgets import QApplication, QFileDialog
from qt_material import apply_stylesheet

import DataManager

#GUI_FILENAME = "Frontend.ui"
GUI_FILENAME = "untitled.ui"
Form, Base = loadUiType(os.path.join(sys.path[1], GUI_FILENAME))
app = None


class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.connect_slots()
        self.dataManager = DataManager.DataManager(0,0,0,0,0,0,0, None)

    def set_grades(self, input_field, output_label):
        score = None
        if str(input_field.text()).isnumeric():
            score = int(input_field.text())
            grade = calcGrade(score)
            output_label.setText(str(grade))
        return score

    def get_score(self, input_field):
        score = None
        if str(input_field.text()).isnumeric():
            score = int(input_field.text())
        return score

    def on_btnCalc_clicked(self):

        overall_score = 0
        overall_score += .2 * self.set_grades(self.LeFei, self.lblGradeFei)
        overall_score += .1 * self.set_grades(self.LeFeiiProductplanning_2, self.lblGradeFeiiProductplanning)
        overall_score += .1 * self.set_grades(self.LeFeiiAlgorithmdevelopment_2, self.lblGradeFeiiProductplanningAlgorithmdevelopmen)
        overall_score += .1 * self.set_grades(self.LeFeiieconomy_2, self.lblGradeFeiiProductplanningEconomy)
        theory_score = self.set_grades(self.LeExaminationproject_2, self.lblGradeExaminationprojecti)
        oral_score = self.set_grades(self.LeExaminationprojectDefence_2, self.lblGradeExaminationprojecti)

        overall_score += .25 * theory_score + .25 * oral_score

        self.dataManager(self.get_score(self.LeFei),
                         self.get_score(self.LeFeiiProductplanning_2),
                         self.get_score(self.LeFeiiAlgorithmdevelopment_2),
                         self.get_score(self.LeFeiieconomy_2),
                         self.get_score(self.LeExaminationproject_2),
                         self.get_score(self.LeExaminationprojectDefence_2)
        )

        self.lblGradeExaminationprojecti.setText(str(
            calcGrade(math.ceil(.5 * theory_score + .5 * oral_score))
        ))

        overall_grade = calcGrade(math.ceil(overall_score))

        self.lblTotalResult.setText("Note: " + str(
            calcGrade(math.ceil(overall_score))
        ))

        self.lblpassed.setText("nicht bestanden" if overall_grade > 4.4 else "bestanden")

    def on_btnSave_clicked(self):
        options = None  # QFileDialog.Option.DontUseNativeDialog
        fileName, filter = QFileDialog.getSaveFileName(self,
                                                       caption="Datei speichern",
                                                       filter="Alle Typen (*);;JSON (*.json)")
        self.dataManager.saveToFile(fileName)

    def set_success(self):
        self.lblSuccess.setText("Die Prüfung wurde bestanden." if self.dataManager.has_passed() else "Die Prüfung wurde nicht bestanden.")

    def on_numValue1_changed(self, num: int):
        self.dataManager.fe1_ItWorkstation = num
        self.dataManager.calculate_all_grades()
        self.lblFe1Output.setText(str(self.dataManager.fe1_ItWorkstation_Grade))
        self.set_success()


    def on_numValue2_changed(self, num: int):
        self.dataManager.fe2_PlanningASoftwareProduct = num
        self.dataManager.calculate_all_grades()
        self.lblFe2Output1.setText(str(self.dataManager.fe2_PlanningASoftwareProduct_Grade))
        self.set_success()

    def on_numValue3_changed(self, num: int):
        self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms = num
        self.dataManager.calculate_all_grades()
        self.lblFe2Output2.setText(str(self.dataManager.fe2_DevelopmentAndImplementationOfAlgorithms_Grade))
        self.set_success()

    def on_numValue4_changed(self, num: int):
        self.dataManager.fe2_EconomicsAndSocialStudies = num
        self.dataManager.calculate_all_grades()
        self.lblFe2Output3.setText(str(self.dataManager.fe2_EconomicsAndSocialStudies_Grade))
        self.set_success()

    def on_numValue5_changed(self, num: int):
        self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Written = self.numFe2_7.value
        self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Oral = self.numFe2_8.value
        self.dataManager.calculate_all_grades()
        self.numFe2_6.setValue(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Score)
        self.lblFe1Output.setText(str(self.dataManager.fe2_PlanningAndImplementingASoftwareProduct_Grade))
        self.set_success()

    def set_dark_mode(self):
        apply_stylesheet(app, "dark_teal.xml")
    def set_bright_mode(self):
        apply_stylesheet(app, "light_blue.xml")

    def connect_slots(self):
        self.numFe1.valueChanged.connect(lambda num: self.on_numValue1_changed(num))
        self.numFe2_1.valueChanged.connect(lambda num: self.on_numValue2_changed(num))
        self.numFe2_2.valueChanged.connect(lambda num: self.on_numValue3_changed(num))
        self.numFe2_3.valueChanged.connect(lambda num: self.on_numValue4_changed(num))
        self.numFe2_7.valueChanged.connect(lambda num: self.on_numValue5_changed(num))
        self.numFe2_8.valueChanged.connect(lambda num: self.on_numValue5_changed(num))
        self.actionBright.triggered.connect(self.set_bright_mode)
        self.actionDark.triggered.connect(self.set_dark_mode)
        #self.btnSave.clicked.connect(self.on_btnSave_clicked)
        pass



def main():
    global app
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    os.chdir(sys.path[1])
    widget = MainWindow()

    # from qt_material
    #apply_stylesheet(app, "dark_teal.xml")
    apply_stylesheet(app, "light_blue.xml")

    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
