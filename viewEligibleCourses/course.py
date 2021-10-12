
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

c1 = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
