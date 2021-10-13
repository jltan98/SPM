class Learner:
    def __init__(self,
                 name="",
                 id="",
                 contact="",
                 coursesTaken=[]):
        self.name = name
        self.id = id
        self.contact = contact
        self.coursesTaken = coursesTaken

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id
        
    def get_contact(self):
        return self.contact

    def get_coursesTaken(self):
        return self.coursesTaken
        
    def checkCourseTaken(self, courseID):
        if (courseID not in self.coursesTaken):
            return self.coursesTaken
        else:
            raise Exception("Course already taken before")

    def courseEligibility(self, prerequisite):
        for courseID in prerequisite:
            if (courseID not in self.coursesTaken):
                raise Exception("Ineligible - did not fulfil prerequisite")
        return self.coursesTaken            

learner1 = Learner('Phris', "L001", "phris@smu.edu.sg", ["IS111", "IS213", "IS215"])