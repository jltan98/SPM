from datetime import datetime
from logging import exception

class Application:
    def __init__(self,
                 appLearner="",
                 appClassID="",
                 appStatus="", 
                 regStartDate=datetime,
                 regEndDate=datetime,
                 adminID=""):
        self.appLearner = appLearner
        self.appClassID = appClassID
        self.appStatus = appStatus
        self.regStartDate = regStartDate
        self.regEndDate = regEndDate
        self.adminID = adminID

    def get_appLearner(self):
        return self.appLearner

    def get_appClassID(self):
        return self.appClassID

    def get_appStatus(self):
        return self.appStatus

    def get_regStartDate(self):
        return self.regStartDate

    def get_regEndDate(self):
        return self.regEndDate

    def get_adminID(self):
        return self.adminID

    def changeStatus(self, updatedStatus):
        status = self.get_appStatus()
        newStatus = status.replace(status, updatedStatus)
        return newStatus
    
    def checkEnrolmentPeriod(self):
        today = datetime.now()
        if (today > self.get_regEndDate()):
            raise Exception("Self-enrolment Period is over on", self.get_regEndDate, ".")
        return True

a1 = Application("L001", "G2", "Processing", datetime(2021, 8, 1), datetime(2022, 8, 31), "Admin001")