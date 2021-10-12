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


t1 = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])

