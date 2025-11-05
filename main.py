import os, sys, math
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QCoreApplication, Signal, Slot, Qt
from PySide6.QtWidgets import QApplication, QFileDialog
from qt_material import apply_stylesheet

import DataManager

GUI_FILENAME = "Frontend.ui"
Form, Base = loadUiType(os.path.join(sys.path[1], GUI_FILENAME))

def VALIDATE(condition):
    if not condition:
        raise Exception("Validation failed!")

def calcGrade(score: int):
    GRADES_JMPTBL = [6.0,6.0,6.0,6.0,6.0,5.9,5.9,5.9,5.9,5.9,5.8,5.8,5.8,5.8,5.8,5.7,5.7,5.7,5.7,5.7,5.6,5.6,5.6,5.6,5.6,5.5,5.5,5.5,5.5,5.5,5.4,5.4,5.3,5.3,5.2,5.2,5.1,5.1,5.0,5.0,4.9,4.9,4.8,4.8,4.7,4.7,4.6,4.6,4.5,4.5,4.4,4.3,4.3,4.2,4.2,4.1,4.0,4.0,3.9,3.9,3.8,3.8,3.7,3.6,3.6,3.5,3.5,3.4,3.3,3.3,3.2,3.1,3.0,3.0,2.9,2.8,2.8,2.7,2.6,2.5,2.5,2.4,2.3,2.2,2.1,2.0,2.0,1.9,1.8,1.7,1.6,1.5,1.4,1.4,1.3,1.3,1.2,1.2,1.1,1.1,1.0]
    VALIDATE(100 >= score >= 0)
    return GRADES_JMPTBL[score]


class MainWindow(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.connect_slots()
        self.dataManager = None

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

    def connect_slots(self):
        self.btnCalc.clicked.connect(self.on_btnCalc_clicked)
        self.btnSave.clicked.connect(self.on_btnSave_clicked)



def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    os.chdir(sys.path[1])
    widget = MainWindow()

    # from qt_material
    apply_stylesheet(app, "dark_teal.xml")
    #apply_stylesheet(app, "light_blue.xml")

    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
