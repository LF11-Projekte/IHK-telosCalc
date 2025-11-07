import json, math
from typing import List, Literal, Optional


class DataManager:

    def __init__(self,
                 fe1_ItWorkstation: int | None,
                 fe2_PlanningASoftwareProduct: int | None,
                 fe2_DevelopmentAndImplementationOfAlgorithms: int | None,
                 fe2_EconomicsAndSocialStudies: int | None,
                 fe2_PlanningAndImplementingASoftwareProduct_Oral: int | None,
                 fe2_PlanningAndImplementingASoftwareProduct_Written: int | None,
                 fe2_OralSupplementaryExamination: int | None,
                 fe2_OralSupplementaryExaminationSubject: Literal["PlanningASoftwareProduct", "DevelopmentAndImplementationOfAlgorithms", "EconomicsAndSocialStudies"] | None):
        self.set_all_values(
            fe1_ItWorkstation,
            fe2_PlanningASoftwareProduct,
            fe2_DevelopmentAndImplementationOfAlgorithms,
            fe2_EconomicsAndSocialStudies,
            fe2_PlanningAndImplementingASoftwareProduct_Oral,
            fe2_PlanningAndImplementingASoftwareProduct_Written,
            fe2_OralSupplementaryExamination,
            fe2_OralSupplementaryExaminationSubject
        )


    def set_all_values(self,
                       fe1_ItWorkstation: int | None,
                       fe2_PlanningASoftwareProduct: int | None,
                       fe2_DevelopmentAndImplementationOfAlgorithms: int | None,
                       fe2_EconomicsAndSocialStudies: int | None,
                       fe2_PlanningAndImplementingASoftwareProduct_Oral: int | None,
                       fe2_PlanningAndImplementingASoftwareProduct_Written: int | None,
                       fe2_OralSupplementaryExamination: int | None,
                       fe2_OralSupplementaryExaminationSubject: Literal["PlanningASoftwareProduct", "DevelopmentAndImplementationOfAlgorithms", "EconomicsAndSocialStudies"] | None):

        self.fe1_ItWorkstation: int = DataManager._int(fe1_ItWorkstation)
        self.fe2_PlanningASoftwareProduct: int = DataManager._int(fe2_PlanningASoftwareProduct)
        self.fe2_DevelopmentAndImplementationOfAlgorithms: int = DataManager._int(fe2_DevelopmentAndImplementationOfAlgorithms)
        self.fe2_EconomicsAndSocialStudies: int = DataManager._int(fe2_EconomicsAndSocialStudies)
        self.fe2_PlanningAndImplementingASoftwareProduct_Oral: int = DataManager._int(fe2_PlanningAndImplementingASoftwareProduct_Oral)
        self.fe2_PlanningAndImplementingASoftwareProduct_Written: int = DataManager._int(fe2_PlanningAndImplementingASoftwareProduct_Written)
        self.fe2_OralSupplementaryExamination: int = DataManager._int(fe2_OralSupplementaryExamination)
        self.fe2_OralSupplementaryExaminationSubject: Literal["PlanningASoftwareProduct",
        "DevelopmentAndImplementationOfAlgorithms", "EconomicsAndSocialStudies"] | None = fe2_OralSupplementaryExaminationSubject
        self.calculate_all_grades()


    def handle_supplementary_exam(self):

        if self.fe2_OralSupplementaryExaminationSubject == "PlanningASoftwareProduct":
            self.fe2_PlanningASoftwareProduct = DataManager._int(self.calc_supplementary_score(
                self.fe2_OralSupplementaryExamination, self.fe2_PlanningASoftwareProduct))
            
        elif self.fe2_OralSupplementaryExaminationSubject == "DevelopmentAndImplementationOfAlgorithms":
            self.fe2_DevelopmentAndImplementationOfAlgorithms = DataManager._int(self.calc_supplementary_score(
                self.fe2_OralSupplementaryExamination, self.fe2_DevelopmentAndImplementationOfAlgorithms))
            
        elif self.fe2_OralSupplementaryExaminationSubject == "EconomicsAndSocialStudies":
            self.fe2_EconomicsAndSocialStudies = DataManager._int(self.calc_supplementary_score(
                self.fe2_OralSupplementaryExamination, self.fe2_EconomicsAndSocialStudies))


    def calculate_all_grades(self):
        self.handle_supplementary_exam()

        self.fe1_ItWorkstation_Grade: float | None = self.calc_grade(self.fe1_ItWorkstation)
        self.fe2_PlanningASoftwareProduct_Grade: float | None = self.calc_grade(self.fe2_PlanningASoftwareProduct)
        self.fe2_DevelopmentAndImplementationOfAlgorithms_Grade: float | None = self.calc_grade(self.fe2_DevelopmentAndImplementationOfAlgorithms)
        self.fe2_EconomicsAndSocialStudies_Grade: float | None = self.calc_grade(self.fe2_EconomicsAndSocialStudies)

        oral_score: float = float(self.fe2_PlanningAndImplementingASoftwareProduct_Oral)
        written_score: float = float(self.fe2_PlanningAndImplementingASoftwareProduct_Written)

        self.fe2_PlanningAndImplementingASoftwareProduct_Score: int = int(math.ceil(0.5 * oral_score + 0.5 * written_score))
        self.fe2_PlanningAndImplementingASoftwareProduct_Grade: float | None = DataManager.calc_grade(self.fe2_PlanningAndImplementingASoftwareProduct_Score)
    

    @staticmethod
    def _int(value: int | None) -> int:
        return value if value is not None else 0


    @staticmethod
    def calc_grade(score: int | None) -> Optional[float]:
        GRADES_JMPTBL: List[float] = [6.0, 6.0, 6.0, 6.0, 6.0, 5.9, 5.9, 5.9, 5.9, 5.9, 5.8, 5.8, 5.8, 5.8, 5.8, 5.7, 5.7, 5.7, 5.7,
                         5.7, 5.6, 5.6, 5.6, 5.6, 5.6, 5.5, 5.5, 5.5, 5.5, 5.5, 5.4, 5.4, 5.3, 5.3, 5.2, 5.2, 5.1, 5.1,
                         5.0, 5.0, 4.9, 4.9, 4.8, 4.8, 4.7, 4.7, 4.6, 4.6, 4.5, 4.5, 4.4, 4.3, 4.3, 4.2, 4.2, 4.1, 4.0,
                         4.0, 3.9, 3.9, 3.8, 3.8, 3.7, 3.6, 3.6, 3.5, 3.5, 3.4, 3.3, 3.3, 3.2, 3.1, 3.0, 3.0, 2.9, 2.8,
                         2.8, 2.7, 2.6, 2.5, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.4, 1.3,
                         1.3, 1.2, 1.2, 1.1, 1.1, 1.0]
        return GRADES_JMPTBL[score] if score is not None and 0 <= score <= 100 else None


    @staticmethod
    def calc_supplementary_score(supplementary_score: int | None, first_score: int | None) -> Optional[int]:
        fist = DataManager._int(supplementary_score)
        supplementary = DataManager._int(first_score)
        return \
            math.ceil(2/3 * fist + 1/3 * supplementary) \
            if fist is not None and supplementary is not None \
            else None

    def has_passed(self) -> bool:
        return \
            True if \
            self.fe1_ItWorkstation_Grade is not None and self.fe1_ItWorkstation_Grade < 4.5 and \
            self.fe2_PlanningASoftwareProduct_Grade is not None and self.fe2_PlanningASoftwareProduct_Grade < 4.5 and \
            self.fe2_DevelopmentAndImplementationOfAlgorithms_Grade is not None and self.fe2_DevelopmentAndImplementationOfAlgorithms_Grade < 4.5 and \
            self.fe2_EconomicsAndSocialStudies_Grade is not None and self.fe2_EconomicsAndSocialStudies_Grade < 4.5 and \
            self.fe2_PlanningAndImplementingASoftwareProduct_Grade is not None and self.fe2_PlanningAndImplementingASoftwareProduct_Grade < 4.5 and \
            self.fe2_PlanningAndImplementingASoftwareProduct_Oral is not None and self.fe2_PlanningAndImplementingASoftwareProduct_Oral > 48 and \
            self.fe2_PlanningAndImplementingASoftwareProduct_Written is not None and self.fe2_PlanningAndImplementingASoftwareProduct_Written > 48 \
            else False


    def saveToFile(self, fileName):
        with open(fileName, "w") as file:
            json_txt = json.dumps({
                "fe1_ItWorkstation": self.fe1_ItWorkstation,
                "fe2_PlanningASoftwareProduct": self.fe2_PlanningASoftwareProduct,
                "fe2_DevelopmentAndImplementationOfAlgorithms": self.fe2_DevelopmentAndImplementationOfAlgorithms,
                "fe2_EconomicsAndSocialStudies": self.fe2_EconomicsAndSocialStudies,
                "fe2_PlanningAndImplementingASoftwareProduct_Oral": self.fe2_PlanningAndImplementingASoftwareProduct_Oral,
                "fe2_PlanningAndImplementingASoftwareProduct_Written": self.fe2_PlanningAndImplementingASoftwareProduct_Written,
                "fe2_OralSupplementaryExamination": self.fe2_OralSupplementaryExamination,
                "fe2_OralSupplementaryExaminationSubject": self.fe2_OralSupplementaryExaminationSubject
            }, indent=4)

            file.write(json_txt)


    def loadFromFile(self,fileName):
        with open(fileName, "r") as file:
            json_txt = file.read()
            data = json.loads(json_txt)

            self.set_all_values(
                data["fe1_ItWorkstation"],
                data["fe2_PlanningASoftwareProduct"],
                data["fe2_DevelopmentAndImplementationOfAlgorithms"],
                data["fe2_EconomicsAndSocialStudies"],
                data["fe2_PlanningAndImplementingASoftwareProduct_Oral"],
                data["fe2_PlanningAndImplementingASoftwareProduct_Written"],
                data["fe2_OralSupplementaryExamination"],
                data["fe2_OralSupplementaryExaminationSubject"]
            )
