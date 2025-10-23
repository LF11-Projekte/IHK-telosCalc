import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Frontend.ui", self)
        self.show()

class ScoreData:
    FeI_WorkplaceConf: int = None
    FeII_SoftwareProdPlanning: int = None
    FeII_AlgorithmDev: int = None
    FeII_Economy: int = None
    FeII_ProjectWork: int = None
    FeII_ProjectDefence: int = None

class ExamResultData:
    FinalMark: int = None
    FeI_Mark: int = None
    FeI_WorkplaceConfMark: None
    FeII_Mark: int = None
    FeII_AlgorithmDevMark: int = None
    FeII_EconomyMark: int = None
    FeII_ProjectOverallMark: int = None



def VALIDATE(condition):
    if not condition:
        raise Exception("Validation failed!")

def calcGrade(score: int):
    GRADES_JMPTBL = [6.0,6.0,6.0,6.0,6.0,5.9,5.9,5.9,5.9,5.9,5.8,5.8,5.8,5.8,5.8,5.7,5.7,5.7,5.7,5.7,5.6,5.6,5.6,5.6,5.6,5.5,5.5,5.5,5.5,5.5,5.4,5.4,5.3,5.3,5.2,5.2,5.1,5.1,5.0,5.0,4.9,4.9,4.8,4.8,4.7,4.7,4.6,4.6,4.5,4.5,4.4,4.3,4.3,4.2,4.2,4.1,4.0,4.0,3.9,3.9,3.8,3.8,3.7,3.6,3.6,3.5,3.5,3.4,3.3,3.3,3.2,3.1,3.0,3.0,2.9,2.8,2.8,2.7,2.6,2.5,2.5,2.4,2.3,2.2,2.1,2.0,2.0,1.9,1.8,1.7,1.6,1.5,1.4,1.4,1.3,1.3,1.2,1.2,1.1,1.1,1.0]
    VALIDATE(100 >= score >= 0)
    return GRADES_JMPTBL[score]

def calcExamResults(scores: ScoreData):
    scores.FeI_WorkplaceConf

def main():
    score = input("Score: ")
    print(calcGrade(int(score)))
    pass

if __name__ == "__main__":
    main()
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    app.exec()
