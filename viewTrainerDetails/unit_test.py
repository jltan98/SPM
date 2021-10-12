import unittest
from unittest import mock
from datetime import datetime
from learner import Learner
from trainer import Trainer
from course import Course
from classes import Classes

class TestViewTrainers(unittest.TestCase):
    # Check if trainer exists >> ID, Name
    def test_existTrainer(self):
        trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        trainerID = trainer.get_trainerID()
        trainerName = trainer.get_name()
        self.assertEqual(trainerID, "T001")
        self.assertEqual(trainerName, "Chris")

    # Check on the list of courses taught
    def test_existCoursesTaught(self):
        trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        coursesTaught = trainer.get_coursesTaught()
        self.assertEqual(coursesTaught, ["IS212", "IS213", "IS215"])

    # Check the skills and experiences of trainer exists
    def test_existSkillsExperience(self):
        trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])
        skill = trainer.get_skills()
        exp = trainer.get_experience()
        self.assertEqual(skill, ["project management", "product services", "software development"])
        self.assertEqual(exp, "3-years experience in customer service...")

