import unittest
from unittest import mock
from datetime import datetime
from trainer import Trainer


class TestViewTrainers(unittest.TestCase):

    def setUp(self):
        self.trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
    
    def tearDown(self):
        self.trainer = None

    # Check if trainer exists >> ID, Name
    def test_existTrainer(self):
        trainerID = self.trainer.get_trainerID()
        trainerName = self.trainer.get_name()
        self.assertEqual(trainerID, "T001")
        self.assertEqual(trainerName, "Chris")

    # Check on the list of courses taught
    def test_existCoursesTaught(self):
        coursesTaught = self.trainer.get_coursesTaught()
        self.assertEqual(coursesTaught, ["IS212", "IS213", "IS215"])

    # Check the skills and experiences of trainer exists
    def test_existSkillsExperience(self):
        skill = self.trainer.get_skills()
        exp = self.trainer.get_experience()
        self.assertEqual(skill, ["project management", "product services", "software development"])
        self.assertEqual(exp, "3-years experience in customer service...")

if __name__ == "__main__":
    unittest.main()
