import os, sys
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QCoreApplication, Signal, Slot, Qt
from PySide6.QtWidgets import QApplication

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

    def on_btnCalc_clicked(self):
        if str(self.LeFei.text()).isnumeric():
            scoreFe1 = int(self.LeFei.text())
            self.lblGradeFei.setText(str(calcGrade(scoreFe1)))

    def connect_slots(self):
        self.btnCalc.clicked.connect(self.on_btnCalc_clicked)



def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    os.chdir(sys.path[1])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
