from datetime import datetime
import array
from logging import Exception

# figure array - how it works

class Classes:
    def __init__(self,
                 classID="",
                 courseID = "",
                 noOfSlots=0,
                 trainerAssignedID="",
                 startDate = datetime,
                 endDate = datetime,
                 classMaterials = array):
        self.classID = classID
        self.courseID = courseID
        self.noOfSlots = noOfSlots
        self.trainerAssignedID = trainerAssignedID
        self.startDate = startDate
        self.endDate = endDate
        self.classMaterials = classMaterials

    def get_classID(self):
        return self.classID

    def get_courseID(self):
        return self.courseID

    def get_noOfSlots(self):
        if self.noOfSlots > 0:
            return self.noOfSlots
        else:
            raise Exception("invalid - should not be negative")

    def get_trainerAssignedID(self):
        return self.trainerAssignedID

    def get_startDate(self):
        return self.startDate

    def get_endDate(self):
        return self.endDate

    def get_classMaterials(self):
        return self.classMaterials

# class0 = Classes("G1", "IS213", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
# class1 = Classes("G2", "IS212", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
