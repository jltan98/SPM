import unittest
from unittest import mock
from datetime import datetime
from learner import Learner
from trainer import Trainer
from course import Course
from classes import Classes

class TestViewEligibleCourses(unittest.TestCase):

    def setUp(self):
        self.learner = Learner('Phris', "L001", "phris@smu.edu.sg", ["IS111", "IS213", "IS215"]) 
        self.course = Course('IS212', "Software Project Management", "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.", ["IS111", "IS213"], 1, ["G1"], "Software Development")
        self.class1 = Classes("G1", "IS213", 20, "T001", datetime(2021, 10, 27), datetime(2022, 1, 31), [])
        self.trainer = Trainer('Chris', "T001", "chris@smu.edu.sg", ["project management", "product services", "software development"], "3-years experience in customer service...", ["IS212", "IS213", "IS215"])

    def tearDown(self):
        self.learner = None
        self.course = None
        self.class1 = None
        self.trainer = None

    # Check if learner is eligible for the course, and course must not be taken before
    def test_eligibility(self):
        prerequisite = self.course.get_prerequisite()
        self.assertEqual(prerequisite, ["IS111", "IS213"])
        # course must not be taken before
        self.assertTrue(self.course.get_courseID() not in self.learner.get_coursesTaken())
        self.assertRaises(Exception, self.learner.checkCourseTaken, 'IS213')
        # if prerequisite has been cleared
        self.assertEqual(self.learner.courseEligibility(prerequisite), self.learner.get_coursesTaken())
        self.assertRaises(Exception, self.learner.courseEligibility, ['IS200'])

    # number of slots available for registration
    def test_slots(self):
        slots = self.class1.get_noOfSlots()
        self.assertEqual(slots, 20)

    # start and end date of classes are stipulated
    def test_existPeriod(self):
        startdate = self.class1.get_startDate()
        enddate = self.class1.get_endDate()
        self.assertEqual(startdate, datetime(2021, 10, 27))
        self.assertEqual(enddate, datetime(2022, 1, 31))

    # course description is indicated
    def test_existDescription(self):
        desc = self.course.get_courseDescription()
        self.assertEqual(desc, "Software project management is dedicated to the planning, scheduling, resource allocation, execution, tracking, and delivery of software and web projects.")

    # assigned trainer is indicated for each classes
    def test_existTrainer(self):
        trainerID = self.trainer.get_trainerID()
        assignedtrainer = self.class1.get_trainerAssignedID()
        self.assertEqual(assignedtrainer, "T001")
        self.assertEqual(trainerID, assignedtrainer)

    # check if subject categories for courses exist
    def test_existSubjectCat(self):
        subjectCat = self.course.get_subjectcategory()
        self.assertEqual(subjectCat, "Software Development")

if __name__ == "__main__":
    unittest.main()


