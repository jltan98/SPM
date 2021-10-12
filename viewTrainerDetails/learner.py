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

# Return True/False based on the eligibility of courses
    def eligiblecourses(self):
        pass

learner1 = Learner('Phris', "phris@smu.edu.sg", ["IS111","IS212", "IS213", "IS215"])

print(learner1.get_name())
print(learner1.get_contact())
print(learner1.get_coursesTaken())
