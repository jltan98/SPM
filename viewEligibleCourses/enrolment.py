from datetime import datetime
import array
from logging import raiseExceptions

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
        elif self.noOfSlots == 0:
            raiseExceptions("not available for registration")
        else:
            raiseExceptions("invalid - should not be negative")

    def get_trainerAssignedID(self):
        return self.trainerAssignedID

    def get_startDate(self):
        return self.startDate

    def get_endDate(self):
        return self.endDate

    def get_classMaterials(self):
        return self.classMaterials

class Course:
    def __init__(self,
                 courseID="",
                 courseName="",
                 courseDescription="",
                 prerequisite=[],
                 noOfClasses=0,
                 classes = [],
                 subjectcategory=""):
        self.courseID = courseID
        self.courseName = courseName
        self.courseDescription = courseDescription
        self.prerequisite = prerequisite
        self.noOfClasses = noOfClasses
        self.classes = classes
        self.subjectcategory = subjectcategory

    def get_courseID(self):
        return self.courseID

    def get_courseName(self):
        return self.courseName

    def get_courseDescription(self):
        return self.courseDescription

    def get_prerequisite(self):
        return self.prerequisite

    def get_noOfClasses(self):
        return self.noOfClasses

    def get_classes(self):
        return self.classes

    def get_subjectcategory(self):
        return self.subjectcategory

class Learner:
    def __init__(self,
                 name="",
                 contact="",
                 coursesTaken=[]):
        self.name = name
        self.contact = contact
        self.coursesTaken = coursesTaken

    def get_name(self):
        return self.name

    def get_contact(self):
        return self.contact

    def get_coursesTaken(self):
        return self.coursesTaken

    def courseEligibility(self, prerequisite):
        for courseID in prerequisite:
            if (courseID not in self.coursesTaken):
                raiseExceptions("Not eligible for course")
                return False
        return True

class Trainer:
    def __init__(self,
                 name="",
                 trainerID="",
                 contact="",
                 skills=[],
                 experience="",
                 coursesTaught=[]):
        self.name = name
        self.trainerID = trainerID
        self.contact = contact
        self.skills = skills
        self.experience = experience
        self.coursesTaught = coursesTaught

    def get_name(self):
        return self.name

    # trainerID unique value
    def get_trainerID(self):
        return self.trainerID

    def get_contact(self):
        return self.contact

    def get_skills(self):
        return self.skills

    def get_experience(self):
        return self.experience

    def get_coursesTaught(self):
        return self.coursesTaught